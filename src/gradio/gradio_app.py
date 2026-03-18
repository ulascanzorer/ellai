import gradio as gr
from src.core.ellai import Ellai
from src.core.utils import load_system_prompt
from ollama import chat
from typing import List

system_prompt = load_system_prompt()
ellai = Ellai(system_prompt=system_prompt)

def chat_gradio(prompt: str, messages: List[gr.ChatMessage]):
    messages.append(gr.ChatMessage(role="user", content=prompt))
    yield messages, gr.update(value="", interactive=False)

    ellai.messages.append({"role": "user", "content": prompt})

    while True:
        stream = chat(
            model=ellai.model,
            messages=ellai.messages,
            tools=ellai.available_tools.values(),
            stream=True,
            think=False,
            options=ellai.model_options
        )

        thinking = ""
        content = ""
        tool_calls = []

        for chunk in stream:
            if chunk.message.thinking:
                if not thinking:    # This is the first thinking chunk.
                    messages.append(gr.ChatMessage(role="assistant", content="", metadata={ "title": "Thinking..." }))
                    
                thinking += chunk.message.thinking
                messages[-1].content = thinking
                yield messages, gr.update()
            if chunk.message.content:
                if not content:     # This is the first actual content chunk.
                    messages.append(gr.ChatMessage(role="assistant", content=""))
                
                content += chunk.message.content
                messages[-1].content = content
                yield messages, gr.update()
            if chunk.message.tool_calls:
                if not tool_calls:  # This is the first tool call chunk.
                    messages.append(gr.ChatMessage(role="assistant", content="", metadata= { "title": "Tool call..." }))
                
                tool_calls.extend(chunk.message.tool_calls)
        
        if thinking or content or tool_calls:
            ellai.messages.append({"role": "assistant", "thinking": thinking, "content": content, "tool_calls": tool_calls})

        if not tool_calls:
            break

        for call in tool_calls:
            function_to_call = ellai.available_tools.get(call.function.name)
            if function_to_call:
                result = function_to_call(**call.function.arguments)
                result = str(result)[:20000]    # Cutting off the result by an arbitrary length to not occupy too much of the context window.
            else:
                result = "Unknown tool"

            ellai.messages.append({"role": "tool", "tool_name": call.function.name, "content": result})

            messages[-1].metadata = { "title": call.function.name }
            messages[-1].content += result
            yield messages, gr.update()

    yield messages, gr.update(interactive=True)

def reset_chat():
    ellai.reset()
    ellai.messages = [{"role": "system", "content": load_system_prompt()}]
    return [], ""

with gr.Blocks() as demo:
    gr.Markdown("# Chat with Ellai; your helpful, private AI assistant 🤖")
    chatbot = gr.Chatbot(
        label="Ellai",
        avatar_images=(
            None,
            "https://em-content.zobj.net/source/twitter/376/robot_1f916.png",
        ),
        height=600,
    )
    with gr.Row():
        user_input = gr.Textbox(
            lines=1,
            label="Message",
            placeholder="Type your message...",
            scale=9
        )
        reset_btn = gr.Button("🔄 Reset", scale=1)

    user_input.submit(
        chat_gradio,
        inputs=[user_input, chatbot],
        outputs=[chatbot, user_input]
    )
    reset_btn.click(reset_chat, outputs=[chatbot, user_input])

demo.launch()