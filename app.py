import streamlit as st
import google.generativeai as genai
from pytrends.request import TrendReq
from serpapi import GoogleSearch
import pandas as pd
import matplotlib.pyplot as plt
import json


@st.cache_data
def get_trends(keyword):
    try:
        pt = TrendReq(hl='en-US', tz=360)
        pt.build_payload([keyword], cat=0, timeframe='today 12-m')
        data = pt.interest_over_time()
        return data
    except Exception as e:
        # Pytrends is liable to fail with 429s, validation should be graceful
        return pd.DataFrame() # Return empty to signal failure/skip


# Page Config
st.set_page_config(page_title="Market Validation Engine", layout="wide")

# Styling - Apple Clean
st.markdown("""
<style>
    .stApp {
        background-color: #FAFAFA;
        color: #1D1D1F;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .stButton>button {
        background-color: #0071E3;
        color: white;
        border-radius: 980px;
        border: none;
        padding: 10px 24px;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #0077ED;
        transform: scale(1.02);
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 1px solid #D2D2D7;
        padding: 8px 12px;
    }
    h1 {
        font-weight: 600;
        letter-spacing: -0.003em;
        font-size: 40px;
    }
    h2 {
        font-weight: 600;
        letter-spacing: -0.003em;
        font-size: 28px;
        margin-top: 30px;
    }
    h3 {
        font-weight: 600;
        font-size: 20px;
    }
    .css-1d391kg {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    if st.button("Reset App", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    
    # Try to get keys from secrets first
    if 'GEMINI_API_KEY' in st.secrets:
        gemini_key = st.secrets['GEMINI_API_KEY']
    else:
        gemini_key = st.text_input("Gemini API Key", type="password")

    if 'SERPAPI_KEY' in st.secrets:
        serpapi_key = st.secrets['SERPAPI_KEY']
    else:
        serpapi_key = st.text_input("SerpApi Key", type="password")

    if gemini_key:
        genai.configure(api_key=gemini_key)

# Main Interface
st.title("Market Validation Engine")
st.markdown("---")

# Session State
if 'niches' not in st.session_state:
    st.session_state.niches = []
if 'selected_niche' not in st.session_state:
    st.session_state.selected_niche = None



# Session State Initialization
if 'niches_l1' not in st.session_state:
    st.session_state.niches_l1 = []
if 'niches_l2' not in st.session_state:
    st.session_state.niches_l2 = []
if 'selected_l1' not in st.session_state:
    st.session_state.selected_l1 = None
if 'selected_niche' not in st.session_state:
    st.session_state.selected_niche = None
if 'phase1_state' not in st.session_state:
    st.session_state.phase1_state = 'input' # input, level1, level2, done

# Phase 1: Market Expansion (Drill-Down)
st.subheader("Phase 1: Market Expansion")

# Helper to Generate
def generate_list(prompt_text):
    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
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

# Step 1: Core Market
if st.session_state.phase1_state == 'input':
    core_market = st.text_input("Core Market", "Wealth")
    if st.button("Analyze Market"):
        if not gemini_key:
            st.error("Please enter Gemini API Key")
        else:
            with st.spinner("Analyzing Market Structure..."):
                prompt = f"""
                Act as a market research expert. Break down the market '{core_market}' into 5 distinct, high-level categories.
                Return ONLY a raw JSON array of strings.
                Example: ["Real Estate", "Crypto", "Stock Market", "Personal Finance", "Business"]
                """
                st.session_state.niches_l1 = generate_list(prompt)
                st.session_state.phase1_state = 'level1'
                st.rerun()

# Step 2: Level 1 Categories
elif st.session_state.phase1_state == 'level1':
    st.write("### Step 2: Select a Category")
    if st.session_state.niches_l1:
        selected_cat = st.radio("High-Level Categories:", st.session_state.niches_l1)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Explore This Category"):
                with st.spinner(f"Drilling down into {selected_cat}..."):
                    prompt = f"""
                    Generate 5 specific, profitable sub-niches for the category: '{selected_cat}'.
                    Return ONLY a raw JSON array of strings.
                    Example: ["Flipping Houses", "Rental Arbitrage", ...]
                    """
                    st.session_state.niches_l2 = generate_list(prompt)
                    st.session_state.selected_l1 = selected_cat
                    st.session_state.phase1_state = 'level2'
                    st.rerun()
        with col2:
             if st.button("Reset"):
                 st.session_state.phase1_state = 'input'
                 st.rerun()

# Step 3: Level 2 Sub-Niches
elif st.session_state.phase1_state == 'level2':
    st.write(f"### Step 3: Select a Sub-Niche in '{st.session_state.selected_l1}'")
    if st.session_state.niches_l2:
        selected_sub = st.radio("Profitable Sub-Niches:", st.session_state.niches_l2)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Lock In This Niche"):
                st.session_state.selected_niche = selected_sub
                st.session_state.phase1_state = 'done'
                st.rerun()
        with col2:
             if st.button("Back"):
                 st.session_state.phase1_state = 'level1'
                 st.rerun()

# Done State
elif st.session_state.phase1_state == 'done':
    st.success(f"Final Selection: **{st.session_state.selected_niche}**")
    if st.button("Start Over"):
        st.session_state.phase1_state = 'input'
        st.session_state.selected_niche = None
        st.session_state.phase2_complete = False
        st.session_state.phase3_complete = False
        st.session_state.snippets = []
        st.rerun()

# Phase 2: Validation
if st.session_state.selected_niche:
    st.markdown("---")
    st.subheader("Phase 2: Validation")
    
    if st.button("Check Trends"):
        st.session_state.show_trends = True

    if st.session_state.get('show_trends'):
        with st.spinner("Fetching trends..."):
            df = get_trends(st.session_state.selected_niche)
            
        if not df.empty and st.session_state.selected_niche in df.columns:
            st.line_chart(df[st.session_state.selected_niche])
            st.markdown("### Is this trending up or down?")
            
            if st.button("Proceed", key="proceed_phase2"):
                st.session_state.phase2_complete = True
        else:
             st.warning("⚠️ Google Trends data unavailable (Google rate limit). Skipping to Reddit analysis...")
             st.session_state.phase2_complete = True
             st.rerun()

# Phase 3: Data Gathering
if st.session_state.get('phase2_complete'):
    st.markdown("---")
    st.subheader("Phase 3: Data Gathering")
    
    if st.button("Mine Reddit"):
        if not serpapi_key:
            st.error("Please provide a SerpApi Key in the sidebar.")
        else:
            query = f"{st.session_state.selected_niche} site:reddit.com inurl:comments (struggle OR hate OR nightmare)"
            st.write(f"Searching: `{query}`")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("Connecting to SerpApi...")
            try:
                search = GoogleSearch({
                    "q": query,
                    "api_key": serpapi_key,
                    "num": 10
                })
                results = search.get_dict()
                progress_bar.progress(50)
                status_text.text("Extracting snippets...")
                
                snippets = []
                # Combine multiple sources for robustness
                organic = results.get('organic_results', [])
                discussions = results.get('discussions_and_forums', [])
                questions = results.get('related_questions', [])
                
                all_results = organic + discussions + questions
                
                for result in all_results:
                    if 'snippet' in result:
                        snippets.append(result['snippet'])
                    elif 'title' in result: # Fallback to title if snippet missing
                        snippets.append(result['title'])
                
                st.session_state.snippets = snippets
                progress_bar.progress(100)
                status_text.text("Done!")
                
                if snippets:
                    st.success(f"Found {len(snippets)} insights.")
                    with st.expander("View Raw Snippets"):
                        for s in snippets:
                            st.write(f"- {s}")
                    st.session_state.phase3_complete = True
                else:
                    st.warning("No relevant snippets found.")
            except Exception as e:
                st.error(f"Search error: {e}")

# Phase 4: Processing
if st.session_state.get('phase3_complete'):
    st.markdown("---")
    st.subheader("Phase 4: Processing")
    
    if st.button("Analyze & Build"):
        if not gemini_key:
             st.error("Gemini API Key required.")
        else:
            with st.spinner("Running Gemini Analysis Chain..."):
                try:
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                    snippets_text = "\n".join(st.session_state.snippets)
                    
                    # Step 1: Pain Extractor
                    pain_prompt = f"""
                    Analyze these Reddit snippets about '{st.session_state.selected_niche}':
                    {snippets_text}
                    
                    Extract 3-5 specific, visceral pain points and direct user quotes.
                    """
                    pain_response = model.generate_content(pain_prompt)
                    pain_points = pain_response.text
                    
                    # Step 2: Gap Generator
                    gap_prompt = f"""
                    Based on these pain points:
                    {pain_points}
                    
                    Generate 3 distinct business opportunities:
                    1. New Paradigm (A completely different way of solving it)
                    2. Differentiation (Better features/UX)
                    3. Tech Angle (AI/Automation solution)
                    """
                    gap_response = model.generate_content(gap_prompt)
                    opportunities = gap_response.text
                    
                    # Step 3: Lovable Prompt
                    lovable_prompt_req = f"""
                    Take the best opportunity from below:
                    {opportunities}
                    
                    Write a 'Before-After-Bridge' prompt for a Landing Page.
                    The output should be a single prompt string that I can paste into an AI image/copy generator.
                    """
                    lovable_response = model.generate_content(lovable_prompt_req)
                    final_prompt = lovable_response.text
                    
                    st.session_state.analysis_results = {
                        "pain_points": pain_points,
                        "opportunities": opportunities,
                        "final_prompt": final_prompt
                    }
                except Exception as e:
                    st.error(f"Analysis Failed: {e}")

    if st.session_state.get('analysis_results'):
        results = st.session_state.analysis_results
        
        st.markdown("### 1. Pain Points")
        st.info(results['pain_points'])
        
        st.markdown("### 2. Opportunities")
        st.success(results['opportunities'])
        
        st.markdown("### 3. Lovable Prompt")
        st.code(results['final_prompt'], language="text")


