import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

PASSWORD = st.secrets["password"]
CSV_URL = st.secrets["csv_url"]

# --- PROTEZIONE CON PASSWORD ---
def check_password():
    def password_entered():
        if st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Rimuove la password dalla memoria
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Ciao Willy, inserisci la password (la solita 🐈)", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Inserisci la password", type="password", on_change=password_entered, key="password")
        st.error("❌ Password errata")
        return False
    else:
        return True

if not check_password():
    st.stop()
# --- FINE PROTEZIONE ---

# Carica CSV da Google Drive
df = pd.read_csv(CSV_URL).drop_duplicates()

# Estrai il paese dall'indirizzo
df['Country'] = df['Address'].str.extract(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)$')

# Interfaccia Streamlit
st.set_page_config(page_title="Mappa degli Indirizzi", layout="wide")
st.title("📍 Esplora Indirizzi e Mappa")

# Barra laterale per la ricerca
with st.sidebar:
    st.header("Ricerca e Filtri")
    search_query = st.text_input("🔍 Cerca nome o indirizzo:", value="")
    country_list = ["Tutti"] + sorted(df['Country'].dropna().unique().tolist())
    selected_country = st.selectbox("🌍 Filtra per Paese:", country_list)
    show_map = st.checkbox("🗺️ Mostra Mappa", value=True)

# Filtraggio dei dati
filtered_df = df.copy()

if selected_country != "Tutti":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

if search_query:
    search_query = search_query.lower()
    filtered_df = filtered_df[
        filtered_df['Name'].str.lower().str.contains(search_query) |
        filtered_df['Address'].str.lower().str.contains(search_query)
    ]

# Mostra risultati filtrati
st.subheader("📋 Risultati Filtrati")
if not filtered_df.empty:
    st.dataframe(filtered_df[['Name', 'Address', 'Country']], use_container_width=True)
else:
    st.warning("Nessun risultato trovato.")

# Mappa
if show_map and not filtered_df.empty:
    st.subheader("🗺️ Mappa")
    m = folium.Map(location=[filtered_df["Latitude"].mean(), filtered_df["Longitude"].mean()], zoom_start=3)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in filtered_df.iterrows():
        popup_html = f"""
        <div style='width: 250px; font-size: 14px;'>
            <strong>{row['Name']}</strong><br>
            {row['Address']}
        </div>
        """
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup_html,
            tooltip=row["Name"],
            icon=folium.Icon(icon='map-marker', prefix='fa')
        ).add_to(marker_cluster)

    st_data = st_folium(m, width=1000, height=600, returned_objects=[])
else:
    st.info("La mappa è nascosta. Seleziona 'Mostra Mappa' nella barra laterale per visualizzarla.")
