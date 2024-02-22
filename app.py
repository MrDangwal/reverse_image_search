import streamlit as st
import requests
import imageio
from google_img_source_search import ReverseImageSearcher
import os
import uuid

uid = uuid.uuid4()

def rev_im(image_path):
    out_list = []
    out_im = []
    html_out = ""
    # Read image using imageio
    image = imageio.imread(image_path)
    # Write image to temporary file
    tmp_path = f"{uid}-im_tmp.png"
    imageio.imwrite(tmp_path, image)
    out_url = f'https://omnibus-reverse-image.hf.space/file={os.path.abspath(tmp_path)}'
    rev_img_searcher = ReverseImageSearcher()
    try:
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
    except ValueError:
        return "Error: Unable to extract image information. Please try again with a different image."

def main():
    st.title("Reverse Image Search")

    search_type = st.radio("Search Type", ["Image", "Video"])

    if search_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            if st.button("Search"):
                # Save the uploaded image to disk
                with open(f"{uid}.png", "wb") as f:
                    f.write(uploaded_image.getvalue())
                result = rev_im(f"{uid}.png")
                st.markdown(result)

if __name__ == "__main__":
    main()
