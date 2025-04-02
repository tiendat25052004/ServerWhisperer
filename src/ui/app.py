import gradio as gr
from src.core.memory import ChatMemory
from src.core.agent import ServerWhispererAgent

class ServerWhispererUI:
    """
    UI for the Server Whisperer application
    """
    def __init__(self):
        """Initialize the UI with memory and agent"""
        self.memory = ChatMemory()
        self.agent = ServerWhispererAgent()
    
    def respond(self, message, chat_history):
        """Process user message and generate response"""
        try:
            message = message.strip()
            if not message:
                return "", chat_history
            
            # Add user message to memory and chat history
            self.memory.add_message("user", message)
            chat_history.append({"role": "user", "content": message})
            
            # Show thinking indicator
            yield "", chat_history + [{"role": "assistant", "content": "I am thinking bro, wait..."}]
            
            # Get context and process request
            context = self.memory.get_context()
            full_input = f"Context:\n{context}\n\nNew request: {message}"
            response = self.agent.process_request(full_input)
            
            # Add response to memory and update chat history
            self.memory.add_message("assistant", response)
            chat_history.append({"role": "assistant", "content": response})
            yield "", chat_history
            
        except Exception as e:
            error_msg = f"⚠️ An error occurred: {str(e)}"
            chat_history.append({"role": "assistant", "content": error_msg})
            return "", chat_history
    
    def clear_chat(self):
        """Clear chat history and memory"""
        self.memory.clear()
        return "", []
    
    def toggle_examples(self, visible):
        """Toggle visibility of examples section"""
        return gr.update(visible=not visible)


def create_app():
    """Create and configure the Gradio application"""
    ui = ServerWhispererUI()
    
    app = gr.Blocks(
        title="🖥️ ServerWhisperer",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {max-width: 2000px !important}
        .chatbot-container {
            max-width: 900px !important; 
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 10px;
            background-color: #f9f9f9;
        }
        """
    )
    
    with app:
        # Header
        gr.Markdown("""
        <div style="text-align: center;">
            <h1>🖥️ServerWhisperer</h1>
            <p>Chatbot for SSH-based server and Docker management.</p>
        </div>
        """)
        
        # Chatbot interface with improved styling
        chatbot = gr.Chatbot(
            label="Conversation History",
            height=600,
            bubble_full_width=False,
            avatar_images=(
                "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",  # User avatar
                "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"    # AI avatar
            ),
            type="messages",
            render_markdown=True
        )
        
        # Input area
        with gr.Row():
            msg = gr.Textbox(
                label="Enter your request",
                placeholder="E.g.: Show docker logs --tail 100 from container 'nginx' on server 'prod-01' and upload to minIO",
                scale=7,
                container=False
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)
        
        # Control buttons
        with gr.Row():
            clear_btn = gr.Button("🧹 Clear Chat")
            examples_btn = gr.Button("📋 Show Examples")
        
        # Examples column
        examples_col = gr.Column(visible=False)
        with examples_col:
            gr.Markdown("### 💡 Example Requests")
            examples = gr.Examples(
                examples=[
                    ["Get docker logs --tail 50 from container 'my-nginx' on server 'datruong' and upload to minIO"],
                    ["What is 10 + 20?"],
                    ["Tell me a joke"],
                    ["Get docker logs from container 'my-nginx' on server 'datruong', analyse and send an email to taiqp90@gmail.com"]
                ],
                inputs=msg,
                label="Click to try"
            )
        
        # Event handlers
        msg.submit(
            ui.respond,
            [msg, chatbot],
            [msg, chatbot]
        )
        
        submit_btn.click(
            ui.respond,
            [msg, chatbot],
            [msg, chatbot]
        )
        
        clear_btn.click(
            ui.clear_chat,
            outputs=[msg, chatbot]
        )
        
        # Examples button click handler
        examples_btn.click(
            lambda: ui.toggle_examples(examples_col.visible),
            outputs=examples_col
        )
    
    return app