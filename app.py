import streamlit as st
from google_img_source_search import ReverseImageSearcher
import uuid

uid = uuid.uuid4()

def rev_im(image):
    out_list = []
    out_im = []
    html_out = ""
    
    # Use google-image-source-search to perform reverse image search
    rev_img_searcher = ReverseImageSearcher()
    
    try:
        # Search for the provided image URL
        res = rev_img_searcher.search(image)
        
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
        
        return (f'Total Found: {count}\n{html_out}')
    
    except Exception as e:
        return (f'An unexpected error occurred: {e}', '', '')

def main():
    st.title("Reverse Image/Video Search")

    search_type = st.radio("Search Type", ["Image", "Video"])

    if search_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            if st.button("Search"):
                # Get the image URL from the uploaded file
                image_url = uploaded_image.url if hasattr(uploaded_image, 'url') else None
                if image_url:
                    result = rev_im(image_url)
                    st.markdown(result)

if __name__ == "__main__":
    main()
