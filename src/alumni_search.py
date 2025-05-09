# src/alumni_search.py

import pandas as pd
import streamlit as st

def load_alumni_data(path="data/alumni_db.csv"):
    """
    Load alumni data from a local CSV file.
    
    Args:
        path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Alumni data as a DataFrame.
    """
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        raise Exception(f"Alumni database not found at {path}")
    except Exception as e:
        raise Exception(f"Error loading alumni data: {str(e)}")

def search_alumni(df, company=None, role=None, batch=None):
    """
    Search alumni based on company, role, and batch year.
    
    Args:
        df (pd.DataFrame): The alumni DataFrame.
        company (str): Company to search for.
        role (str): Role/domain to search for.
        batch (int/str): Batch year to search for.
    
    Returns:
        pd.DataFrame: Filtered alumni data.
    """
    if company:
        df = df[df['current_company'].str.contains(company, case=False, na=False)]
    if role:
        df = df[df['domain'].str.contains(role, case=False, na=False)]
    if batch:
        df = df[df['batch'] == int(batch)]
    return df

def show_alumni_search():
    st.title("🔍 Alumni Search")
    st.markdown("""<div style='margin-bottom: 2rem;'>
        Connect with our alumni network and explore their career journeys.
        </div>""", unsafe_allow_html=True)
    
    # Load alumni data
    try:
        df = load_alumni_data()
    except Exception as e:
        st.error(f"⚠️ {str(e)}")
        return
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    with col1:
        company = st.text_input("🏢 Company")
    with col2:
        role = st.text_input("💼 Role/Domain")
    with col3:
        batch = st.selectbox("🎓 Batch Year", options=[None] + sorted(df['batch'].unique().tolist()))
    
    # Search results
    filtered_df = search_alumni(df, company, role, batch)
    
    if len(filtered_df) == 0:
        st.info("No alumni found matching your search criteria.")
    else:
        st.markdown(f"### Found {len(filtered_df)} Alumni")
        
        # Display alumni cards in a grid
        cols = st.columns(3)
        for idx, row in filtered_df.iterrows():
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style='padding: 1rem; background: var(--card-bg); border-radius: var(--border-radius); 
                             border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 1rem;'>
                        <h3 style='margin: 0; color: var(--primary-color);'>{row['name']}</h3>
                        <p style='color: var(--text-color); opacity: 0.8; margin: 0.5rem 0;'>
                            🏢 {row['current_company']}<br>
                            💼 {row['domain']}<br>
                            🎓 Batch {row['batch']}
                        </p>
                        {f'<a href="{row["linkedin"]}" target="_blank" style="color: var(--primary-color);">🔗 LinkedIn Profile</a>' if pd.notna(row.get('linkedin')) else ''}
                    </div>
                    """, unsafe_allow_html=True)
