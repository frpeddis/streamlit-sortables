import streamlit as st
import pandas as pd
from streamlit_sortables import sort_items

# Titolo dell'applicazione
st.title('Scoperte Invenzioni')

# Carica il file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.info("Attendi il caricamento del file CSV.")
    data = pd.DataFrame()

# Se i dati sono sufficienti, seleziona 5 record casuali
if not data.empty and len(data) >= 5:
    if 'selected_records' not in st.session_state:
        st.session_state['selected_records'] = data.sample(5)

    # Mostra le invenzioni casuali
    st.write('Invenzioni Casuali:')
    items = [{'header': 'Invenzioni', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]

    # Utilizza streamlit-sortables per ordinare gli elementi
    sorted_items = sort_items(items, multi_containers=True, direction="vertical")

    # Verifica l'ordine
    if st.button("Verifica Ordine"):
        ordered_records = pd.DataFrame()
        for desc in sorted_items[0]['items']:
            ordered_records = ordered_records.append(st.session_state['selected_records'][st.session_state['selected_records']['Descrizione Breve'] == desc])

        ordered_correctly = ordered_records['anno della scoperta'].is_monotonic_increasing
        if ordered_correctly and len(ordered_records) == len(sorted_items[0]['items']):
            st.success("Hai indovinato l'ordine corretto!")
        else:
            st.error("Ordine non corretto. Riprova.")
