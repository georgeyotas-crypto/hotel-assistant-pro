import streamlit as st
from openai import OpenAI
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Hotel Assistant Pro", layout="centered")
st.title("🏨 Hotel Assistant Pro")
st.markdown("Έξυπνος βοηθός για ερωτήσεις πελατών")

st.divider()

# --- Σύνδεση με Google Sheet ---
st.markdown("### 📂 Δεδομένα από Google Sheet")

# Αρχικοποίηση session state για τα δεδομένα
if "df" not in st.session_state:
    st.session_state.df = None
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None

# Κουμπί ανανέωσης
col1, col2 = st.columns([3, 1])
with col2:
    refresh_button = st.button("🔄 Ανανέωση δεδομένων", use_container_width=True)

# Συνάρτηση για φόρτωση δεδομένων
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        st.session_state.df = df
        st.session_state.last_refresh = datetime.now().strftime("%H:%M:%S")
        return df
    except Exception as e:
        st.error(f"Σφάλμα σύνδεσης: {e}")
        return None

# Φόρτωση δεδομένων (στην αρχή ή μετά από refresh)
if refresh_button or st.session_state.df is None:
    st.session_state.df = load_data()

# Εμφάνιση δεδομένων
if st.session_state.df is not None:
    st.success(f"✅ Συνδέθηκε! Βρέθηκαν {len(st.session_state.df)} δωμάτια.")
    if st.session_state.last_refresh:
        st.caption(f"Τελευταία ανανέωση: {st.session_state.last_refresh}")
    st.dataframe(st.session_state.df)
    
    # Δημιουργία κειμένου με ΟΛΑ τα δεδομένα
    hotel_data_full = "ΠΑΡΑΚΑΤΩ ΕΙΝΑΙ ΟΛΑ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΞΕΝΟΔΟΧΕΙΟΥ:\n"
    for _, row in st.session_state.df.iterrows():
        hotel_data_full += f"""
- Δωμάτιο: {row['Δωμάτιο']}
  Τιμή/βράδυ: {row['Τιμή/βράδυ']}
  Παροχές: {row['Παροχές']}
  Διαθεσιμότητα Ιούλιος: {row['Διαθεσιμότητα Ιούλιος']}
  Διαθεσιμότητα Αύγουστος: {row['Διαθεσιμότητα Αύγουστος']}
"""
else:
    st.warning("Δεν ήταν δυνατή η φόρτωση δεδομένων. Παρακαλώ ελέγξτε τη σύνδεση.")
    st.stop()

st.divider()

# --- Email πελάτη ---
st.markdown("### 📧 Επικόλλησε το email που έλαβες")
email_text = st.text_area(
    "Email πελάτη:",
    height=150,
    placeholder="Π.χ.: Καλησπέρα, υπάρχει διαθεσιμότητα για δίκλινο 10-15 Αυγούστου; Δέχεστε σκύλο;"
)

# --- Κουμπί ανάλυσης ---
if st.button("✍️ Δημιουργία απάντησης", type="primary"):
    if not email_text.strip():
        st.warning("Παρακαλώ επικόλλησε ένα email.")
    else:
        with st.spinner("Η τεχνητή νοημοσύνη αναλύει και απαντά..."):
            prompt = f"""
Είσαι ένας εξυπηρετικός γραμματέας σε ξενοδοχείο.

Χρησιμοποίησε ΜΟΝΟ τα παρακάτω δεδομένα του ξενοδοχείου για να απαντήσεις στο email του πελάτη.

Δεδομένα ξενοδοχείου:
{hotel_data_full}

Email πελάτη:
{email_text}

Γράψε μια επαγγελματική, φιλική απάντηση στα Ελληνικά.
- Απάντα σε ΟΛΕΣ τις ερωτήσεις (τιμές, παροχές, σκύλους, wifi, πάρκινγκ, κλπ.)
- Αν ρωτάει για συγκεκριμένη ημερομηνία, έλεγξε τη διαθεσιμότητα στα δεδομένα
- Αν η ημερομηνία ΔΕΝ υπάρχει, εξήγησέ το ευγενικά και πρότεινε εναλλακτικές
- Κλείσε με πρόταση για κράτηση

Απάντηση:
"""
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            answer = response.choices[0].message.content
            st.success("✅ Η απάντηση δημιουργήθηκε!")
            st.markdown(answer)

# --- Sidebar με οδηγίες ---
st.sidebar.markdown("### 💡 Πώς λειτουργεί")
st.sidebar.info(
    "1️⃣ Το Google Sheet περιέχει δωμάτια, τιμές, παροχές και διαθεσιμότητα\n"
    "2️⃣ Πατήστε 'Ανανέωση δεδομένων' για να δείτε τις τελευταίες αλλαγές στο sheet\n"
    "3️⃣ Επικολλήστε το email του πελάτη\n"
    "4️⃣ Το AI διαβάζει τα δεδομένα και απαντάει σε όλες τις ερωτήσεις\n\n"
    "**Το Google Sheet πρέπει να είναι δημόσιο (Anyone with the link → Viewer)**"
)