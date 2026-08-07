import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="GastricPeace - GLP-1 Dining Directory",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MOCK DATA ---
# In a production app, this would be linked to a Google Sheet or database.
if 'directory_data' not in st.session_state:
    st.session_state.directory_data = pd.DataFrame([
        {
            "Name": "Green Garden Bistro",
            "Neighborhood": "Downtown",
            "Protocol_Match": "Wegovy Pill (Morning Fasting Friendly)",
            "Gastric_Peace_Index": "4.8 / 5.0",
            "Menu_Hack": "Offers a 'Micro 3oz Salmon Filet' off-menu. Replaces heavy cooking oils with bone broth upon request."
        },
        {
            "Name": "The Protein Foundry",
            "Neighborhood": "Westside",
            "Protocol_Match": "Foundayo (Anytime On-The-Go)",
            "Gastric_Peace_Index": "4.9 / 5.0",
            "Menu_Hack": "Features zero-sugar functional elixirs and ginger-infused anti-nausea shots. Custom clean macro bowls available."
        },
        {
            "Name": "Olive & Vine Tapas",
            "Neighborhood": "Midtown",
            "Protocol_Match": "Universal GLP-1 Friendly",
            "Gastric_Peace_Index": "4.2 / 5.0",
            "Menu_Hack": "Explicitly permits adults to order high-protein small plates from the kids menu with zero split-plate fees."
        }
    ])

# --- HEADER SECTION ---
st.title("🍽️ GastricPeace")
st.subheader("The Living Directory for the Daily GLP-1 Generation")
st.write("Stop guessing what to order. Discover restaurants, menus, and dishes optimized for daily oral weight-loss protocols.")

st.markdown("---")

# --- FILTERING INTERFACE ---
st.markdown("### 🔍 Find a Safe Spot")

# Filter 1: Medication Protocol
protocol_filter = st.selectbox(
    "What is your daily medication protocol?",
    options=["All Protocols", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)"]
)

# Filter 2: Neighborhood Search
neighborhood_search = st.text_input("Enter neighborhood or city:", placeholder="e.g., Downtown")

# --- DATA FILTERING LOGIC ---
filtered_df = st.session_state.directory_data

if protocol_filter != "All Protocols":
    # Match specific protocol or universal spots
    filtered_df = filtered_df[
        (filtered_df['Protocol_Match'] == protocol_filter) | 
        (filtered_df['Protocol_Match'] == "Universal GLP-1 Friendly")
    ]

if neighborhood_search:
    filtered_df = filtered_df[filtered_df['Neighborhood'].str.contains(neighborhood_search, case=False)]

# --- DISPLAY RESULTS ---
st.markdown(f"#### Showing {len(filtered_df)} Verified Results")

if filtered_df.empty:
    st.info("No matching locations found. Try adjusting your filters or be the first to submit a spot below!")
else:
    for idx, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### {row['Name']}")
            st.markdown(f"📍 **Neighborhood:** {row['Neighborhood']} | 💊 **Protocol:** {row['Protocol_Match']}")
            st.markdown(f"🤢 **Gastric Peace Index:** `{row['Gastric_Peace_Index']}` *(Low Reflux/Nausea Rating)*")
            st.markdown(f"💡 **Unlisted Menu Hack:** {row['Menu_Hack']}")
            st.markdown("---")

# --- CROWDSOURCED COMMUNITY SUBMISSION FORM ---
st.markdown("### ➕ Share a GLP-1 Friendly Spot")
st.write("Help the community map out more safe spaces by submitting your favorite restaurant hack.")

with st.form("submission_form", clear_on_submit=True):
    new_name = st.text_input("Restaurant Name*")
    new_hood = st.text_input("Neighborhood/City*")
    new_protocol = st.selectbox(
        "Which protocol handles this spot best?*",
        options=["Universal GLP-1 Friendly", "Wegovy Pill (Morning Fasting Friendly)", "Foundayo (Anytime On-The-Go)"]
    )
    new_gpi = st.slider("Gastric Peace Index (1 = Triggered severe nausea/reflux, 5 = Completely stomach safe)", 1.0, 5.0, 4.5, 0.1)
    new_hack = st.text_area("What is the unlisted menu hack? (e.g., small portions allowed, ginger shots, oil swaps)*")
    
    submit_button = st.form_submit_button("Submit Anonymous Review")
    
    if submit_button:
        if new_name and new_hood and new_hack:
            # Format new entry
            new_entry = {
                "Name": new_name,
                "Neighborhood": new_hood,
                "Protocol_Match": new_protocol,
                "Gastric_Peace_Index": f"{new_gpi} / 5.0",
                "Menu_Hack": new_hack
            }
            # Append to session state data
            st.session_state.directory_data = pd.concat([st.session_state.directory_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"🎉 Thank you! '{new_name}' has been temporarily added to your local view.")
            st.rerun()
        else:
            st.error("Please fill out all required fields marked with an asterisk (*).")
