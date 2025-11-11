import streamlit as st
from langchain_groq import ChatGroq
from io import BytesIO
import json

# -------------------------------
# 1️⃣  Initialize App & Session
# -------------------------------
st.set_page_config(page_title="Candidate Dashboard", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# 2️⃣  Authentication
# -------------------------------
def login_page():
    st.title("🔐 Candidate Login / Signup")
    choice = st.radio("Select Action", ["Login", "Signup"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button(choice):
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Please fill all fields.")

def logout_button():
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# -------------------------------
# 3️⃣  Groq LLM Utility
# -------------------------------
def call_groq_llm(prompt):
    """Stub for Groq API - replace with actual implementation"""
    # Example: chat = ChatGroq(api_key="YOUR_KEY", model="llama3-70b-8192")
    # response = chat([HumanMessage(content=prompt)])
    # return response.content
    return f"[LLM Response Placeholder for Prompt: {prompt[:80]}...]"

# -------------------------------
# 4️⃣  Resume Management Tab
# -------------------------------
def resume_management():
    st.header("📄 Resume Management")
    mode = st.radio("Choose Option", ["Upload CV", "Paste CV Text", "Get from LinkedIn", "Form-Based CV"])

    if mode == "Upload CV":
        file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
        if file:
            st.success("✅ Resume uploaded successfully.")
    elif mode == "Paste CV Text":
        text = st.text_area("Paste your Resume Content")
    elif mode == "Get from LinkedIn":
        link = st.text_input("Paste your LinkedIn Profile URL")
    else:
        st.info("Form-based CV builder coming soon...")

    st.subheader("📊 View Resume As:")
    view = st.radio("View Format", ["PDF", "Markdown", "JSON"])
    st.button("Download Resume")

# -------------------------------
# 5️⃣  Job Descriptions Tab
# -------------------------------
def job_descriptions():
    st.header("💼 Job Descriptions (JD)")
    col1, col2 = st.columns(2)
    with col1:
        skill = st.text_input("Search by Skill (e.g., Python, ML, React)")
        job_type = st.selectbox("Job Type", ["All", "Remote", "Onsite"])
    with col2:
        if st.button("🔍 Search JD"):
            st.info(f"Showing jobs for '{skill}' - {job_type}")
    
    st.markdown("### Upload / Paste JD")
    jd_file = st.file_uploader("Upload JD (PDF/DOCX)", type=["pdf", "docx"])
    jd_text = st.text_area("Or paste JD text")
    jd_link = st.text_input("JD Web Link / LinkedIn URL")

# -------------------------------
# 6️⃣  Match Resume & JD Tab
# -------------------------------
def match_cv_jd():
    st.header("🔍 Match Resume with JD")
    st.write("Upload or Select Resume and JD to compute LLM-based Match Score")
    if st.button("Match CV with JD"):
        result = call_groq_llm("Compare resume with JD and provide ranked matches.")
        st.success(result)

# -------------------------------
# 7️⃣  Cover Letter Tab
# -------------------------------
def cover_letter():
    st.header("📝 Cover Letter Generator")
    jd = st.text_area("Paste the JD")
    resume = st.text_area("Paste your Resume")
    if st.button("Generate Cover Letter"):
        letter = call_groq_llm(f"Write a personalized cover letter for this JD:\n{jd}\nUsing resume:\n{resume}")
        st.text_area("Generated Cover Letter", value=letter, height=300)
        st.download_button("Download Cover Letter", data=letter, file_name="cover_letter.txt")

# -------------------------------
# 8️⃣  Mock Interview Tab
# -------------------------------
def mock_interview():
    st.header("🎙️ Mock Interview & Evaluation")
    jd_text = st.text_area("Paste JD for Interview Context")
    if st.button("Start Interview"):
        question = call_groq_llm(f"Generate first interview question for JD:\n{jd_text}")
        st.write(f"**Question:** {question}")

# -------------------------------
# 9️⃣  Skill Evaluation Tab
# -------------------------------
def skill_evaluation():
    st.header("🧠 Skill Evaluation")
    skills = st.text_area("Enter your key skills (comma-separated)")
    if st.button("Evaluate"):
        evaluation = call_groq_llm(f"Evaluate these skills: {skills}")
        st.json({"Evaluation": evaluation})

# -------------------------------
# 🔟  Skill Roadmap Tab
# -------------------------------
def skill_roadmap():
    st.header("📘 Skill Gap & Roadmap")
    jd_text = st.text_area("Paste JD to find skill gap")
    resume_text = st.text_area("Paste Resume")
    if st.button("Generate Roadmap"):
        roadmap = call_groq_llm(f"Find skill gaps between this JD and Resume, and suggest a course roadmap:\n{jd_text}\n{resume_text}")
        st.markdown(roadmap)

# -------------------------------
# 🔸 Main Dashboard Layout
# -------------------------------
def dashboard():
    st.sidebar.title(f"👤 {st.session_state.username}'s Dashboard")
    logout_button()
    tabs = st.sidebar.radio("📂 Modules", [
        "Dashboard Overview",
        "Resume Management",
        "Job Descriptions",
        "Match Resume & JD",
        "Cover Letter",
        "Mock Interview",
        "Skill Evaluation",
        "Skill Roadmap"
    ])

    if tabs == "Dashboard Overview":
        st.title("📊 Candidate Dashboard Overview")
        st.info("Welcome! Navigate from sidebar to access each feature.")
    elif tabs == "Resume Management":
        resume_management()
    elif tabs == "Job Descriptions":
        job_descriptions()
    elif tabs == "Match Resume & JD":
        match_cv_jd()
    elif tabs == "Cover Letter":
        cover_letter()
    elif tabs == "Mock Interview":
        mock_interview()
    elif tabs == "Skill Evaluation":
        skill_evaluation()
    elif tabs == "Skill Roadmap":
        skill_roadmap()

# -------------------------------
# 🚀  Run App
# -------------------------------
if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
