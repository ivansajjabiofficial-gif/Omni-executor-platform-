import streamlit as st
import os
import pandas as pd
from datetime import datetime
from engine import OmniEngine, setup_logger

# Page configuration
st.set_page_config(
    page_title="Omni Executor | Reasoning Engine",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
logger = setup_logger()

def init_session_state():
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "history" not in st.session_state:
        st.session_state.history = []

def main():
    init_session_state()
    
    # Custom CSS for Sleek Interface
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        .main { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #0f172a; color: #94a3b8; }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #ffffff; }

        .stButton>button {
            width: 100%;
            border-radius: 6px;
            height: 44px;
            background-color: #4f46e5;
            color: white;
            font-weight: 700;
            border: none;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.2s ease;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        }
        .stButton>button:hover { background-color: #4338ca; box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3); }

        .report-section {
            padding: 24px;
            border-radius: 12px;
            background-color: white;
            border: 1px solid #e2e8f0;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        }
        
        h1, h2, h3, h4 { font-family: 'Inter', sans-serif; color: #1e293b; letter-spacing: -0.02em; }
        .stTextArea textarea { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; padding-bottom: 24px; border-bottom: 1px solid #1e293b; margin-bottom: 24px;">
                <div style="width: 24px; height: 24px; background-color: #6366f1; border-radius: 4px;"></div>
                <div style="color: white; font-weight: 700; font-size: 1.1rem; letter-spacing: -0.02em;">OMNI EXECUTOR</div>
            </div>
            <p style="color: #64748b; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-top: -20px; margin-bottom: 30px;">
                Reasoning Engine v4.5 (Consolidated)
            </p>
        """, unsafe_allow_html=True)
        
        with st.expander("🔑 API SETTINGS", expanded=False):
            os.environ["GEMINI_API_KEY"] = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
            os.environ["OPENROUTER_API_KEY"] = st.text_input("OpenRouter Key", type="password", value=os.getenv("OPENROUTER_API_KEY", ""))

        st.markdown("<p style='color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;'>Service Tier</p>", unsafe_allow_html=True)
        tier = st.selectbox("Tier", ["Starter", "Pro", "Enterprise"], label_visibility="collapsed")
        
        st.markdown("<p style='color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-top: 20px;'>History</p>", unsafe_allow_html=True)
        if st.session_state.history:
            for i, h in enumerate(st.session_state.history[-5:]):
                st.button(f"Session: {h['timestamp']}", key=f"hist_{i}")
        else:
            st.caption("No previous sessions.")

    # Main Grid
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px;">
            <div>
                <h1 style="margin: 0; font-size: 1.875rem;">🏗️ Omni Executor</h1>
                <p style="color: #64748b; font-size: 0.875rem; margin-top: 4px;">Strategic Reasoning & Business Execution Architecture</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            problem_text = st.text_area("Define the Business Problem", placeholder="Describe the challenge...", height=250)
            uploaded_file = st.file_uploader("Upload Data (CSV/Excel)", type=["csv", "xlsx"])
        with col2:
            scale = st.selectbox("Business Scale", ["Small Business", "Medium Business", "Large Company", "Agency", "Institution", "Enterprise"])
            category = st.selectbox("Category", ["Strategic", "Operational", "Financial", "Compliance", "Growth"])
            industry = st.text_input("Industry", placeholder="e.g. Fintech")

    if st.button("EXECUTE ANALYSIS"):
        if problem_text:
            with st.spinner("Analyzing Architecture..."):
                engine = OmniEngine()
                data_sum = engine.analyze_file(uploaded_file) if uploaded_file else None
                results = engine.generate_analysis(problem_text, scale, category, industry, data_sum)
                st.session_state.analysis_results = results
                st.session_state.history.append({"timestamp": datetime.now().strftime("%H:%M:%S")})
                st.rerun()

    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        st.divider()
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Priority", res.get("Priority Level", "N/A"))
        m2.metric("Confidence", f"{res.get('Confidence', 0)}%")
        m3.metric("Status", "Strategy Optimized")

        # Sections
        sections = [
            "Problem Summary", "Current State", "Likely Root Causes", "Target State", 
            "Recommended Actions", "Quick Wins in 7 Days", "30-Day Plan", 
            "KPIs to Track", "Risks and Cautions", "Automation Opportunities"
        ]
        
        for section in sections:
            if section in res:
                st.markdown(f"""
                    <div class="report-section">
                        <h4 style="margin: 0 0 12px 0; font-size: 0.75rem; text-transform: uppercase; color: #6366f1;">{section}</h4>
                """, unsafe_allow_html=True)
                content = res[section]
                if isinstance(content, list):
                    for item in content: st.markdown(f"- {item}")
                else: st.markdown(content)
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
