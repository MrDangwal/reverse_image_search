import streamlit as st
from google_img_source_search import ReverseImageSearcher
from PIL import Image
import os 
import uuid

uid = uuid.uuid4()

def rev_im(image):
    try:
        out_list = []
        out_im = []
        html_out = ""
        # Convert uploaded file to PIL image
        pil_image = Image.open(image)
        # Save the PIL image to a temporary file
        temp_image_path = f"{uid}-im_tmp.png"
        pil_image.save(temp_image_path)
        # Construct the image URL
        out_url = f'https://omnibus-reverse-image.hf.space/file={temp_image_path}'
        # Perform reverse image search
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
        if count == 0:
            return f'No matching images found.'
        else:
            return f'Total Found: {count}\n{html_out}'
    except Exception as e:
        # Catch any exceptions and return an error message
        print(f"Error processing image: {e}")
        return f'An unexpected error occurred while processing the image.'

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
