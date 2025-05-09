# src/alumni_dashboard.py

import streamlit as st
import json
import os
from datetime import datetime
from ProfileManagement import load_profile, save_profile

def save_job_opening(job_data):
    """Save job opening data to a local JSON file."""
    jobs_dir = "data/job_openings"
    os.makedirs(jobs_dir, exist_ok=True)
    
    job_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(jobs_dir, f"job_{job_id}.json")
    
    with open(filepath, "w") as f:
        json.dump(job_data, f, indent=4)

def load_job_openings():
    """Load all job openings from the job_openings directory."""
    jobs_dir = "data/job_openings"
    jobs = []
    if os.path.exists(jobs_dir):
        for filename in os.listdir(jobs_dir):
            if filename.endswith(".json"):
                with open(os.path.join(jobs_dir, filename), "r") as f:
                    job = json.load(f)
                    jobs.append(job)
    return jobs

def save_mentor_application(mentor_data):
    """Save mentor application data to a local JSON file."""
    mentors_dir = "data/mentors"
    os.makedirs(mentors_dir, exist_ok=True)
    
    filepath = os.path.join(mentors_dir, f"{mentor_data['username']}.json")
    
    with open(filepath, "w") as f:
        json.dump(mentor_data, f, indent=4)

def show_alumni_dashboard():
    st.title("🎓 Alumni Dashboard")
    
    if "username" not in st.session_state:
        st.error("⚠️ Please log in to access the alumni dashboard")
        return
        
    username = st.session_state["username"]
    profile_data = load_profile(username)
    
    # Welcome Section
    st.markdown(f"### 👋 Welcome back, {profile_data.get('name', username)}!")
    st.markdown("""<div style='margin-bottom: 2rem;'>
        Thank you for being part of our alumni network. Your experience and insights are valuable to our students.
        </div>""", unsafe_allow_html=True)
    
    # Main Options
    tab1, tab2, tab3, tab4 = st.tabs(["📬 Student Requests", "💼 Share Job Opening", "🤝 Become a Mentor", "👤 Update Profile"])
    
    with tab1:
        st.subheader("📬 Student Requests")
        st.info("No pending requests at the moment.")
        
    with tab2:
        st.subheader("💼 Share a Job Opening")
        with st.form("job_form"):
            company = st.text_input("Company Name")
            role = st.text_input("Job Role/Title")
            description = st.text_area("Job Description")
            requirements = st.text_area("Requirements")
            apply_link = st.text_input("Application Link")
            
            submitted = st.form_submit_button("📤 Post Job Opening")
            
            if submitted:
                if company and role and description:
                    job_data = {
                        "company": company,
                        "role": role,
                        "description": description,
                        "requirements": requirements,
                        "apply_link": apply_link,
                        "posted_by": username,
                        "posted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_job_opening(job_data)
                    st.success("✅ Job opening posted successfully!")
                else:
                    st.error("⚠️ Please fill in all required fields")
        
        st.divider()
        st.subheader("📋 Recent Job Postings")
        for job in load_job_openings():
            with st.expander(f"{job['role']} at {job['company']}"):
                st.markdown(f"**Description:** {job['description']}")
                st.markdown(f"**Requirements:** {job['requirements']}")
                if job['apply_link']:
                    st.markdown(f"[Apply Here]({job['apply_link']})")
                st.caption(f"Posted by {job['posted_by']} on {job['posted_date']}")
    
    with tab3:
        st.subheader("🤝 Become a Mentor")
        if not profile_data:
            st.warning("⚠️ Please complete your profile before applying as a mentor")
        else:
            with st.form("mentor_form"):
                expertise = st.text_area("Areas of Expertise")
                availability = st.selectbox("Availability per week", 
                    ["1-2 hours", "3-4 hours", "5+ hours"])
                motivation = st.text_area("Why do you want to be a mentor?")
                
                submitted = st.form_submit_button("🤝 Apply as Mentor")
                
                if submitted:
                    if expertise and motivation:
                        mentor_data = {
                            "username": username,
                            "name": profile_data['name'],
                            "expertise": expertise,
                            "availability": availability,
                            "motivation": motivation,
                            "application_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        save_mentor_application(mentor_data)
                        st.success("✅ Mentor application submitted successfully!")
                    else:
                        st.error("⚠️ Please fill in all required fields")
    
    with tab4:
        st.subheader("👤 Update Your Profile")
        if profile_data:
            st.markdown(f"**Current Profile:**")
            st.markdown(f"**Name:** {profile_data['name']}")
            st.markdown(f"**Email:** {profile_data['email']}")
            st.markdown(f"**Career Goal:** {profile_data['career_goal']}")
            st.markdown(f"**Skills:** {', '.join(profile_data['skills'])}")
            st.markdown(f"**Certifications:** {', '.join(profile_data['certifications'])}")
            st.markdown(f"**Projects:** {profile_data['projects']}")
            
            if st.button("✏️ Edit Profile"):
                st.session_state["show_profile_edit"] = True
        else:
            st.info("📝 Please create your profile to get started.")