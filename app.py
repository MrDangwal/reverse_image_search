import streamlit as st
import os
import uuid
from google_img_source_search import ReverseImageSearcher
from urllib.parse import quote

uid = uuid.uuid4()

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Create the "uploads" directory if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        with open(os.path.join("uploads", f"{uid}.png"), "wb") as f:
            f.write(uploaded_file.getvalue())
        return os.path.abspath(os.path.join("uploads", f"{uid}.png"))
    return None

def rev_im(uploaded_image):
    tmp_path = save_uploaded_file(uploaded_image)
    if tmp_path is not None:
        # Construct the URL for the uploaded image
        local_url = f"http://localhost:8501/files/{tmp_path}"
        
        rev_img_searcher = ReverseImageSearcher()
        try:
            res = rev_img_searcher.search(local_url)
            count = 0
            html_out = ""
            for search_item in res:
                count += 1
                html_out += f"""<div>
                    Title: {search_item.page_title}<br>
                    Site: <a href='{search_item.page_url}' target='_blank' rel='noopener noreferrer'>{search_item.page_url}</a><br>
                    Img: <a href='{search_item.image_url}' target='_blank' rel='noopener noreferrer'>{search_item.image_url}</a><br>
                    <img class='my_im' src='{search_item.image_url}'><br>
                </div>"""
            
            st.markdown(f'Total Found: {count}\n{html_out}')
        except RuntimeError as e:
            st.error(f"An unexpected error occurred while processing the image: {e}")

def main():
    st.title("Reverse Image Search")

    search_type = st.radio("Search Type", ["Image", "Video"])

    if search_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            if st.button("Search"):
                rev_im(uploaded_image)

if __name__ == "__main__":
    main()
