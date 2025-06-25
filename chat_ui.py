import gradio as gr
import requests

API_URL = "http://localhost:8000/chat"

# Main chatbot function
def chat_with_bot(message, history, user_id):
    try:
        res = requests.post(API_URL, json={
            "user_id": user_id,
            "message": message
        })
        reply = res.json().get("response", "⚠️ No response.")
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"
    history.append((message, reply))
    return "", history

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 AI Customer Support Chatbot")

    with gr.Row():
        user_id_dropdown = gr.Dropdown(
            choices=["user1", "user2", "user3"],
            label="Select User",
            value="None"
        )

    chatbot = gr.Chatbot(label="Chat History")
    message_box = gr.Textbox(placeholder="Type your message here...", label="Your Message")
    send_button = gr.Button("Send")

    # Connect button and textbox to function
    send_button.click(
        chat_with_bot,
        inputs=[message_box, chatbot, user_id_dropdown],
        outputs=[message_box, chatbot]
    )

    message_box.submit(
        chat_with_bot,
        inputs=[message_box, chatbot, user_id_dropdown],
        outputs=[message_box, chatbot]
    )

demo.launch()
