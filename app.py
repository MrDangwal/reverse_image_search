import streamlit as st
from google_img_source_search import ReverseImageSearcher
import tempfile
import base64
import os

def save_uploaded_file(uploaded_file):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    return temp_file.name

def main():
    st.title("Reverse Image Search")

    # File uploader
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        tmp_path = save_uploaded_file(uploaded_file)

        # Convert the image file to base64
        with open(tmp_path, "rb") as img_file:
            image_data = base64.b64encode(img_file.read()).decode("utf-8")

        # Initialize ReverseImageSearcher
        rev_img_searcher = ReverseImageSearcher()

        # Search for similar images
        res = rev_img_searcher.search_by_image_data(image_data)

        # Display search results
        for search_item in res:
            st.write(f'Title: {search_item.page_title}')
            st.write(f'Site: {search_item.page_url}')
            st.write(f'Image: {search_item.image_url}\n')

if __name__ == '__main__':
    main()
