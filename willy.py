# import streamlit as st
# import pandas as pd
# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium

# # Load CSV from Google Drive
# csv_url = 'https://drive.google.com/uc?id=1uMF-hAgVr9Ha6awyz6bOJDVywbsXwhiH'
# df = pd.read_csv(csv_url).drop_duplicates()

# # Extract country from address
# df['Country'] = df['Address'].str.extract(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)$')

# # Streamlit UI
# st.set_page_config(page_title="Address Map Viewer", layout="wide")
# st.title("📍 Address Explorer & Map")

# # Sidebar search controls
# with st.sidebar:
#     st.header("Search & Filter")
#     search_query = st.text_input("🔍 Search name or address:", value="")
#     country_list = ["All"] + sorted(df['Country'].dropna().unique().tolist())
#     selected_country = st.selectbox("🌍 Filter by Country:", country_list)
#     show_map = st.checkbox("🗺️ Show Map", value=True)

# # Filter logic
# filtered_df = df.copy()

# if selected_country != "All":
#     filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# if search_query:
#     search_query = search_query.lower()
#     filtered_df = filtered_df[
#         filtered_df['Name'].str.lower().str.contains(search_query) |
#         filtered_df['Address'].str.lower().str.contains(search_query)
#     ]

# # Show filtered results table
# st.subheader("📋 Filtered Results")
# if not filtered_df.empty:
#     st.dataframe(filtered_df[['Name', 'Address', 'Country']], use_container_width=True)
# else:
#     st.warning("No matching results.")

# # Build and show map
# if show_map and not filtered_df.empty:
#     st.subheader("🗺️ Map")
#     m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=3)
#     marker_cluster = MarkerCluster().add_to(m)

#     for _, row in filtered_df.iterrows():
#         popup_html = f"""
#         <div style='width: 250px; font-size: 14px;'>
#             <strong>{row['Name']}</strong><br>
#             {row['Address']}
#         </div>
#         """
#         # folium.Marker(
#         #     location=[row["Latitude"], row["Longitude"]],
#         #     popup=popup_html,
#         #     tooltip=row["Name"]
#         # ).add_to(marker_cluster)
#         folium.Marker(
#             location=[row["Latitude"], row["Longitude"]],
#             popup=popup_html,
#             tooltip=row["Name"],
#             icon=folium.Icon(icon='map-marker', prefix='fa')  # <- this fixes the broken icon!
#         ).add_to(marker_cluster)


#     st_data = st_folium(m, width=1000, height=600, returned_objects=[])
# else:
#     st.info("Map is hidden. Check the 'Show Map' option in the sidebar to display it.")

import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# --- PASSWORD PROTECTION ---
PASSWORD = "your_password_here"

def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Remove password from memory
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input
        st.text_input("Ciao Willy, inserisci password (la solita 🐈)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Wrong password
        st.text_input("Enter password", type="password", on_change=password_entered, key="password")
        st.error("❌ Incorrect password")
        return False
    else:
        # Correct password
        return True

if not check_password():
    st.stop()
# --- END PASSWORD PROTECTION ---

# Load CSV from Google Drive
csv_url = 'https://drive.google.com/uc?id=1uMF-hAgVr9Ha6awyz6bOJDVywbsXwhiH'
df = pd.read_csv(csv_url).drop_duplicates()

# Extract country from address
df['Country'] = df['Address'].str.extract(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)$')

# Streamlit UI
st.set_page_config(page_title="Address Map Viewer", layout="wide")
st.title("📍 Address Explorer & Map")

# Sidebar search controls
with st.sidebar:
    st.header("Search & Filter")
    search_query = st.text_input("🔍 Search name or address:", value="")
    country_list = ["All"] + sorted(df['Country'].dropna().unique().tolist())
    selected_country = st.selectbox("🌍 Filter by Country:", country_list)
    show_map = st.checkbox("🗺️ Show Map", value=True)

# Filter logic
filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

if search_query:
    search_query = search_query.lower()
    filtered_df = filtered_df[
        filtered_df['Name'].str.lower().str.contains(search_query) |
        filtered_df['Address'].str.lower().str.contains(search_query)
    ]

# Show filtered results table
st.subheader("📋 Filtered Results")
if not filtered_df.empty:
    st.dataframe(filtered_df[['Name', 'Address', 'Country']], use_container_width=True)
else:
    st.warning("No matching results.")

# Build and show map
if show_map and not filtered_df.empty:
    st.subheader("🗺️ Map")
    m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=3)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in filtered_df.iterrows():
        popup_html = f"""
        <div style='width: 250px; font-size: 14px;'>
            <strong>{row['Name']}</strong><br>
            {row['Address']}
        </div>
        """
        # folium.Marker(
        #     location=[row["Latitude"], row["Longitude"]],
        #     popup=popup_html,
        #     tooltip=row["Name"]
        # ).add_to(marker_cluster)
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup_html,
            tooltip=row["Name"],
            icon=folium.Icon(icon='map-marker', prefix='fa')  # <- this fixes the broken icon!
        ).add_to(marker_cluster)


    st_data = st_folium(m, width=1000, height=600, returned_objects=[])
else:
    st.info("Map is hidden. Check the 'Show Map' option in the sidebar to display it.")
