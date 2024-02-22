import streamlit as st
from google_img_source_search import ReverseImageSearcher
from PIL import Image
import os 
import uuid

uid = uuid.uuid4()

def rev_im(image):
    out_list = []
    out_im = []
    html_out = ""
    image = Image.open(image)
    image.save(f"{uid}-im_tmp.png")
    out_url = f'https://omnibus-reverse-image.hf.space/file={uid}-im_tmp.png'
    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(out_url)
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
