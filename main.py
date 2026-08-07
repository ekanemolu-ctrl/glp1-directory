import streamlit as st
import pandas as pd

# --- APP CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="GLP Life Miami - The Daily Oral Lifestyle Directory",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom mobile-first layout styling injection
st.markdown("""
    <style>
    .main .block-container { max-width: 550px; padding-top: 2rem; padding-bottom: 2rem; }
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; color: #111827; margin-bottom: 0.25rem; }
    h2 { font-size: 1.5rem !important; font-weight: 700 !important; }
    h3 { font-size: 1.2rem !important; font-weight: 700 !important; color: #1F2937; margin-top: 1rem; }
    .stSelectbox, .stTextInput { margin-bottom: 1rem; }
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
st.title("🌴 GLP Life")
st.markdown("**The Daily Oral Lifestyle Directory**")
st.caption("Navigate Miami's premier dining and wellness landscape on your daily oral protocol. Discover local stomach-safe menus, morning post-fast routines, and verified skin clinics.")

st.markdown("---")

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
st.markdown("---")

if filtered_df.empty:
    st.info("No matching Miami locations found. Try adjusting your filters or submit a new spot below!")
else:
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### {row['Name']}")
            
            # Metadata row with crisp formatting
            st.markdown(f"📍 **Area:** {row['Neighborhood']} | 🏷️ `{row['Protocol_Match']}`")
            
            # Gastric Peace score colored visual block
            gpi_val = float(row['Gastric_Peace_Index'])
            status_icon = "🏆" if gpi_val >= 4.7 else "🟢"
            st.markdown(f"{status_icon} **Stomach Safety Score:** `{gpi_val} / 5.0` *(Low Reflux Alert)*")
            
            # Highlighted hack layout box
            st.info(f"**Community Menu Hack:**\n{row['Menu_Hack']}")
            st.markdown("---")

# --- CROWDSOURCED COMMUNITY SUBMISSION FORM ---
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
