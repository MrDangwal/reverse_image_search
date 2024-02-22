import streamlit as st
import os
import uuid
import requests
from urllib.parse import quote
from google_img_source_search import ReverseImageSearcher
from pyngrok import ngrok

uid = uuid.uuid4()

def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    with open(os.path.join("uploads", f"{uid}.png"), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join("uploads", f"{uid}.png")

def start_ngrok_server(image_path):
    # Start ngrok tunnel
    public_url = ngrok.connect(addr="8000")
    return f"{public_url}/" + quote(os.path.basename(image_path))

def rev_im(image):
    out_list = []
    out_im = []
    html_out = ""
    
    # Save the uploaded image to disk
    tmp_path = save_uploaded_file(image)

    # Start ngrok server to host the image
    server_url = start_ngrok_server(tmp_path)

    rev_img_searcher = ReverseImageSearcher()
    try:
        res = rev_img_searcher.search(server_url)
    except RuntimeError as e:
        return str(e)

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

    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
        if st.button("Search"):
            result = rev_im(uploaded_image)
            st.markdown(result)

if __name__ == "__main__":
    main()
