import streamlit as st
import google.generativeai as genai
from pytrends.request import TrendReq
from serpapi import GoogleSearch
import pandas as pd
import matplotlib.pyplot as plt
import json
from fpdf import FPDF
import base64

# Page Config
st.set_page_config(page_title="Market Validation Engine V2.0", layout="wide", page_icon="rocket")

# -----------------------------------------------------------------------------
# 1. Styling & Visual Overhaul
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Settings */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        background-color: #F8F9FA;
        font-family: 'Inter', sans-serif;
        color: #1D1D1F;
    }
    .card {
        color: #1D1D1F;


    /* Headlines */
    h1, h2, h3 {
        color: #1E293B;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.8rem; margin-top: 1.5rem; margin-bottom: 1rem; }
    h3 { font-size: 1.3rem; margin-bottom: 0.5rem; }

    /* Cards */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #0F172A;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #334155;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:active {
        transform: scale(0.98);
    }

    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        padding: 10px 12px;
    }

    /* Alerts */
    .stAlert {
        border-radius: 8px;
        border: 1px solid transparent;
    }
    
    /* Utility */
    hr { border-color: #E2E8F0; margin: 2rem 0; }
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Smart Sidebar & Authentication
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Configuration")
    
    # Smart Auth Logic
    if 'GEMINI_API_KEY' in st.secrets:
        gemini_key = st.secrets['GEMINI_API_KEY']
    else:
        gemini_key = st.text_input("Gemini API Key", type="password")

    if 'SERPAPI_KEY' in st.secrets:
        serpapi_key = st.secrets['SERPAPI_KEY']
    else:
        serpapi_key = st.text_input("SerpApi Key", type="password")
    
    # Auth Status Indicator
    if 'GEMINI_API_KEY' in st.secrets and 'SERPAPI_KEY' in st.secrets:
        st.success("✅ API Keys Loaded from Secrets")

    if gemini_key:
        genai.configure(api_key=gemini_key)
        
    # Model Selection Logic
    # Hardcoded to stable production model as per requirements
    selected_model_name = "gemini-3-flash-preview"
    
    st.caption(f"🤖 Using AI Model: {selected_model_name}")

    if st.button("Reset App", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
@st.cache_data
def get_trends(keyword):
    try:
        pt = TrendReq(hl='en-US', tz=360)
        pt.build_payload([keyword], cat=0, timeframe='today 12-m')
        data = pt.interest_over_time()
        return data
    except Exception:
        return pd.DataFrame()

def clean_text(text):
    """
    Cleans text to be compatible with latin-1 encoding for FPDF.
    Replaces common smart quotes/dashes and handles other unicode characters.
    """
    if not isinstance(text, str):
        return str(text)
        
    replacements = {
        '\u2013': '-', '\u2014': '--',
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2026': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Final safety net: replace any remaining non-latin characters
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_list(prompt_text):
    try:
        model = genai.GenerativeModel(selected_model_name)
        response = model.generate_content(prompt_text)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
        return json.loads(text)
    except Exception as e:
        st.error(f"Generation Error: {e}")
        return []

def create_pdf(niche, pain_points, opportunity, moat, prompt):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=clean_text(f"Market Validation Report: {niche}"), ln=1, align='C')
    pdf.ln(10)
    
    # Pain Points
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Top Pain Points", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(pain_points))
    pdf.ln(5)
    
    # Business Idea
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Validated Business Idea", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(opportunity))
    pdf.ln(5)

    # Moat
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Defensible Moat", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=clean_text(moat))
    pdf.ln(5)
    
    # Prompt
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Lovable Landing Page Prompt", ln=1)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, txt=clean_text(prompt))
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# -----------------------------------------------------------------------------
# Main Interface
# -----------------------------------------------------------------------------
st.title("Market Validation Engine V2.0")
st.markdown("---")

# Session Initialization
if 'niches' not in st.session_state: st.session_state.niches = []
if 'selected_niche' not in st.session_state: st.session_state.selected_niche = None
if 'niches_l1' not in st.session_state: st.session_state.niches_l1 = []
if 'niches_l2' not in st.session_state: st.session_state.niches_l2 = []
if 'selected_l1' not in st.session_state: st.session_state.selected_l1 = None
if 'phase1_state' not in st.session_state: st.session_state.phase1_state = 'input'

# -----------------------------------------------------------------------------
# Phase 1: Market Expansion
# -----------------------------------------------------------------------------
st.write('<div class="card">', unsafe_allow_html=True)
st.subheader("Phase 1: Market Expansion")

if st.session_state.phase1_state == 'input':
    core_market = st.text_input("Enter Core Market (e.g., 'Wealth', 'Fitness')", "Wealth")
    if st.button("Analyze Market Structure"):
        if not gemini_key:
            st.error("Please configure API Keys.")
        else:
            with st.spinner("Consulting Gemini..."):
                try:
                    prompt = f"Act as a market expert. Break '{core_market}' into 5 distinct high-level categories. Return ONLY a raw JSON array of strings."
                    result = generate_list(prompt)
                    if result:
                         st.session_state.niches_l1 = result
                         st.session_state.phase1_state = 'level1'
                         st.rerun()
                    else:
                         st.error("AI returned empty list. Please try again.")
                except Exception as e:
                    st.error(f"AI Error: {e}")

elif st.session_state.phase1_state == 'level1':
    st.write("### Step 2: Select a Category")
    
    # UI Safety Check
    if not st.session_state.get('niches_l1'):
         st.warning("No categories found. Please try analyzing the market again.")
         if st.button("Back to Start"):
             st.session_state.phase1_state = 'input'
             st.rerun()
    else:
        selected_cat = st.radio("High-Level Categories:", st.session_state.niches_l1)
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Drill Down"):
                with st.spinner(f"Exploring {selected_cat}..."):
                    try:
                        prompt = f"Generate 5 specific, profitable sub-niches for: '{selected_cat}'. Return ONLY a raw JSON array of strings."
                        result = generate_list(prompt)
                        if result:
                            st.session_state.niches_l2 = result
                            st.session_state.selected_l1 = selected_cat
                            st.session_state.phase1_state = 'level2'
                            st.rerun()
                        else:
                             st.error("AI returned empty sub-niche list.")
                    except Exception as e:
                         st.error(f"AI Error: {e}")
        with col2:
            if st.button("Reset Phase"):
                st.session_state.phase1_state = 'input'
                st.rerun()

elif st.session_state.phase1_state == 'level2':
    st.write(f"### Step 3: Select Sub-Niche in '{st.session_state.selected_l1}'")
    if st.session_state.niches_l2:
        selected_sub = st.radio("Profitable Sub-Niches:", st.session_state.niches_l2)
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Lock In Niche"):
                st.session_state.selected_niche = selected_sub
                st.session_state.phase1_state = 'done'
                st.rerun()
        with col2:
            if st.button("Back"):
                st.session_state.phase1_state = 'level1'
                st.rerun()

elif st.session_state.phase1_state == 'done':
    st.success(f"Final Selection: **{st.session_state.selected_niche}**")
    if st.button("Start Over"):
        st.session_state.phase1_state = 'input'
        st.session_state.selected_niche = None
        st.session_state.phase2_complete = False
        st.session_state.phase3_complete = False
        st.session_state.analysis_complete = False
        st.session_state.snippets = []
        st.rerun()

st.write('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Phase 2: Validation
# -----------------------------------------------------------------------------
if st.session_state.selected_niche:
    st.write('<div class="card">', unsafe_allow_html=True)
    st.subheader("Phase 2: Trend Validation")
    
    if st.button("Run Trend Analysis"):
        st.session_state.show_trends = True

    if st.session_state.get('show_trends'):
        with st.spinner("Fetching Google Trends data..."):
            df = get_trends(st.session_state.selected_niche)
            
        if not df.empty and st.session_state.selected_niche in df.columns:
            st.line_chart(df[st.session_state.selected_niche])
            st.success("Data successfully retrieved.")
            if st.button("Proceed to Data Mining", key="proceed_phase2"):
                st.session_state.phase2_complete = True
        else:
             st.warning("⚠️ Google Trends data unavailable (Rate Limit). Skipping to next phase automatically.")
             st.session_state.phase2_complete = True
    
    st.write('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Phase 3: Data Gathering (Reddit)
# -----------------------------------------------------------------------------
if st.session_state.get('phase2_complete'):
    st.write('<div class="card">', unsafe_allow_html=True)
    st.subheader("Phase 3: Insight Mining")
    
    if st.button("Mine Reddit for Pain Points"):
        if not serpapi_key:
            st.error("SerpApi Key required.")
        else:
            query = f"{st.session_state.selected_niche} site:reddit.com inurl:comments (struggle OR hate OR nightmare)"
            st.info(f"Searching: `{query}`")
            
            progress_bar = st.progress(0)
            try:
                search = GoogleSearch({
                    "q": query,
                    "api_key": serpapi_key,
                    "num": 10
                })
                results = search.get_dict()
                progress_bar.progress(50)
                
                snippets = []
                # Robust extraction
                sources = [results.get('organic_results', []), 
                           results.get('discussions_and_forums', []), 
                           results.get('related_questions', [])]
                
                for source in sources:
                    for item in source:
                        if 'snippet' in item: snippets.append(item['snippet'])
                        elif 'title' in item: snippets.append(item['title'])
                
                st.session_state.snippets = snippets
                progress_bar.progress(100)
                
                if snippets:
                    st.success(f"Found {len(snippets)} insights.")
                    with st.expander("View Raw Data"):
                        for s in snippets: st.write(f"- {s}")
                    st.session_state.phase3_complete = True
                else:
                    st.warning("No relevant snippets found. Try a different niche.")
                    
            except Exception as e:
                st.error(f"Search failed: {e}")
    st.write('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Phase 4: Processing & Competitor Loop
# -----------------------------------------------------------------------------
if st.session_state.get('phase3_complete'):
    st.write('<div class="card">', unsafe_allow_html=True)
    st.subheader("Phase 4: Intelligent Analysis")
    
    if st.button("Analyze & Build Strategy"):
        if not gemini_key:
             st.error("Gemini API Key required.")
        else:
            with st.spinner("Generating Core Analysis..."):
                try:
                    model = genai.GenerativeModel(selected_model_name)
                    snippets_text = "\n".join(st.session_state.snippets)
                    
                    # 1. Pain Points
                    pain_prompt = f"Analyze these snippets about '{st.session_state.selected_niche}':\n{snippets_text}\nExtract 3 distinct, visceral pain points."
                    pain_response = model.generate_content(pain_prompt)
                    pain_points = pain_response.text
                    
                    # 2. Initial Opportunity
                    opp_prompt = f"Based on these pain points:\n{pain_points}\nGenerate 1 singular, high-potential business opportunity (SaaS, Info Product, or Service)."
                    opp_response = model.generate_content(opp_prompt)
                    opportunity = opp_response.text
                    
                    st.session_state.temp_analysis = {
                        "pain_points": pain_points,
                        "opportunity": opportunity
                    }
                    st.session_state.analysis_step_1 = True

                except Exception as e:
                    st.error(f"Analysis Failed: {e}")

    # Competitor Loop
    if st.session_state.get('analysis_step_1'):
        st.info("Searching for Competitors to validate 'Moat'...")
        with st.spinner("Checking Competitors..."):
            try:
                # Search Competitors
                opp_summary = st.session_state.temp_analysis['opportunity'][:100] # truncate for query
                comp_query = f"{opp_summary} competitors alternative"
                search = GoogleSearch({"q": comp_query, "api_key": serpapi_key, "num": 5})
                res = search.get_dict()
                
                competitors = []
                if 'organic_results' in res:
                    for item in res['organic_results']:
                        competitors.append(f"{item.get('title')}: {item.get('snippet')}")
                
                comp_text = "\n".join(competitors)
                
                # Refine with Moat
                refine_prompt = f"""
                I have this business idea: {st.session_state.temp_analysis['opportunity']}
                
                I found these potential competitors:
                {comp_text}
                
                Refine the business idea to have a specific 'Moat' or competitive advantage that solves the pain points better than the competitors.
                Explain WHY it wins.
                """
                
                model = genai.GenerativeModel(selected_model_name)
                moat_response = model.generate_content(refine_prompt)
                moat_analysis = moat_response.text
                
                # Lovable Prompt
                love_prompt = f"Create a 'Before-After-Bridge' copywriting prompt for a landing page for this refined idea:\n{moat_analysis}"
                love_response = model.generate_content(love_prompt)
                final_prompt = love_response.text
                
                st.session_state.final_results = {
                    "pain_points": st.session_state.temp_analysis['pain_points'],
                    "opportunity": st.session_state.temp_analysis['opportunity'],
                    "moat": moat_analysis,
                    "prompt": final_prompt
                }
                st.session_state.analysis_complete = True
                
            except Exception as e:
                st.error(f"Competitor Loop Failed: {e}")

    # Display Results
    if st.session_state.get('analysis_complete'):
        res = st.session_state.final_results
        
        st.markdown("### 1. Market Pain")
        st.success(res['pain_points'])
        
        st.markdown("### 2. The Opportunity")
        st.info(res['opportunity'])
        
        st.markdown("### 3. The Moat (Competitor-Proofing)")
        st.warning(res['moat'])
        
        st.markdown("### 4. Landing Page Prompt")
        st.code(res['prompt'], language="text")

        st.success("Analysis Complete. Download your Executive Report below.")

        # PDF Download
        pdf_bytes = create_pdf(
            st.session_state.selected_niche,
            res['pain_points'],
            res['opportunity'],
            res['moat'],
            res['prompt']
        )
        
        st.download_button(
            label="📄 Download Executive Report",
            data=pdf_bytes,
            file_name=f"{st.session_state.selected_niche}_Report.pdf",
            mime='application/pdf'
        )

    st.write('</div>', unsafe_allow_html=True)
