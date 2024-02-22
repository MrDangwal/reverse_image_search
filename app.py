import streamlit as st
from google_img_source_search import ReverseImageSearcher

def main():
    st.title("Reverse Image Search")

    # File uploader for image
    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        # Perform reverse image search
        result = rev_im(uploaded_image)
        st.write(result)

def rev_im(image_data):
    # Perform reverse image search using the uploaded image data
    rev_img_searcher = ReverseImageSearcher()
    res = rev_img_searcher.search(image_data)

    # Process the search results
    search_results = []
    for search_item in res:
        search_results.append({
            "Title": search_item.page_title,
            "Site": search_item.page_url,
            "Image": search_item.image_url
        })

    return search_results

if __name__ == "__main__":
    main()
