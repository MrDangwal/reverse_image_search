from google_img_source_search import ReverseImageSearcher
import streamlit as st
import os
import uuid

uid = uuid.uuid4()

def main():
    st.title("Reverse Image Search")

    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        # Save the uploaded image to disk
        tmp_path = save_uploaded_file(uploaded_image)

        if tmp_path is not None:
            # Create a temporary URL for the uploaded image
            tmp_url = st.get_url(tmp_path)
            if tmp_url is not None:
                # Perform reverse image search
                rev_img_searcher = ReverseImageSearcher()
                try:
                    res = rev_img_searcher.search(tmp_url)
                    for search_item in res:
                        st.write(f'Title: {search_item.page_title}')
                        st.write(f'Site: {search_item.page_url}')
                        st.write(f'Img: {search_item.image_url}\n')
                except RuntimeError as e:
                    st.error(f"An unexpected error occurred while processing the image: {e}")

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Create the "uploads" directory if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        with open(os.path.join("uploads", f"{uid}.png"), "wb") as f:
            f.write(uploaded_file.getvalue())
        return os.path.join("uploads", f"{uid}.png")
    return None

if __name__ == "__main__":
    main()
