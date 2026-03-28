import streamlit as st
import requests

st.set_page_config(page_title="Mushroom Classifier", page_icon="🍄")

st.title("Mushroom Edibility Predictor")
st.markdown("Enter the characteristics of the mushroom to check if it's safe to eat.")


with st.form("mushroom_form"):
    col1, col2 = st.columns(2)

    with col1:
        cap_shape = st.selectbox("Cap Shape", options=["x", "b", "c", "f", "k", "s"])
        cap_surface = st.selectbox("Cap Surface", options=["f", "g", "y", "s"])
        cap_color = st.selectbox("Cap Color", options=["n", "b", "c", "g", "r", "p", "u", "e", "w", "y"])
        bruises = st.selectbox("Bruises?", options=["t", "f"])

    with col2:
        odor = st.selectbox("Odor", options=["p", "a", "l", "y", "f", "m", "n", "c", "s"])
        gill_size = st.selectbox("Gill Size", options=["n", "b"])
        gill_color = st.selectbox("Gill Color", options=["k", "n", "b", "h", "g", "r", "o", "p", "u", "e", "w", "y"])
        stalk_shape = st.selectbox("Stalk Shape", options=["e", "t"])


    submit = st.form_submit_button("Predict")


if submit:

    payload = {
        "cap_shape": cap_shape,
        "cap_surface": cap_surface,
        "cap_color": cap_color,
        "bruises": bruises,
        "odor": odor,
        "gill_size": gill_size,
        "gill_color": gill_color,
        "stalk_shape": stalk_shape
    }


    api_url = "http://127.0.0.1:8006/predict"

    try:
        with st.spinner('Analyzing...'):
            response = requests.post(
                api_url,
                json=payload,
                timeout=10
            )

        if response.status_code == 200:
            result = response.json()


            if result.get("result") == "p" or result.get("poisonous"):
                st.error(f"### Result: POISONOUS")
            else:
                st.success(f"### Result: EDIBLE")

            st.json(result)
        else:
            st.error(f"Server Error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Failed: Is your FastAPI running? \n({e})")