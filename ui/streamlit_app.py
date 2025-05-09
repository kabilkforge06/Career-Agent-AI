import sys
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = str(current_dir.parent)
sys.path.append(parent_dir)

import streamlit as st
from src.Authentication import show_login
from src.job_dashboard import generate_agentic_roadmap
from src.alumni_search import load_alumni_data, search_alumni
from src.resume_analyzer import analyze_resume
from src.ProfileManagement import show_profile_page   # ✅ Import your Profile Page

# Page configuration
st.set_page_config(
    page_title="CareerMate AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open(Path(__file__).parent / 'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom fonts
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Login/Logout Logic
if not st.session_state["logged_in"]:
    show_login()
else:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"""<h1 style='margin-bottom: 0.5rem;'>👋 Welcome, {st.session_state['username']}!</h1>""", unsafe_allow_html=True)
        st.markdown("<div style='height: 2px; background: var(--primary-color); margin: 1rem 0;'></div>", unsafe_allow_html=True)
        
        role = st.session_state["role"]
        
        if role == "student":
            selected_page = st.selectbox(
                "Navigation",
                ["🎯 Job Dashboard", "📄 Resume Analyzer", "🔍 Alumni Search", "👤 My Profile"],
                format_func=lambda x: x.split()[-1]
            )
        else:
            selected_page = "🎓 Alumni Dashboard"

    # Main Content Area
    if role == "student":
        if "🎯 Job Dashboard" in selected_page:
            st.markdown("<div class='main-content'>", unsafe_allow_html=True)
            st.markdown("<h1 class='main-header'>🎯 Career Planning Dashboard</h1>", unsafe_allow_html=True)
            st.markdown("<h3 class='sub-header'>Let AI help plan your career path</h3>", unsafe_allow_html=True)
            st.markdown("""
                <div class='section-intro'>
                    <p>Welcome to your personalized career planning assistant! Input your career goals and preferences below, 
                    and let our AI create a customized roadmap for your success.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            with st.form("career_form", clear_on_submit=False):
                col1, col2 = st.columns(2)
                with col1:
                    goal = st.text_input("Career Goal", placeholder="e.g., Data Scientist, Full Stack Developer")
                with col2:
                    companies = st.text_input("Target Companies", placeholder="e.g., Google, Microsoft, Amazon")
                submitted = st.form_submit_button("🚀 Generate Career Roadmap")

            if submitted:
                if not goal:
                    st.error("Please enter a career goal!")
                else:
                    with st.status("🤖 AI is creating your roadmap...", expanded=True) as status:
                        try:
                            roadmap = generate_agentic_roadmap(goal, companies)
                            status.update(label="✅ Roadmap generated!", state="complete")
                            st.markdown(roadmap)
                        except Exception as e:
                            st.error(f"Error generating roadmap: {str(e)}")

        elif "📄 Resume Analyzer" in selected_page:
            st.markdown("<div class='main-content'>", unsafe_allow_html=True)
            st.markdown("<h1 class='main-header'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
            st.markdown("<h3 class='sub-header'>Get instant feedback on your resume</h3>", unsafe_allow_html=True)
            st.markdown("""
                <div class='section-intro'>
                    <p>Upload your resume and receive AI-powered insights on how to improve it. 
                    Our system will analyze your content and provide actionable recommendations.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Upload your resume (TXT format)",
                type=["txt"],
                help="Please ensure your resume is in text format"
            )

            if uploaded_file:
                with st.expander("📝 Resume Preview", expanded=False):
                    resume_text = uploaded_file.read().decode("utf-8")
                    st.text_area("Content", resume_text, height=200)

                if st.button("🔍 Analyze Resume", use_container_width=True):
                    with st.status("🤖 Analyzing your resume...", expanded=True) as status:
                        try:
                            suggestions = analyze_resume(resume_text)
                            status.update(label="✅ Analysis complete!", state="complete")
                            st.markdown(suggestions)
                        except Exception as e:
                            st.error(f"Error analyzing resume: {str(e)}")

        elif "🔍 Alumni Search" in selected_page:
            st.markdown("<div class='main-content'>", unsafe_allow_html=True)
            st.markdown("<h1 class='main-header'>🔍 Alumni Network</h1>", unsafe_allow_html=True)
            st.markdown("<h3 class='sub-header'>Connect with alumni from your college</h3>", unsafe_allow_html=True)
            st.markdown("""
                <div class='section-intro'>
                    <p>Discover and connect with alumni who've walked the path before you. 
                    Filter by company, role, or graduation year to find relevant connections.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            try:
                df = load_alumni_data()
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    company = st.text_input("🏢 Company")
                with col2:
                    role_input = st.text_input("💼 Role/Domain")
                with col3:
                    batch = st.selectbox(
                        "📅 Batch",
                        options=["All"] + sorted(df['batch'].astype(str).unique())
                    )

                if st.button("🔍 Search", use_container_width=True):
                    results = search_alumni(
                        df, company, role_input,
                        None if batch == "All" else int(batch)
                    )
                    if len(results) > 0:
                        st.success(f"Found {len(results)} alumni!")
                        st.dataframe(
                            results,
                            use_container_width=True,
                            column_config={
                                "name": "Alumni Name",
                                "company": "Company",
                                "role": "Current Role",
                                "batch": "Graduation Year"
                            }
                        )
                    else:
                        st.warning("No alumni found matching your criteria.")
            except Exception as e:
                st.error(f"Error loading alumni data: {str(e)}")

        elif "👤 My Profile" in selected_page:
            show_profile_page()   # ✅ Your new Student Profile page!

    else:  # Alumni role
        st.header("🎓 Alumni Dashboard")
        st.subheader("Welcome to the Alumni Portal! 🌟")
        st.info("""
        **Coming Soon:**
        - Student Profile Search
        - Project Showcase
        - Mentorship Programs
        - Interview Experience Sharing
        """)

