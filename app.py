import json
import streamlit as st
from classifier import classify_po

st.set_page_config(page_title="PO Category Classifier", layout="centered")
st.title("PO Category Classifier")

with st.form("po_form"):
    po_description = st.text_area("PO description", height=120)
    supplier = st.text_input("Supplier (optional)")
    submitted = st.form_submit_button("Classify")

if submitted:
    po_description = po_description.strip()
    supplier = supplier.strip()

    if not po_description:
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        if isinstance(result, (dict, list)):
            st.json(result)
        else:
            try:
                st.json(json.loads(result))
            except Exception:
                st.error("Invalid model response.")
                with st.expander("Raw response"):
                    st.text(result)
