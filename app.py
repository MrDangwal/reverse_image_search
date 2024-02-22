import streamlit as st
import os
from google_img_source_search import ReverseImageSearcher

def rev_im(image_path):
    rev_img_searcher = ReverseImageSearcher()
    try:
        res = rev_img_searcher.search(image_path)
        for search_item in res:
            st.write(f'Title: {search_item.page_title}')
            st.write(f'Site: {search_item.page_url}')
            st.image(search_item.image_url, caption='Image')
    except RuntimeError as e:
        st.error(f"An unexpected error occurred while processing the image: {e}")

def main():
    st.title("Reverse Image Search")

    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        # Save the uploaded image to a temporary location
        with open("temp_image.png", "wb") as f:
            f.write(uploaded_image.getvalue())
        # Get the absolute path of the uploaded image
        image_path = os.path.abspath("temp_image.png")
        rev_im(image_path)

if __name__ == "__main__":
    main()
