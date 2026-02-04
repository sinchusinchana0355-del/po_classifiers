import streamlit as st
import json
from classifier import classify_po

st.set_page_config(page_title="PO category classifier", layout="centered")

st.title("PO category classifier")

st.markdown(
    """
    <style>
      /* Rounded corners for input widgets */
      div[data-baseweb="input"] > div {
        border-radius: 10px !important;
      }
      div[data-baseweb="textarea"] > div {
        border-radius: 10px !important;
      }
      /* Rounded corners for buttons */
      button[kind="primary"] {
        border-radius: 10px !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

po_description = st.text_area("PO description", height=120)
supplier = st.text_input("Supplier (optional)")

if st.button("Classify"):
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        try:
            st.json(json.loads(result))
        except Exception:
            st.error("Invalid model response")
            st.text(result)
