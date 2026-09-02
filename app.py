import streamlit as st
import time

# Page Config
st.set_page_config(page_title="Enterprise Assistant", page_icon="🤖")

# --- MOCK DATA & CONFIG ---
BAD_WORDS = ["stupid", "idiot", "dumb", "badword", "abuse"]

HR_POLICIES = {
    "leave": "Employees are entitled to 20 days of paid leave per year. Leave can be applied via the HR Portal.",
    "remote": "Remote work is allowed up to 2 days a week with your direct manager's approval.",
    "salary": "Salaries are credited on the last working day of every month."
}

IT_SUPPORT = {
    "password": "To reset your password, visit the IT portal at it.company.com and click 'Forgot Password'.",
    "wifi": "The guest Wi-Fi password is 'Welcome2026'.",
    "laptop": "For hardware issues, please raise a ticket on the IT helpdesk and drop your laptop at Desk 4B."
}

# --- FUNCTIONS ---
def check_bad_language(text):
    for word in BAD_WORDS:
        if word in text.lower():
            return True
    return False

def generate_mock_response(query):
    query_lower = query.lower()
    
    # Simple keyword matching for mock responses
    if "hr" in query_lower or "leave" in query_lower or "salary" in query_lower:
        if "leave" in query_lower:
            return HR_POLICIES["leave"]
        elif "salary" in query_lower:
            return HR_POLICIES["salary"]
        else:
            return "For HR related queries, please specify if it's about leave, remote work, or salary."
            
    elif "it" in query_lower or "password" in query_lower or "wifi" in query_lower:
        if "password" in query_lower:
            return IT_SUPPORT["password"]
        elif "wifi" in query_lower:
            return IT_SUPPORT["wifi"]
        else:
            return "For IT support, you can ask about password reset, wifi, or laptop issues."
            
    elif "event" in query_lower or "townhall" in query_lower:
        return "The next company Townhall is scheduled for this Friday at 3 PM in the Main Auditorium."
        
    elif "hi" in query_lower or "hello" in query_lower:
        return "Hello! I am your Intelligent Enterprise Assistant. How can I help you with HR policies, IT support, or other organizational matters today?"
        
    else:
        return "I am a basic AI assistant right now. I didn't quite understand that. Please ask about HR policies, IT support, or company events."

# --- AUTHENTICATION (Mock 2FA) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Login - Enterprise Assistant")
    st.write("Please authenticate using 2-Factor Authentication.")
    
    email = st.text_input("Corporate Email ID")
    
    if email:
        st.success(f"OTP sent to {email}. (For demo, just type: 1234)")
        otp = st.text_input("Enter OTP", type="password")
        
        if st.button("Verify OTP & Login"):
            if otp == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid OTP. Please try again.")

else:
    # --- MAIN APP ---
    st.title("🤖 Intelligent Enterprise Assistant")
    st.write("Ask me anything about HR, IT, or upload a document for processing.")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
        
    # --- DOCUMENT PROCESSING ---
    st.sidebar.header("📄 Document Processing")
    st.sidebar.write("Upload a document to extract information.")
    uploaded_file = st.sidebar.file_uploader("Upload PDF/TXT Document", type=["txt", "pdf"])
    
    if uploaded_file is not None:
        st.sidebar.success(f"'{uploaded_file.name}' uploaded successfully!")
        if st.sidebar.button("Summarize / Extract Info"):
            with st.spinner("Processing document..."):
                # Simulating processing time (< 5 seconds)
                time.sleep(2) 
                st.sidebar.markdown("### 📝 Extracted Summary")
                st.sidebar.info(
                    "**Mock Output:** The document primarily discusses new organizational strategies for Q3. "
                    "Key focus areas include improving internal communication, upgrading IT infrastructure, "
                    "and revising remote work policies."
                )

    # --- CHAT INTERFACE ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is your question?"):
        
        # Display user message
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 1. Filter Bad Language
        if check_bad_language(prompt):
            response = "⚠️ **System Warning:** Your message contains inappropriate language blocked by our dictionary. Please maintain professional decorum."
        else:
            # 2. Generate Response (Mock AI with < 5s delay)
            with st.spinner("Thinking..."):
                time.sleep(1) 
                response = generate_mock_response(prompt)

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)
            
        st.session_state.messages.append({"role": "assistant", "content": response})
