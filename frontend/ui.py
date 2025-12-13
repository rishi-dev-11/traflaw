import streamlit as st
import requests

# --- Configuration ---
API_URL = "http://127.0.0.1:8000/ask"
st.set_page_config(page_title="Traffic Law AI", page_icon="⚖️", layout="wide")

# --- UI Styling ---
st.title("⚖️ Indian Traffic Law Assistant")
st.markdown("""
<style>
    .source-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask about penalties, acts, or case laws..."):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Searching legal database...")
        
        try:
            # Call FastAPI Backend
            payload = {"query": prompt, "top_k": 5}
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            
            answer = data["answer"]
            sources = data["sources"]

            # Display Answer
            message_placeholder.markdown(answer)
            
            # Display Sources in an Expander
            with st.expander("📚 View Legal Sources & Context"):
                for idx, source in enumerate(sources):
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {idx+1}: {source['source']}</strong> 
                        <span style="float:right; color:gray">Score: {source['score']:.2f}</span><br>
                        <em>{source['text'][:300]}...</em>
                    </div>
                    """, unsafe_allow_html=True)

            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except requests.exceptions.ConnectionError:
            message_placeholder.error("❌ Could not connect to the backend. Is FastAPI running?")
        except Exception as e:
            message_placeholder.error(f"❌ Error: {str(e)}")

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    st.info("This bot retrieves information from the Motor Vehicles Act (1988) and related Indian court cases.")
    st.markdown("---")
    st.write("🔧 **Backend:** FastAPI + Pinecone")
    st.write("🧠 **Model:** Claude 3 Sonnet")