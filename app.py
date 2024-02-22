import streamlit as st
from google_img_source_search import ReverseImageSearcher
from PIL import Image
import os
import uuid

uid = uuid.uuid4()

def process_vid(file, cur_frame, every_n):
    new_video_in = str(file)
    capture = cv2.VideoCapture(new_video_in)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    rev_img_searcher = ReverseImageSearcher()
    html_out = ""
    count = int(every_n)
    if cur_frame == "" or cur_frame is None:
        start_frame = 0
    elif cur_frame != "" and cur_frame is not None:
        start_frame = int(cur_frame)
    try:
        for i in range(start_frame, frame_count - 1):
            if count == int(every_n):
                count = 1
                print(i)
                capture.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame_f = capture.read(i)
                cv2.imwrite(f"{uid}-vid_tmp{i}.png", frame_f)
                frame_path = f"{uid}-vid_tmp{i}.png"
                out_url = f'https://omnibus-reverse-image.hf.space/file={frame_path}'
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

def rev_im(image):
    try:
        out_list = []
        out_im = []
        html_out = ""
        with Image.open(image) as img:
            img.save(f"{uid}-im_tmp.png")
            out = os.path.abspath(f"{uid}-im_tmp.png")
            out_url = f'https://omnibus-reverse-image.hf.space/file={out}'
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
            raise RuntimeError('No images found in the search results.')
        return (f'Total Found: {count}\n{html_out}')
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")

def main():
    st.title("Reverse Image/Video Search")

    search_type = st.radio("Search Type", ["Image", "Video"])

    if search_type == "Image":
        uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            if st.button("Search"):
                result = rev_im(uploaded_image)
                if result:
                    st.markdown(result)

    elif search_type == "Video":
        video_url = st.text_input("Enter Video URL")
        every_n = st.number_input("Every /nth frame", value=10)
        if st.button("Search"):
            # Your video download logic here
            result = 'path_to_video.mp4'  # Assuming path to video
            if result is not None:
                video_path = result
                vid_file = open(video_path, 'rb')
                vid_bytes = vid_file.read()
                st.video(vid_bytes, format='video/mp4')

                cur_frame = st.text_input("Enter Current Frame")
                if st.button("Start"):
                    status, _, _ = process_vid(video_path, cur_frame, every_n)
                    st.markdown(status)

if __name__ == "__main__":
    main()
