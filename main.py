import streamlit as st
import pandas as pd
import time

# --- APP CONFIGURATION & THEME STYLING ---
st.set_page_config(
    page_title="GLP Life Miami - The Daily Oral Lifestyle Directory",
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp { background-color: #0B0F19 !important; color: #E2E8F0 !important; }
    .main .block-container { max-width: 520px; padding-top: 1.5rem; padding-bottom: 2rem; }
    h1 { font-family: 'Inter', sans-serif !important; font-size: 2.6rem !important; font-weight: 800 !important; color: #FFFFFF !important; margin-bottom: 0.1rem; letter-spacing: -0.05em; }
    h3 { font-size: 1.3rem !important; font-weight: 700 !important; color: #00F5A0 !important; margin-top: 1.5rem; }
    .glp-card { background-color: #161F30 !important; border: 1px solid #24334D !important; border-radius: 16px !important; padding: 1.25rem !important; margin-bottom: 1.25rem !important; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important; }
    .stAlert { background-color: #1E293B !important; color: #F8FAFC !important; border-left: 4px solid #00F5A0 !important; border-radius: 8px !important; }
    .stButton>button { background-color: #00F5A0 !important; color: #0B0F19 !important; border-radius: 30px !important; border: none !important; padding: 0.5rem 2rem !important; width: 100% !important; font-weight: 700 !important; letter-spacing: 0.05em; }
    .timer-btn>button { background-color: #FF4B4B !important; color: white !important; }
    input, select, textarea { background-color: #161F30 !important; color: #FFFFFF !important; border: 1px solid #24334D !important; }
    hr { border-top: 1px solid #24334D !important; }
    code { background-color: #0B0F19 !important; color: #00F5A0 !important; padding: 0.2rem 0.4rem !important; border-radius: 4px !important; }
    </style>
""", unsafe_allow_html=True)

# --- REAL-WORLD DATA SEEDING ---
if 'directory_data' not in st.session_state:
    st.session_state.directory_data = pd.DataFrame([
        {"Name": "Pura Vida (Brickell)", "Neighborhood": "Brickell", "Protocol_Match": "Wegovy Pill (Morning Fasting Friendly)", "Gastric_Peace_Index": 4.8, "Min_Protein_g": 25, "Menu_Hack": "Perfect for the post-fast window. Order the 'Perfect Egg Sandwich' on gluten-free bread with zero aioli. Pair with almond milk latte."},
        {"Name": "Mandolin Aegean Bistro", "Neighborhood": "Design District", "Protocol_Match": "Universal GLP-1 Friendly", "Gastric_Peace_Index": 4.9, "Min_Protein_g": 42, "Menu_Hack": "Order the Grilled Octopus. Clean, premium olive oil base prevents the severe delayed-emptying nausea common with heavy commercial seed oils."},
        {"Name": "Coyo Taco", "Neighborhood": "Wynwood", "Protocol_Match": "Foundayo (Anytime On-The-Go)", "Gastric_Peace_Index": 4.1, "Min_Protein_g": 30, "Menu_Hack": "Avoid active salsas and onions to prevent late-day acid reflux. Request a naked chicken bowl over plain lettuce with sliced avocados."},
        {"Name": "SkinLocal MedSpa", "Neighborhood": "Brickell", "Protocol_Match": "Aesthetic & Skin Architecture", "Gastric_Peace_Index": 5.0, "Min_Protein_g": 0, "Menu_Hack": "Top tier for rapid-weight-loss skin laxity. Offers a specialized 'GLP-1 Collagen Protocol' merging targeted fillers and RF skin tightening."}
    ])

# --- HEADER HERO ---
st.title("🧬 GLP Life")
st.markdown("<p style='font-size:1.1rem; font-weight:700; color:#00F5A0; margin:0; letter-spacing:0.05em;'>THE MODERN BIO-HACKER PROTOCOL</p>", unsafe_allow_html=True)
st.caption("Precision lifestyle management for daily oral metabolic protocols. Map stomach-safe dining, track fasting routines, and counteract muscle wasting.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- FEATURE 1: VALUE-ADD 30-MIN MORNING FAST TIMER ---
st.markdown("### ⏱️ Morning Fasting Companion")
if 'timer_triggered' not in st.session_state:
    st.session_state.timer_triggered = False

if not st.session_state.timer_triggered:
    if st.button("🔴 Just Took My Daily Pill (Start 30-Min Fast)"):
        st.session_state.timer_triggered = True
        st.rerun()
else:
    st.success("⏳ Your empty-stomach absorption window is active! Protect your dose.")
    st.info("💡 **While you wait:** Avoid drinking coffee, consuming vitamins, or taking other oral tablets for the next 30 minutes to guarantee maximum clinical efficacy.")
    if st.button("Reset Timer", key="reset_btn"):
        st.session_state.timer_triggered = False
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# --- FEATURE 2: VALUE-ADD METABOLIC PROTEIN FILTER ---
st.markdown("### 🔍 Smart Local Discovery")

# Protein deficit sliding scale configuration
protein_deficit = st.slider(
    "How much protein (grams) do you still need to hit your goal today?",
    min_value=0, max_value=80, value=0, step=5,
    help="We will filter and prioritize local meals capable of matching your muscle-preservation goals."
)

protocol_filter = st.selectbox(
    "Filter by daily medication profile:",
    options=["All Categories", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)", "Aesthetic & Skin Architecture"]
)

neighborhood_search = st.text_input("Search neighborhood or establishment:", placeholder="e.g., Brickell, Pura Vida")

# --- FILTER ARCHITECTURE LOGIC ---
filtered_df = st.session_state.directory_data

# Apply protein metric filter dynamically
if protein_deficit > 0:
    filtered_df = filtered_df[filtered_df['Min_Protein_g'] >= (protein_deficit * 0.5)] # Matches meals solving at least half their remaining deficit

if protocol_filter != "All Categories":
    filtered_df = filtered_df[(filtered_df['Protocol_Match'] == protocol_filter) | (filtered_df['Protocol_Match'] == "Universal GLP-1 Friendly")]

if neighborhood_search:
    filtered_df = filtered_df[(filtered_df['Name'].str.contains(neighborhood_search, case=False)) | (filtered_df['Neighborhood'].str.contains(neighborhood_search, case=False))]

# --- RENDER RESULTS ---
st.markdown(f"**Showing {len(filtered_df)} Tailored Results**")

if filtered_df.empty:
    st.info("No matching profiles found. Try lowering your remaining protein requirements or clear the text search filter.")
else:
    for idx, row in filtered_df.iterrows():
        status_icon = "🏆" if row['Gastric_Peace_Index'] >= 4.7 else "🟢"
        protein_tag = f"🥩 {row['Min_Protein_g']}g Protein" if row['Min_Protein_g'] > 0 else "✨ Wellness"
        
        card_html = f"""
        <div class="glp-card">
            <h3 style="margin:0 0 0.25rem 0; color:#FFFFFF;">{row['Name']}</h3>
            <p style="font-size:0.85rem; margin:0 0 0.5rem 0; color:#94A3B8;">
                📍 <b>Area:</b> {row['Neighborhood']} | <span style="color:#00F5A0;"><b>{protein_tag}</b></span>
            </p>
            <p style="font-size:0.9rem; margin:0; color:#E2E8F0;">
                {status_icon} <b>Stomach Safety Score:</b> <code>{row['Gastric_Peace_Index']} / 5.0</code>
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        st.info(f"**Targeted Action Optimization:**\n{row['Menu_Hack']}")

# --- CROWDSOURCED ENTRY PIPELINE ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### ➕ Contribute a Core Protocol Review")
with st.form("submission_form", clear_on_submit=True):
    new_name = st.text_input("Business Name*")
    new_hood = st.text_input("Miami Neighborhood Area*")
    new_protocol = st.selectbox("Medication Category Match*", ["Universal GLP-1 Friendly", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)", "Aesthetic & Skin Architecture"])
    new_protein = st.number_input("Estimated Protein Yield per serving (grams)*", min_value=0, max_value=100, value=25)
    new_gpi = st.slider("Stomach Safety Rating (1 = High GI Distress, 5 = Safe)*", 1.0, 5.0, 4.5, 0.1)
    new_hack = st.text_area("What is the exact clinical hack or menu workaround?*")
    submit_button = st.form_submit_button("Log Protocol Review")
    
    if submit_button and new_name and new_hood and new_hack:
        new_entry = {"Name": new_name, "Neighborhood": new_hood, "Protocol_Match": new_protocol, "Gastric_Peace_Index": new_gpi, "Min_Protein_g": new_protein, "Menu_Hack": new_hack}
        st.session_state.directory_data = pd.concat([st.session_state.directory_data, pd.DataFrame([new_entry])], ignore_index=True)
        st.success(f"🎉 Entry mapped! '{new_name}' integrated successfully.")
        st.rerun()
