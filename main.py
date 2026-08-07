import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="GastricPeace Miami - Oral GLP-1 Directory",
    page_icon="🌴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- REAL-WORLD LOCAL MIAMI DATA ---
if 'directory_data' not in st.session_state:
    st.session_state.directory_data = pd.DataFrame([
        {
            "Name": "Pura Vida (Brickell)",
            "Neighborhood": "Brickell / South Beach",
            "Protocol_Match": "Wegovy Pill (Morning Fasting Friendly)",
            "Gastric_Peace_Index": "4.8 / 5.0",
            "Menu_Hack": "Perfect for the post-30-minute fasting window. Order the 'Perfect Egg Sandwich' on gluten-free bread, but request zero aioli. Pair with an iced almond milk latte to completely bypass morning dairy-induced nausea."
        },
        {
            "Name": "Mandolin Aegean Bistro",
            "Neighborhood": "Design District",
            "Protocol_Match": "Universal GLP-1 Friendly",
            "Gastric_Peace_Index": "4.9 / 5.0",
            "Menu_Hack": "Order the Grilled Octopus and a side of plain Greek yogurt. The kitchen uses clean, high-grade olive oil rather than inflammatory seed oils, making it completely safe for highly sensitive, delayed-emptying digestive tracts."
        },
        {
            "Name": "Coyo Taco",
            "Neighborhood": "Wynwood / Brickell",
            "Protocol_Match": "Foundayo (Anytime On-The-Go)",
            "Gastric_Peace_Index": "4.1 / 5.0",
            "Menu_Hack": "Pill-users alert: Avoid the standard salsa and pickled onions, which trigger immediate late-afternoon acid reflux. Order the pollo al carbon as a naked bowl over plain shredded lettuce with avocado slices for clean macros."
        },
        {
            "Name": "SkinLocal MedSpa",
            "Neighborhood": "MiMo District / Brickell",
            "Protocol_Match": "Aesthetic & Skin Architecture",
            "Gastric_Peace_Index": "5.0 / 5.0",
            "Menu_Hack": "Highly rated by oral protocol patients for targeting rapid-weight-loss skin laxity. Ask for their specialized 'GLP-1 Collagen Boosting Protocol' combining custom mid-face fillers and radiofrequency skin tightening."
        }
    ])

# --- HEADER SECTION ---
st.title("🌴 GastricPeace Miami")
st.subheader("The Daily Oral GLP-1 Lifestyle Directory")
st.write("Navigating Miami's food and wellness scene on a daily protocol. Discover local safe menus, morning post-fast routines, and verified skin clinics.")

st.markdown("---")

# --- FILTERING INTERFACE ---
st.markdown("### 🔍 Filter by Local Need")

protocol_filter = st.selectbox(
    "What is your daily medication protocol / need?",
    options=["All Protocols", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)", "Aesthetic & Skin Architecture"]
)

neighborhood_search = st.text_input("Search Miami Neighborhood or Business Name:", placeholder="e.g., Brickell, Design District, Pura Vida")

# --- DATA FILTERING LOGIC ---
filtered_df = st.session_state.directory_data

if protocol_filter != "All Protocols":
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
st.markdown(f"#### Showing {len(filtered_df)} Verified Miami Spots")

if filtered_df.empty:
    st.info("No matching Miami locations found. Try adjusting your filters or submit a new spot below!")
else:
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### {row['Name']}")
            st.markdown(f"📍 **Area:** {row['Neighborhood']} | 💊 **Category:** {row['Protocol_Match']}")
            st.markdown(f"🤢 **Stomach Safety Score:** `{row['Gastric_Peace_Index']}`")
            st.markdown(f"💡 **Exact Local Hack:** {row['Menu_Hack']}")
            st.markdown("---")

# --- CROWDSOURCED COMMUNITY SUBMISSION FORM ---
st.markdown("### ➕ Add a Miami Menu Hack or Clinic")
with st.form("submission_form", clear_on_submit=True):
    new_name = st.text_input("Business Name*")
    new_hood = st.text_input("Miami Neighborhood (e.g., Brickell, Coconut Grove)*")
    new_protocol = st.selectbox(
        "Category Match*",
        options=["Universal GLP-1 Friendly", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)", "Aesthetic & Skin Architecture"]
    )
    new_gpi = st.slider("Stomach Safe / Satisfaction Score (1-5)*", 1.0, 5.0, 4.5, 0.1)
    new_hack = st.text_area("What is the exact menu hack, ordering setup, or treatment configuration?*")
    
    submit_button = st.form_submit_button("Submit Anonymous Miami Review")
    
    if submit_button:
        if new_name and new_hood and new_hack:
            new_entry = {
                "Name": new_name,
                "Neighborhood": new_hood,
                "Protocol_Match": new_protocol,
                "Gastric_Peace_Index": f"{new_gpi} / 5.0",
                "Menu_Hack": new_hack
            }
            st.session_state.directory_data = pd.concat([st.session_state.directory_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"🎉 Success! '{new_name}' has been added to the live Miami view.")
            st.rerun()
