# app.py
# Streamlit app with Groq LLM - FREE and SUPER FAST!

import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="AI Chatbot with Groq",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        align-items: flex-end;
    }
    .assistant-message {
        background-color: #f5f5f5;
        align-items: flex-start;
    }
    </style>
""", unsafe_allow_html=True)

# Get Groq API key from secrets or environment
def get_groq_api_key():
    try:
        return st.secrets["GROQ_API_KEY"]
    except:
        return os.getenv("GROQ_API_KEY")

GROQ_API_KEY = get_groq_api_key()

if not GROQ_API_KEY:
    st.error("⚠️ Groq API key not found!")
    st.info("Create .streamlit/secrets.toml with:\nGROQ_API_KEY = \"your-api-key\"")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_input" not in st.session_state:
    st.session_state.last_input = None
if "processing" not in st.session_state:
    st.session_state.processing = False

if "groq_client" not in st.session_state:
    if GROQ_API_KEY:
        try:
            st.session_state.groq_client = Groq(api_key=GROQ_API_KEY)
            st.session_state.model_loaded = True
        except Exception as e:
            st.session_state.model_loaded = False
            st.session_state.error_message = str(e)
    else:
        st.session_state.model_loaded = False
        st.session_state.error_message = "Groq API key not found"

# Available Groq models
GROQ_MODELS = {
    "Llama 3.1 70B (Recommended)": "llama-3.1-70b-versatile",
    "Llama 3.1 8B (Faster)": "llama-3.1-8b-instant",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it"
}

# Sidebar
with st.sidebar:
    st.title("⚡ AI Chatbot with Groq")
    st.markdown("**FREE & Lightning Fast!**")
    st.markdown("---")
    
    # Model status
    st.subheader("Status")
    if st.session_state.get("model_loaded"):
        st.success("✅ Connected to Groq")
    else:
        st.error("❌ Not connected")
        st.warning(st.session_state.get("error_message", "Unknown error"))
        
        # Show instructions to add API key
        with st.expander("🔑 How to get FREE Groq API Key"):
            st.markdown("""
            1. Go to [console.groq.com](https://console.groq.com)
            2. Sign up (FREE, no credit card!)
            3. Go to API Keys section
            4. Create new API key
            5. Copy the key
            
            **For Streamlit Cloud:**
            - App settings → Secrets
            - Add: `GROQ_API_KEY = "gsk_..."`
            
            **For local testing:**
            - Create `.env` file
            - Add: `GROQ_API_KEY=gsk_...`
            """)
    
    st.markdown("---")
    
    # Model selection
    st.subheader("Model Settings")
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "Llama 3.1 70B (Recommended)"
    
    model_name = st.selectbox(
        "Choose Model",
        options=list(GROQ_MODELS.keys()),
        index=0
    )
    st.session_state.selected_model = model_name
    
    # Temperature
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    
    # Max tokens
    max_tokens = st.slider("Max Tokens", 100, 4000, 1024, 100)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Info
    st.subheader("About")
    st.info(
        "**Powered by Groq**\n\n"
        "- ⚡ Ultra-fast inference\n"
        "- 🆓 FREE API access\n"
        "- 🚀 Multiple models\n"
        "- 🔒 Secure & private\n\n"
        "Groq uses LPU technology for blazing-fast AI!"
    )
    
    # Message count
    if st.session_state.messages:
        st.markdown("---")
        st.metric("Total Messages", len(st.session_state.messages))

# Main chat interface
st.title("💬 Chat with AI Assistant")

if not st.session_state.get("model_loaded"):
    st.error("⚠️ Please configure your Groq API key to start chatting.")
    st.info("👈 Check the sidebar for instructions on getting a FREE API key!")
    
    # Big call-to-action
    st.markdown("---")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        ### 🎉 Get Started in 2 Minutes!
        
        1. Visit [console.groq.com](https://console.groq.com)
        2. Sign up FREE (no credit card!)
        3. Get your API key
        4. Add it to settings
        
        **That's it!** Start chatting with AI instantly! ⚡
        """)
else:
    st.markdown(f"Ask me anything! Powered by **{st.session_state.selected_model}** ⚡")

    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(
                f'<div class="chat-message user-message"><b>You:</b><br>{content}</div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-message assistant-message"><b>Assistant:</b><br>{content}</div>', 
                unsafe_allow_html=True
            )

    # Chat input and processing
    user_input = st.chat_input("Type your message here... ⚡")

    if user_input and not st.session_state.processing and user_input != st.session_state.last_input:
        try:
            st.session_state.processing = True
            st.session_state.last_input = user_input
            
            # Add user message to chat
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
            
            with st.spinner("Thinking... ⚡"):
                # Prepare messages for Groq API
                api_messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Provide clear, concise, and friendly responses."
                    }
                ]
                api_messages.extend(st.session_state.messages[-10:])
                
                # Get response from Groq
                chat_completion = st.session_state.groq_client.chat.completions.create(
                    messages=api_messages,
                    model=GROQ_MODELS[st.session_state.selected_model],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    stream=False
                )
                
                # Add assistant response to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": chat_completion.choices[0].message.content
                })
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            if st.session_state.messages:
                st.session_state.messages.pop()  # Remove failed message
        finally:
            st.session_state.processing = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with Streamlit ⚡ Powered by Groq | FREE & Lightning Fast! ⚡"
    "</div>",
    unsafe_allow_html=True
)