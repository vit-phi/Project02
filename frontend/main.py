import requests
import streamlit as st
from PIL import Image

STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the wave": "the_wave",
    "udnie": "udnie",
}

#st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Style Transfer Web App")

# displays a file uploader widget
image = st.file_uploader("Choose an image")

# displays the select widget for the styles
style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

# displays a button
if st.button("Style Transfer"):
    if image is not None and style is not None:
        files = {"file": image.getvalue()}
        try:
            # Send POST request to the backend
            res = requests.post(f"http://backend:8080/{style}", files=files)
            
            # Print the raw response to debug
            st.write(f"Raw response from API: {res.text}")
            
            # Check if the status code is 200 (OK)
            if res.status_code == 200:
                try:
                    # Try to parse JSON response
                    img_path = res.json()
                    st.write(f"Parsed response: {img_path}")  # Print parsed response to debug
                    img_name = img_path.get("name")
                    
                    if img_name is not None:
                        image = Image.open(img_name)  # Open the image file from the path returned
                        st.image(image, width=500)
                    else:
                        st.error("Received empty 'name' from the backend API.")
                except requests.exceptions.JSONDecodeError:
                    st.error("API response is not in valid JSON format.")
                    st.text(f"Response content: {res.text}")
            else:
                st.error(f"Error: API returned status code {res.status_code}")
                st.text(f"Response content: {res.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {str(e)}")
