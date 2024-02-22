import streamlit as st
import requests
import os
import uuid
import http.server
import socketserver
from threading import Thread
from urllib.parse import quote
import socket

from google_img_source_search import ReverseImageSearcher

uid = uuid.uuid4()

def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    with open(os.path.join("uploads", f"{uid}.png"), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join("uploads", f"{uid}.png")

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def start_http_server(image_path):
    # Change to the directory containing the image
    os.chdir(os.path.dirname(image_path))
    
    # Start a simple HTTP server on a random available port
    port = get_free_port()
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    
    thread = Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    return f'http://localhost:{port}/{quote(os.path.basename(image_path))}'

def rev_im(image):
    out_list = []
    out_im = []
    html_out = ""
    
    # Save the uploaded image to disk
    tmp_path = save_uploaded_file(image)

    # Start a simple HTTP server to serve the image
    server_url = start_http_server(tmp_path)

    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(server_url)

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
