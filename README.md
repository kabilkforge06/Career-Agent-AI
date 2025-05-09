# 🎯 CareerMate AI – AI-Powered Career Mentoring Platform

CareerMate AI is a smart career assistant platform designed for students and alumni. It leverages AI to provide personalized career roadmaps, resume analysis, alumni networking, and profile management — all through a clean and interactive Streamlit interface.

---

## 🚀 Key Features

- ✅ **AI-Powered Career Planning Dashboard**  
  Generate personalized skill roadmaps, certification paths, and interview tips using LLMs like OpenAI or Gemini.

- ✅ **AI Resume Analyzer**  
  Upload your resume in `.txt` format and get smart suggestions on how to improve it.

- ✅ **Alumni Search Module**  
  Search and filter alumni by company, domain, and batch to explore real connections.

- ✅ **Student Profile Management**  
  Students can manage their profile, including name, email, career goal, skills, certifications, projects, and resume.

- ✅ **Role-Based Navigation**  
  Custom experience for `student` and `alumni` users — controlled by login authentication.

- ✅ **Clean UI with Streamlit + Custom CSS**  
  Styled with CSS, responsive layout, and Google Fonts for a professional feel.

---

## 🛠 Tech Stack

| Layer | Tech |
|-------|------|
| 🧠 AI | OpenAI API / Gemini / BitNet / Mistral (via Ollama) |
| 🌐 Frontend + Backend | Python, Streamlit |
| 🗂️ Data Storage | Local JSON files, CSV for alumni |
| 📊 Data Handling | Pandas |
| 🎨 Styling | Custom CSS + Google Fonts |
| 🔐 Auth | Session-based login system (students & alumni) |

---

## 📁 Project Folder Structure
Career-Agent-AI/
├── ai_modules/ # AI interaction helpers (OpenAI, BitNet, etc.)
│ |---llm.helper.py(You can use any LLM)
│ └── 
│ └── resume_prompt.py
│
├── data/ # Data files
│ └── alumni_db.csv # Alumni details
│ └── profiles/ # Saved student profiles (JSON)
│
├── src/ # Core application logic
│ └── Authentication.py # Login logic
│ └── job_dashboard.py # Career roadmap
│ └── resume_analyzer.py # Resume analysis logic
│ └── alumni_search.py # Alumni search logic
│ └── ProfileManagement.py # Student profile edit/save
│
├── style.css # Custom CSS for UI styling
├── streamlit_app.py # 🔥 Main Streamlit app entry point
├── requirements.txt # Python dependencies
└── README.md # This file
---

## ⚙️ How to Run the App Locally

### 1. Clone the Repository

```bash
git clone https://github.com/kabilkforge06/Career-Agent-AI.git
cd Career-Agent-AI
###
2. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Run the Streamlit App
bash
Copy
Edit
streamlit run streamlit_app.py
🧠 Future Enhancements
🔐 Firebase or Supabase authentication & cloud resume storage

🧭 Smart job recommendations based on profile insights

🎓 Alumni mentorship matchmaking system

📊 Admin dashboard to manage student/alumni data

🌐 Multilingual support (Tamil + English)

📸 Screenshots (optional)
(You can add screenshots or demo GIFs here once ready)
Drag .png or .gif into the README or embed like:
![CareerMate Dashboard](images/dashboard_screenshot.png)

👨‍💻 Developed By
Kabilan Murali
2nd Year IT Student
Kongunadu College of Engineering and Technology

📌 GitHub
🔗 LinkedIn

“Empowering every student with AI-driven career clarity.”
— CareerMate AI













