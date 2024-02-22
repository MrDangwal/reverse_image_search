import streamlit as st
from google_img_source_search import ReverseImageSearcher
from PIL import Image
import io
import os

# Function to save the uploaded file and return the local file path
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded file
        with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Return the local file path
        return os.path.abspath(os.path.join("uploads", uploaded_file.name))
    return None

# Main function to perform reverse image search
def rev_im(image):
    # Initialize Google Image Source Search
    rev_img_searcher = ReverseImageSearcher()
    
    try:
        # Perform reverse image search
        res = rev_img_searcher.search(image)
        # Print search results
        for search_item in res:
            st.write(f'Title: {search_item.page_title}')
            st.write(f'Site: {search_item.page_url}')
            st.image(search_item.image_url, caption='Image')

    except Exception as e:
        st.error(f"An unexpected error occurred while processing the image: {e}")

def main():
    st.title("Reverse Image Search")

    # File uploader for uploading the image
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(image, caption='Uploaded Image')

        # Save the uploaded file and get the local file path
        file_path = save_uploaded_file(uploaded_file)
        if file_path is not None:
            # Perform reverse image search using the local file path
            rev_im(file_path)

if __name__ == "__main__":
    main()
