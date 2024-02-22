import streamlit as st
import requests
import os
import uuid
from google_img_source_search import ReverseImageSearcher
from urllib.parse import quote

uid = uuid.uuid4()

def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        with open(os.path.join("uploads", f"{uid}.png"), "wb") as f:
            f.write(uploaded_file.getvalue())
        return os.path.abspath(os.path.join("uploads", f"{uid}.png"))
    return None

def rev_im(image):
    out_list = []
    out_im = []
    html_out = ""
    # Save the uploaded image to a temporary file
    tmp_path = save_uploaded_file(image)
    if tmp_path is None:
        return "No image uploaded."

    # Construct the URL with proper encoding
    out_url = f'https://{st.server.server_address[0]}:{st.server.port}/{quote(tmp_path)}'
    
    print("Output URL:", out_url)  # Debug statement
    
    rev_img_searcher = ReverseImageSearcher()
    try:
        res = rev_img_searcher.search(out_url)
    except Exception as e:
        print("Error:", e)  # Debug statement
        return f"An unexpected error occurred while processing the image. Error: {str(e)}"
    
    count = 0
    for search_item in res:
        count += 1
        out_dict = {
            'Title': f'{search_item.page_title}',
            'Site': f'{search_item.page_url}',
            'Img': f'{search_item.image_url}',
        }
        html_out = f"""{html_out}
        <div>
        Title: {search_item.page_title}<br>
        Site: <a href='{search_item.page_url}' target='_blank' rel='noopener noreferrer'>{search_item.page_url}</a><br>
        Img: <a href='{search_item.image_url}' target='_blank' rel='noopener noreferrer'>{search_item.image_url}</a><br>
        <img class='my_im' src='{search_item.image_url}'><br>
        </div>"""
    return f'Total Found: {count}\n{html_out}'

def main():
    st.title("Reverse Image Search")

    search_type = st.radio("Search Type", ["Image", "Video"])

    if search_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            if st.button("Search"):
                result = rev_im(uploaded_image)
                st.markdown(result)

if __name__ == "__main__":
    main()
