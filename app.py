import streamlit as st
import pandas as pd
import gdown
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Hotel Assistant Pro", layout="centered")
st.title("🏨 Hotel Assistant Pro")
st.markdown("Έξυπνος βοηθός για ερωτήσεις πελατών")

st.divider()

# --- Φόρτωση δεδομένων από Google Sheet ---
st.markdown("### 📂 Δεδομένα από Google Sheet")

# >>>>>>>>>>>>>>>>>>>>>>> ΕΔΩ ΒΑΛΕ ΤΟ ID ΤΟΥ SHEET ΣΟΥ <<<<<<<<<<<<<<<<<<<<<
"https://docs.google.com/spreadsheets/d/11_KBJd6ua6FltmplT0fIEbwu0Yb3l6XgNyBaVLkqHw0/edit?gid=0#gid=0"  # Αντικατέστησε με το πραγματικό ID σου
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



# --- Δημιουργία κειμένου για το AI ---
hotel_data_full = "ΠΑΡΑΚΑΤΩ ΕΙΝΑΙ ΟΛΑ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΞΕΝΟΔΟΧΕΙΟΥ:\n"
for _, row in df.iterrows():
    hotel_data_full += f"""
- Δωμάτιο: {row['Δωμάτιο']}
  Τιμή/βράδυ: {row['Τιμή/βράδυ']}
  Παροχές: {row['Παροχές']}
  Διαθεσιμότητα Ιούλιος: {row['Διαθεσιμότητα Ιούλιος']}
  Διαθεσιμότητα Αύγουστος: {row['Διαθεσιμότητα Αύγουστος']}
"""
st.divider()

# --- Email πελάτη ---
st.markdown("### 📧 Επικόλλησε το email που έλαβες")
email_text = st.text_area("Email πελάτη:", height=150)

# --- Κουμπί ανάλυσης ---
if st.button("✍️ Δημιουργία απάντησης", type="primary"):
    if not email_text.strip():
        st.warning("Παρακαλώ επικόλλησε ένα email.")
    else:
        with st.spinner("Η τεχνητή νοημοσύνη αναλύει..."):
            prompt = f"""
Είσαι ένας εξυπηρετικός γραμματέας σε ξενοδοχείο.

Χρησιμοποίησε ΜΟΝΟ τα παρακάτω δεδομένα του ξενοδοχείου για να απαντήσεις στο email του πελάτη.

Δεδομένα ξενοδοχείου:
{hotel_data_full}

Email πελάτη:
{email_text}

Γράψε μια επαγγελματική, φιλική απάντηση στα Ελληνικά.
- Απάντα σε ΟΛΕΣ τις ερωτήσεις (τιμές, παροχές, κλπ.)
- Αν ρωτάει για συγκεκριμένη ημερομηνία, έλεγξε τη διαθεσιμότητα στα δεδομένα.
- Κλείσε με πρόταση για κράτηση.

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