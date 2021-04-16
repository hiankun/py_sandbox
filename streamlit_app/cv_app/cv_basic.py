import streamlit as st
import numpy as np
import cv2

class CvFunc():
    def __init__(self):
        self.canny_lower = 100
        self.canny_upper = 200

    def cv_functions(self):
        show_edge = False
        cv_func = st.sidebar.radio(
                label="choose a method:",
                options=('rgb2gray', 'rgb2bgr', 'rgb2hsv')
                )
        if cv_func == 'rgb2gray':
            show_edge = st.sidebar.checkbox(label="show edge")
            if show_edge:
                self.canny_lower = st.sidebar.slider("lower: ", 0,255,100)
                self.canny_upper = st.sidebar.slider("upper: ", 0,255,200)
        return cv_func, show_edge

    def convert_img(self, cv_img, mode, show_edge):
        if mode == 'rgb2gray':
            converted_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
            if show_edge:
                converted_img = cv2.Canny(
                        converted_img, self.canny_lower, self.canny_upper)
        elif mode == 'rgb2bgr':
            converted_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        elif mode == 'rgb2hsv':
            converted_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2HSV)
        else:
            converted_img = cv_img
    
        return converted_img


def get_textfile_content(filepath):
    with open(filepath, mode='r') as f:
        content = f.read()
    return content

def description():
    content = get_textfile_content('./cv_basic.md')
    st.sidebar.markdown(content)

def init_settings():
    st.set_page_config(
            page_title="OpenCV test",
            page_icon="🤖",
            )

def get_cv_img(uploaded_file, img_mode=cv2.IMREAD_COLOR):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    _img = cv2.imdecode(file_bytes, img_mode)
    return cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)

def main():
    cvfunc = CvFunc()
    init_settings()
    description()

    input_file = st.file_uploader(
            label="upload an image",
            type=['png','jpg','jpeg']
            )

    cv_func, show_edge = cvfunc.cv_functions()

    converted_img = None
    if input_file:
        cv_img = get_cv_img(input_file)
        st.image(cv_img)#, channels="BGR")
        converted_img = cvfunc.convert_img(cv_img, cv_func, show_edge)

    if converted_img is not None:
        st.image(converted_img)


if __name__=='__main__':
    main()
