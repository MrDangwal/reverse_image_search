import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from google_img_source_search import ReverseImageSearcher
import pylocaltunnel

# Function to save the uploaded file
def save_uploaded_file(uploaded_file):
    uid = st.session_state.session_id
    with open(f"uploads/{uid}.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    return f"uploads/{uid}.png"

# Function to start a local server using pylocaltunnel
def start_localtunnel_server(port):
    tunnel = pylocaltunnel.Tunnel(port)
    public_url = tunnel.start()
    return public_url

# Main function
def main():
    st.title("Reverse Image Search")

    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

        # Save the uploaded file
        tmp_path = save_uploaded_file(uploaded_image)

        # Start localtunnel server
        server_url = start_localtunnel_server(8000)

        # Perform reverse image search
        rev_img_searcher = ReverseImageSearcher()
        res = rev_img_searcher.search(server_url)

        # Display search results
        st.subheader("Search Results:")
        for search_item in res:
            st.write(f'Title: {search_item.page_title}')
            st.write(f'Site: {search_item.page_url}')
            st.image(search_item.image_url, caption="Image", use_column_width=True)

# Run the main function
if __name__ == "__main__":
    main()
