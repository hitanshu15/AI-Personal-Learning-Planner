import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AI Learning Planner",
    page_icon="🎓",
    layout="wide"
)
# =====================================================
# CUSTOM CSS (UI ENHANCEMENT)
# =====================================================
st.markdown("""
<style>
.main-title {
    font-size: 2.4rem;
    font-weight: 700;
}
.subtitle {
    color: #6b7280;
    font-size: 1.1rem;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 600;
}
.small-text {
    color: #9ca3af;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE INIT
# =====================================================
if "final_result" not in st.session_state:
    st.session_state.final_result = None

if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None

# =====================================================
# HEADER
# =====================================================
st.markdown('<div class="main-title">🎓 AI Personal Learning Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get a clear, structured 30-day roadmap tailored to your career goals</div>', unsafe_allow_html=True)
st.divider()

# =====================================================
# ENV & MODEL SETUP
# =====================================================
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    st.error("🚨 GROQ_API_KEY not found. Please set it in your .env file.")
    st.stop()

try:
    model = ChatGroq(model="openai/gpt-oss-120b")
except Exception:
    st.error("❌ Failed to initialize language model.")
    st.stop()

parser = StrOutputParser()

# =====================================================
# PROMPTS
# =====================================================

prompt_1 = PromptTemplate(template= """ 
 You are a career learning advisor.

Target Role: {target_role} 
User Skills: {skills}

Tasks:
1. List core skills required for the role
2. Identify which skills the user already has
3. Identify missing or weak skills
4. Explain assumptions clearly

Return structured output.
""",
input_variables=["skills","target_role"]
)

###########################################################


prompt_2 = PromptTemplate(template= """ 

Based on the following skill gap analysis:
{gap_analysis}

Give only information which is ask in bullet points.(short + clear with proper reasoning) 
1) user skills which it already has list it out.
2) Skill Assessment.
3) missing or weak skills.
4) Required Skills for the role.
                          

Create a 30-day learning plan.


Rules:
- Start from fundamentals
- Avoid overload
- Each day must include:
  - Objective
  - 2–4 tasks create 
  - Suggested learning resources
- Practical and achievable
- Split the plan week by week.
- It should be in structured tabluer as per week. 
- Task column should be should simple one line sentence for user to understand do not use high vocab.

                                         
Format clearly by day and child can also understand structure should that excellent not confusing.
you must output structured reasoning + a realistic 30-day plan, not motivational text.

please stay on topic do not answer if qeustion is asked out of the topic. say sorry i can't answer it.
""",
input_variables=["gap_analysis"]
)
# =====================================================
# INPUT CARD
# =====================================================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Define Your Goal</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-text">Enter your target role and current skill set</div>', unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        target_role = st.text_input(
            "Target Role",
            placeholder="AI Developer / Data Scientist / ML Engineer"
        )

    with col2:
        skills_input = st.text_input(
            "Current Skills (comma-separated)",
            placeholder="Python, Pandas, NumPy, TensorFlow"
        )

    generate_btn = st.button("🚀 Generate 30-Day Learning Plan", type="primary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# GENERATION LOGIC
# =====================================================
if generate_btn:
    if not target_role.strip() or not skills_input.strip():
        st.error("⚠️ Please provide both target role and skills.")
        st.stop()

    skills = [s.strip() for s in skills_input.split(",") if s.strip()]
    current_inputs = (target_role, tuple(skills))

    if st.session_state.last_inputs != current_inputs:
        with st.spinner("🧠 Analyzing skill gaps & building your roadmap..."):
            chain = prompt_1 | model | parser | prompt_2 | model | parser

            st.session_state.final_result = chain.invoke({
                "target_role": target_role,
                "skills": skills
            })

            st.session_state.last_inputs = current_inputs

# =====================================================
# OUTPUT SECTION
# =====================================================
if st.session_state.final_result:
    st.write("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 Your 30-Day Learning Roadmap</div>', unsafe_allow_html=True)
    st.markdown(st.session_state.final_result)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⬇️ Download Your Plan</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📄 Download as TXT",
            data=st.session_state.final_result,
            file_name="30_day_learning_plan.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.download_button(
            "📝 Download as Markdown",
            data=st.session_state.final_result,
            file_name="30_day_learning_plan.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.write("")
st.markdown(
    "<center class='small-text'>Built with ❤️ using Streamlit & Groq</center>",
    unsafe_allow_html=True
)
