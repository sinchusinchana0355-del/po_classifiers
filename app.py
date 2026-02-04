if st.session_state.history:
    if st.button("Show last result"):
        last = st.session_state.history[0]
        st.subheader("Last result")
        st.text(f"Description: {last['description']}")
        if last["supplier"]:
            st.text(f"Supplier: {last['supplier']}")
        if isinstance(last["result"], (dict, list)):
            st.json(last["result"])
        else:
            st.text(last["result"])

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
