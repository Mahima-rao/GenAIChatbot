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

    # Show user ID and format message
    user_msg = f"👤 {user_id}: {message}"
    bot_msg = f"🤖 Bot: {reply}"
    history.append((user_msg, bot_msg))
    return "", history

# Build the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 ZenBot")

    with gr.Row():
        user_id_dropdown = gr.Dropdown(
            choices=["Shashi", "Jo", "Magda","None"],
            label="Select User",
            value="None"
        )

    chatbot = gr.Chatbot(label="Chat History")
    message_box = gr.Textbox(placeholder="Type your message here...", label="Your Message")
    send_button = gr.Button("Send")

    # Send button click triggers chat
    send_button.click(
        chat_with_bot,
        inputs=[message_box, chatbot, user_id_dropdown],
        outputs=[message_box, chatbot]
    )

    # Hitting enter also sends message
    message_box.submit(
        chat_with_bot,
        inputs=[message_box, chatbot, user_id_dropdown],
        outputs=[message_box, chatbot]
    )

demo.launch()
