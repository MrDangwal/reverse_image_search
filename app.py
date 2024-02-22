import streamlit as st
import requests
import yt_dlp
from google_img_source_search import ReverseImageSearcher
from PIL import Image
import os
import uuid

uid = uuid.uuid4()

def dl(inp):
    out = None
    out_file = []
    try:
        inp_out = inp.replace("https://", "")
        inp_out = inp_out.replace("/", "_").replace(".", "_").replace("=", "_").replace("?", "_")
        if "twitter" in inp:
            os.system(f'yt-dlp "{inp}" --extractor-arg "twitter:api=syndication" --trim-filenames 160 -o "{uid}/{inp_out}.mp4" -S res,mp4 --recode mp4')
        else:
            os.system(f'yt-dlp "{inp}" --trim-filenames 160 -o "{uid}/{inp_out}.mp4" -S res,mp4 --recode mp4')

        out = f"{uid}/{inp_out}.mp4"
        print(out)
    except Exception as e:
        print(e)
    return out, "", "", ""

def process_vid(file, cur_frame, every_n):
    new_video_in = str(file)
    capture = cv2.VideoCapture(new_video_in)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    rev_img_searcher = ReverseImageSearcher()
    html_out = ""
    count = int(every_n)
    if cur_frame == "" or cur_frame == None:
        start_frame = 0
    elif cur_frame != "" and cur_frame != None:
        start_frame = int(cur_frame)
    try:
        for i in range(start_frame, frame_count - 1):
            if count == int(every_n):
                count = 1
                print(i)
                capture.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame_f = capture.read(i)
                cv2.imwrite(f"{uid}-vid_tmp{i}.png", frame_f)
                out = os.path.abspath(f"{uid}-vid_tmp{i}.png")
                out_url = f'https://omnibus-reverse-image.hf.space/file={out}'
                print(out)
                res = rev_img_searcher.search(out_url)
                out_cnt = 0
                if len(res) > 0:
                    for search_item in res:
                        out_cnt += 1
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
                    return (f'Total Found: {out_cnt}\n{html_out}', f"Found frame: {i}", i + int(every_n))
            count += 1
    except Exception as e:
        return (f'{e}', "", "")
    return ('No frame matches found.', "", "")

def rev_im(uploaded_image):
    try:
        # Check if uploaded_image is not None and is of type 'UploadedFile'
        if uploaded_image is not None and isinstance(uploaded_image, UploadedFile):
            # Open the uploaded image using PIL
            with Image.open(uploaded_image) as img:
                # Save the image to a temporary file
                tmp_image_path = f"{uid}-im_tmp.png"
                img.save(tmp_image_path)

            # Perform reverse image search using the temporary image file
            return perform_reverse_image_search(tmp_image_path)
        else:
            return ('Invalid image file', 'Please upload a valid image file', '')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ('An unexpected error occurred.', str(e), '')

def perform_reverse_image_search(image_path):
    try:
        out_list = []
        out_im = []
        html_out = ""
        
        # Generate URL for the temporary image file
        out_url = f'https://omnibus-reverse-image.hf.space/file={image_path}'
        print(f"Searching reverse image with URL: {out_url}")
        
        # Perform reverse image search
        rev_img_searcher = ReverseImageSearcher()
        res = rev_img_searcher.search(out_url)
        
        # Process search results
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
        print(f"An unexpected error occurred: {e}")
        return ('An unexpected error occurred.', str(e), '')

def main():
    st.title("Reverse Image/Video Search")

    search_type = st.radio("Search Type", ["Image", "Video"])

    if search_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            if st.button("Search"):
                result = rev_im(uploaded_image)
                st.markdown(result)

    elif search_type == "Video":
        video_url = st.text_input("Enter Video URL")
        every_n = st.number_input("Every /nth frame", value=10)
        if st.button("Search"):
            result = dl(video_url)
            if result is not None:
                video_path, _, _, _ = result
                vid_file = open(video_path, 'rb')
                vid_bytes = vid_file.read()
                st.video(vid_bytes, format='video/mp4')

                cur_frame = st.text_input("Enter Current Frame")
                if st.button("Start"):
                    status, _, _ = process_vid(video_path, cur_frame, every_n)
                    st.markdown(status)

if __name__ == "__main__":
    main()
