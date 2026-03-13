import gradio as gr
from ellai import Ellai
from utils import load_system_prompt

system_prompt = load_system_prompt()
ellai = Ellai(system_prompt=system_prompt)

def chat_gradio(prompt: str, messages: list):
    # Add user message to UI.
    messages.append(gr.ChatMessage(role="user", content=prompt))
    yield messages, gr.update(value="", interactive=False)

    # Append to Ellai's internal history.
    ellai.messages.append({"role": "user", "content": prompt})

    while True:
        from ollama import chat, ChatResponse
        response: ChatResponse = chat(
            model=ellai.model,
            messages=ellai.messages,
            tools=ellai.available_tools.values(),
            think=False,
            options=ellai.model_options
        )

        # Append raw response message to Ellai's history.
        ellai.messages.append(response.message)

        if response.message.thinking:
            messages.append(gr.ChatMessage(
                role="assistant",
                content=response.message.thinking,
                metadata={"title": "💭 Thinking..."}
            ))
            yield messages, gr.update()

        if response.message.tool_calls:
            for tool_call in response.message.tool_calls:
                function_to_call = ellai.available_tools.get(tool_call.function.name)
                if function_to_call:
                    args = tool_call.function.arguments
                    result = function_to_call(**args)
                    result_str = str(result)[:4000 * 4]

                    # Correct role for tool results.
                    ellai.messages.append({
                        "role": "tool",
                        "content": result_str,
                        "tool_name": tool_call.function.name
                    })
                    messages.append(gr.ChatMessage(
                        role="assistant",
                        content=result_str,
                        metadata={"title": f"🔧 Called: {tool_call.function.name}"}
                    ))
                else:
                    ellai.messages.append({
                        "role": "tool",
                        "content": f"Tool {tool_call.function.name} not found",
                        "tool_name": tool_call.function.name
                    })
                    messages.append(gr.ChatMessage(
                        role="assistant",
                        content=f"Tool `{tool_call.function.name}` not found",
                        metadata={"title": "⚠️ Tool error"}
                    ))
                yield messages, gr.update()

        else:
            # Final response.
            if response.message.content:
                messages.append(gr.ChatMessage(
                    role="assistant",
                    content=response.message.content
                ))
                yield messages, gr.update()
            break

    yield messages, gr.update(interactive=True)

def reset_chat():
    ellai.reset()
    ellai.messages = [{"role": "system", "content": load_system_prompt()}]
    return [], ""

with gr.Blocks() as demo:
    gr.Markdown("# Chat with Ellai 🤖")
    chatbot = gr.Chatbot(
        label="Ellai",
        avatar_images=(
            None,
            "https://em-content.zobj.net/source/twitter/141/parrot_1f99c.png",
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