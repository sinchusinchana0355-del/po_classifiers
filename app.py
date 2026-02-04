import streamlit as st
import json
from datetime import datetime
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

if "po_description" not in st.session_state:
    st.session_state.po_description = ""

if "history" not in st.session_state:
    st.session_state.history = []

sample_options = {
    "IT hardware": "Purchase of 20 laptop chargers and 10 USB-C docking stations for IT rollout",
    "Office supplies": "Order of 15 boxes of printer paper and 50 blue ballpoint pens",
    "Facilities": "Monthly HVAC maintenance service for headquarters building",
}

if st.button("Use sample input 1"):
    st.session_state.po_description = sample_options["IT hardware"]

if st.button("Use sample input 2"):
    st.session_state.po_description = sample_options["Office supplies"]

selected_sample = st.selectbox("Sample inputs", list(sample_options.keys()))
if st.button("Apply selected sample"):
    st.session_state.po_description = sample_options[selected_sample]

po_description = st.text_area(
    "PO description",
    height=120,
    key="po_description",
)
supplier = st.text_input("Supplier (optional)")

if st.button("Classify"):
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        parsed = None
        if isinstance(result, (dict, list)):
            parsed = result
        else:
            try:
                parsed = json.loads(result)
            except Exception:
                parsed = None

        st.subheader("Result")
        if parsed is not None:
            st.json(parsed)
        else:
            st.error("Invalid model response")
            st.text(result)

        st.session_state.history.insert(
            0,
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "description": po_description.strip(),
                "supplier": supplier.strip(),
                "result": parsed if parsed is not None else result,
            },
        )
        st.session_state.history = st.session_state.history[:5]

if st.session_state.history:
    st.subheader("Recent history")
    for item in st.session_state.history:
        st.markdown(f"**{item['timestamp']}**")
        st.text(f"Description: {item['description']}")
        if item["supplier"]:
            st.text(f"Supplier: {item['supplier']}")
        if isinstance(item["result"], (dict, list)):
            st.json(item["result"])
        else:
            st.text(item["result"])
