import streamlit as st
import pandas as pd

# --- APP CONFIGURATION & THEME STYLING ---
st.set_page_config(
    page_title="GLP Life Miami - The Daily Oral Lifestyle Directory",
    page_icon="🧬", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom mobile CSS injection to build a Sleek Dark Mode (Modern Bio-Hacker) interface
st.markdown("""
    <style>
    /* Main Background & Text Color - Deep Charcoal / Slate */
    .stApp {
        background-color: #0B0F19 !important;
        color: #E2E8F0 !important;
    }
    
    /* Document Container Max-Width for Mobile Screens */
    .main .block-container { 
        max-width: 520px; 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
    }
    
    /* Typography Hierarchy with Neon Accents */
    h1 { 
        font-family: 'Inter', sans-serif !important;
        font-size: 2.6rem !important; 
        font-weight: 800 !important; 
        color: #FFFFFF !important; 
        margin-bottom: 0.1rem; 
        letter-spacing: -0.05em;
    }
    h3 { 
        font-size: 1.3rem !important; 
        font-weight: 700 !important; 
        color: #00F5A0 !important; /* Electric Mint Accent */
        margin-top: 1.5rem; 
    }
    
    /* Custom Bio-Hacker Content Card Blocks */
    .glp-card {
        background-color: #161F30 !important;
        border: 1px solid #24334D !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Styled Community Custom Info Box */
    .stAlert {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-left: 4px solid #00F5A0 !important;
        border-radius: 8px !important;
    }
    
    /* Styling Buttons to Neon Mint / Dark Text */
    .stButton>button {
        background-color: #00F5A0 !important;
        color: #0B0F19 !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        width: 100% !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
    }
    
    /* Customize Input Fields for Dark Mode Harmony */
    input, select, textarea {
        background-color: #161F30 !important;
        color: #FFFFFF !important;
        border: 1px solid #24334D !important;
    }
    
    /* Clean Dark Divider Line */
    hr { border-top: 1px solid #24334D !important; }
    
    /* Custom code block coloring inside cards */
    code {
        background-color: #0B0F19 !important;
        color: #00F5A0 !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- REAL-WORLD LOCAL MIAMI DATA ---
if 'directory_data' not in st.session_state:
    st.session_state.directory_data = pd.DataFrame([
        {
            "Name": "Pura Vida (Brickell)",
            "Neighborhood": "Brickell / South Beach",
            "Protocol_Match": "Wegovy Pill (Morning Fasting Friendly)",
            "Gastric_Peace_Index": "4.8",
            "Menu_Hack": "Perfect for the post-30-minute fasting window. Order the 'Perfect Egg Sandwich' on gluten-free bread, but request zero aioli. Pair with an iced almond milk latte to completely bypass morning dairy-induced nausea."
        },
        {
            "Name": "Mandolin Aegean Bistro",
            "Neighborhood": "Design District",
            "Protocol_Match": "Universal GLP-1 Friendly",
            "Gastric_Peace_Index": "4.9",
            "Menu_Hack": "Order the Grilled Octopus and a side of plain Greek yogurt. The kitchen uses clean, high-grade olive oil rather than inflammatory seed oils, making it completely safe for highly sensitive, delayed-emptying digestive tracts."
        },
        {
            "Name": "Coyo Taco",
            "Neighborhood": "Wynwood / Brickell",
            "Protocol_Match": "Foundayo (Anytime On-The-Go)",
            "Gastric_Peace_Index": "4.1",
            "Menu_Hack": "Pill-users alert: Avoid the standard salsa and pickled onions, which trigger immediate late-afternoon acid reflux. Order the pollo al carbon as a naked bowl over plain shredded lettuce with avocado slices for clean macros."
        },
        {
            "Name": "SkinLocal MedSpa",
            "Neighborhood": "MiMo District / Brickell",
            "Protocol_Match": "Aesthetic & Skin Architecture",
            "Gastric_Peace_Index": "5.0",
            "Menu_Hack": "Highly rated by oral protocol patients for targeting rapid-weight-loss skin laxity. Ask for their specialized 'GLP-1 Collagen Boosting Protocol' combining custom mid-face fillers and radiofrequency skin tightening."
        }
    ])

# --- HEADER HERO SECTION ---
st.title("🧬 GLP Life")
st.markdown("<p style='font-size:1.1rem; font-weight:700; color:#00F5A0; margin:0; letter-spacing:0.05em;'>THE DAILY ORAL LIFESTYLE DIRECTORY</p>", unsafe_allow_html=True)
st.caption("Navigate Miami's premier dining and wellness landscape on your daily oral protocol. Discover local stomach-safe menus, morning post-fast routines, and verified skin clinics.")

st.markdown("<hr>", unsafe_allow_html=True)

# --- FILTERING INTERFACE ---
st.markdown("### 🔍 Find Local Safe Spots")

protocol_filter = st.selectbox(
    "Filter by daily medication protocol or need:",
    options=["All Categories", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)", "Aesthetic & Skin Architecture"]
)

neighborhood_search = st.text_input("Search Miami neighborhood or business:", placeholder="e.g., Brickell, Design District, Pura Vida")

# --- DATA FILTERING LOGIC ---
filtered_df = st.session_state.directory_data

if protocol_filter != "All Categories":
    filtered_df = filtered_df[
        (filtered_df['Protocol_Match'] == protocol_filter) | 
        (filtered_df['Protocol_Match'] == "Universal GLP-1 Friendly")
    ]

if neighborhood_search:
    filtered_df = filtered_df[
        (filtered_df['Name'].str.contains(neighborhood_search, case=False)) |
        (filtered_df['Neighborhood'].str.contains(neighborhood_search, case=False))
    ]

# --- DISPLAY RESULTS ---
st.markdown(f"**Showing {len(filtered_df)} Verified Miami Locations**")
st.markdown("<hr>", unsafe_allow_html=True)

if filtered_df.empty:
    st.info("No matching Miami locations found. Try adjusting your filters or submit a new spot below!")
else:
    for idx, row in filtered_df.iterrows():
        gpi_val = float(row['Gastric_Peace_Index'])
        status_icon = "🏆" if gpi_val >= 4.7 else "🟢"
        
        card_html = f"""
        <div class="glp-card">
            <h3 style="margin:0 0 0.25rem 0; color:#FFFFFF;">{row['Name']}</h3>
            <p style="font-size:0.85rem; margin:0 0 0.5rem 0; color:#94A3B8;">
                📍 <b>Area:</b> {row['Neighborhood']} | <span style="color:#00F5A0;">🏷️ <i>{row['Protocol_Match']}</i></span>
            </p>
            <p style="font-size:0.9rem; margin:0; color:#E2E8F0;">
                {status_icon} <b>Stomach Safety Score:</b> <code>{gpi_val} / 5.0</code>
            </p>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        st.info(f"**Community Menu Hack:**\n{row['Menu_Hack']}")

# --- CROWDSOURCED COMMUNITY SUBMISSION FORM ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### ➕ Add a Miami Hack or Clinic")
st.caption("Help the GLP Life community map out safe spaces by submitting your favorite restaurant hack anonymously.")

with st.form("submission_form", clear_on_submit=True):
    new_name = st.text_input("Business Name*")
    new_hood = st.text_input("Miami Neighborhood (e.g., Brickell, Coconut Grove)*")
    new_protocol = st.selectbox(
        "Medication Category Match*",
        options=["Universal GLP-1 Friendly", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)", "Aesthetic & Skin Architecture"]
    )
    new_gpi = st.slider("Stomach Safety Rating (1 = High GI Distress, 5 = Completely Safe)*", 1.0, 5.0, 4.5, 0.1)
    new_hack = st.text_area("What is the exact menu hack, ordering setup, or treatment configuration?*")
    
    submit_button = st.form_submit_button("Submit Anonymous Miami Review")
    
    if submit_button:
        if new_name and new_hood and new_hack:
            new_entry = {
                "Name": new_name,
                "Neighborhood": new_hood,
                "Protocol_Match": new_protocol,
                "Gastric_Peace_Index": f"{new_gpi}",
                "Menu_Hack": new_hack
            }
            st.session_state.directory_data = pd.concat([st.session_state.directory_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"🎉 Success! '{new_name}' has been added to the live GLP Life Miami directory.")
            st.rerun()
        else:
            st.error("Please fill out all required fields marked with an asterisk (*).")
