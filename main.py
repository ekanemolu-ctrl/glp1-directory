import streamlit as st
import pandas as pd

# --- APP CONFIGURATION & THEME STYLING ---
st.set_page_config(
    page_title="GLP Life Miami - The Daily Oral Lifestyle Directory",
    page_icon="🧬", # Updated to a DNA helix representing clinical biology and molecular health
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom mobile CSS injection to completely override standard Streamlit branding
st.markdown("""
    <style>
    /* Main Background & Text Color */
    .stApp {
        background-color: #FBFBF9 !important;
        color: #1A3020 !important;
    }
    
    /* Document Container Max-Width for Mobile Screens */
    .main .block-container { 
        max-width: 520px; 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
    }
    
    /* Custom Luxury Typography Hierarchy */
    h1 { 
        font-family: 'Playfair Display', serif !important;
        font-size: 2.6rem !important; 
        font-weight: 800 !important; 
        color: #0F291B !important; 
        margin-bottom: 0.1rem; 
    }
    h3 { 
        font-size: 1.3rem !important; 
        font-weight: 700 !important; 
        color: #0F291B !important; 
        margin-top: 1.5rem; 
    }
    
    /* Custom Content Card Blocks */
    .glp-card {
        background-color: #FFFFFF !important;
        border: 1px solid #EAEAE4 !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 4px 12px rgba(15, 41, 27, 0.02) !important;
    }
    
    /* Styled Community Custom Info Box */
    .stAlert {
        background-color: #F1F4F1 !important;
        color: #1A3020 !important;
        border-left: 4px solid #2D5A27 !important;
        border-radius: 8px !important;
    }
    
    /* Styling Buttons to Premium Brand Green */
    .stButton>button {
        background-color: #0F291B !important;
        color: #FFFFFF !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
        width: 100% !important;
        font-weight: 600 !important;
    }
    
    /* Clean Divider Line */
    hr { border-top: 1px solid #EAEAE4 !important; }
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
st.title("🧬 GLP Life") # Replaced the tropical palm with a biological DNA helix anchor
st.markdown("<p style='font-size:1.1rem; font-weight:600; color:#2D5A27; margin:0;'>The Daily Oral Lifestyle Directory</p>", unsafe_allow_html=True)
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
            <h3 style="margin:0 0 0.25rem 0; color:#0F291B;">{row['Name']}</h3>
            <p style="font-size:0.85rem; margin:0 0 0.5rem 0; color:#5A6B5D;">
                📍 <b>Area:</b> {row['Neighborhood']} | 🏷️ <i>{row['Protocol_Match']}</i>
            </p>
            <p style="font-size:0.9rem; margin:0 0 0.5rem 0; color:#0F291B;">
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
