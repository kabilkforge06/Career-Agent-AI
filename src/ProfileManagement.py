# src/ProfileManagement.py

import streamlit as st
import json
import os

def save_profile(username, profile_data):
    """Save profile data into a local JSON file."""
    profiles_dir = "data/profiles"
    os.makedirs(profiles_dir, exist_ok=True)
    filepath = os.path.join(profiles_dir, f"{username}.json")

    with open(filepath, "w") as f:
        json.dump(profile_data, f, indent=4)

def load_profile(username):
    """Load profile data from a local JSON file if exists."""
    filepath = f"data/profiles/{username}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    else:
        return None

def load_all_profiles():
    """Load all profile data from the profiles directory."""
    profiles_dir = "data/profiles"
    profiles = []
    if os.path.exists(profiles_dir):
        for filename in os.listdir(profiles_dir):
            if filename.endswith(".json"):
                username = filename[:-5]  # Remove .json extension
                profile = load_profile(username)
                if profile:
                    profile["username"] = username
                    profiles.append(profile)
    return profiles

def show_profile_page():
    st.title("👤 Profile Management")
    
    if "username" not in st.session_state:
        st.error("⚠️ Please log in to access your profile")
        return
        
    username = st.session_state["username"]
    profile_data = load_profile(username)
    
    tab1, tab2 = st.tabs(["My Profile", "All Users"])

    with tab1:
        with st.form("profile_form"):
            st.subheader("📝 Edit Your Profile")

            name = st.text_input("Full Name", value=profile_data.get("name") if profile_data else "")
            email = st.text_input("Email Address", value=profile_data.get("email") if profile_data else "")
            career_goal = st.text_input("Career Goal", value=profile_data.get("career_goal") if profile_data else "")
            skills = st.text_input("Skills (comma-separated)", value=",".join(profile_data.get("skills", [])) if profile_data else "")
            certifications = st.text_input("Certifications (comma-separated)", value=",".join(profile_data.get("certifications", [])) if profile_data else "")
            projects = st.text_area("Projects", value=profile_data.get("projects") if profile_data else "", height=100)

            uploaded_resume = st.file_uploader("Upload Resume (optional)", type=["pdf"])

            submitted = st.form_submit_button("💾 Save Profile")

            if submitted:
                new_profile = {
                    "name": name,
                    "email": email,
                    "career_goal": career_goal,
                    "skills": [s.strip() for s in skills.split(",") if s.strip()],
                    "certifications": [c.strip() for c in certifications.split(",") if c.strip()],
                    "projects": projects,
                }

                if uploaded_resume:
                    resume_path = f"data/profiles/{username}_resume.pdf"
                    with open(resume_path, "wb") as f:
                        f.write(uploaded_resume.getbuffer())
                    new_profile["resume_path"] = resume_path

                save_profile(username, new_profile)
                st.success("✅ Profile saved successfully!")
                st.rerun()

        if profile_data:
            st.divider()
            st.subheader("📄 Your Saved Profile")
            st.markdown(f"**Name:** {profile_data['name']}")
            st.markdown(f"**Email:** {profile_data['email']}")
            st.markdown(f"**Career Goal:** {profile_data['career_goal']}")
            st.markdown(f"**Skills:** {', '.join(profile_data['skills'])}")
            st.markdown(f"**Certifications:** {', '.join(profile_data['certifications'])}")
            st.markdown(f"**Projects:** {profile_data['projects']}")
            if profile_data.get("resume_path"):
                st.markdown(f"[Download Resume 📄]({profile_data['resume_path']})", unsafe_allow_html=True)
        else:
            st.info("📝 Create your profile by filling out the form above.")
            
    with tab2:
        st.subheader("👥 All Users")
        all_profiles = load_all_profiles()
        
        if not all_profiles:
            st.info("No user profiles found.")
        else:
            cols = st.columns(3)
            for idx, profile in enumerate(all_profiles):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"### {profile['name']}")
                        st.caption(f"@{profile['username']}")
                        st.markdown(f"**Career Goal:** {profile.get('career_goal', 'Not specified')}")
                        st.markdown(f"**Skills:** {', '.join(profile.get('skills', []))}")
                        if profile.get('resume_path'):
                            st.markdown(f"[View Resume 📄]({profile['resume_path']})")
                        st.divider()
