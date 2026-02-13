# AI-Personal-Learning-Planner
This is a AI Tool which help you to create planning or Roadmap to reach your desire goal.

🚀 Setup Instructions
1️⃣ Prerequisites

# Make sure you have the following installed:
1) Python 3.9 or higher
2) pip (Python package manager)
3) A valid Groq API key 

# 📦 Dependency Installation
(Optional but Recommended) Create a Virtual Environment 
- Recommended Anaconda

# Run code to create a Virtual Environment 
- conda create -n env python=3.10.10

# Install Required Dependencies 
- pip install -r requirements.txt

# Create a .env file and add your API key:
- GROQ_API_KEY=your_api_key_here

# Run the Application
- streamlit run app.py

# 📤 Output The application generates:

1) User Skill Understanding
2) Skill Gap Analysis
3) Strengths
4) Weak / Missing skills
5) Clear assumptions
6) 30-Day Learning Plan
   
    1)  Daily objectives
    2) 2–4 actionable tasks per day
    3) Suggested learning resources

7) Exportable Learning Plan
.txt
.md

# 🧯 Error Handling & Reliability
- Validates empty or invalid user inputs
- Gracefully handles LLM/API failures
- Prevents UI crashes using safe guards
- Displays user-friendly error messages
- Allows retry without restarting the app
  
# Deployed link of Application
https://ai-personal-learning-planner-34.streamlit.app/

# 🏁 Conclusion
This AI Personal Learning Planner demonstrates how LLMs can be used as reasoning engines, not just text generators — delivering clear, structured, and personalized learning guidance.
