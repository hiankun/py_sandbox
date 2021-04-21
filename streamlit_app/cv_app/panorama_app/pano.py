import streamlit as st
import numpy as np
import cv2
from time import time
from datetime import datetime
from PIL import Image, ImageOps

class ProcBase():
    def __init__(self, mode=None):
        if mode == 'pano':
            self.scale = st.sidebar.slider(
                label="Downscale ratio:", 
                min_value=0.1, 
                max_value=1.0, 
                value=0.1,
                step=0.1,
                help="Use smaller ratio to get result quickly.",
                )
        self.save_path = st.sidebar.text_input(
                label="Save files to:",
                value="./saved_files",
                help="Set your path to save the processed files.",
                )


    def check_img_orientation(self, img_file_list):
        """ Check the orientation of input images and try to correct it.
        The rotated images will be saved in the working folder.
        """
        _img_file_list = []
        for img_file in img_file_list:
            try:
                img = ImageOps.exif_transpose(
                    Image.open(img_file))
            except:
                img = Image.open(img_file)
            if self.scale:
                w,h = img.size
                img = img.resize((int(w*self.scale),int(h*self.scale)))
            img.save(img_file.name)
            _img_file_list.append(img_file.name)

        return _img_file_list


class CvFunc(ProcBase):
    def __init__(self, mode=None):
        super().__init__(mode)

    #@st.cache
    def get_panorama(self, img_files):
        images = []
        for filename in img_files:
            img = cv2.imread(filename)
            images.append(img)
        
        stitcher = cv2.Stitcher.create()
        _, res = stitcher.stitch(images)
        return res


def get_textfile_content(filepath):
    with open(filepath, mode='r') as f:
        content = f.read()
    return content

def temp_note():
    st.sidebar.markdown(
            """
# TODO

* saving files path
* remove temp saved images
* click and drawing functions
* GIS ([GeoPandas](https://geopandas.readthedocs.io/en/latest/))
    """)

def init_settings():
    st.set_page_config(
            page_title='Panorama',
            page_icon='🌅',
            layout='wide',
            )

def sidebar_ui(content_file):
    content = get_textfile_content(content_file)
    st.sidebar.markdown(content)
    st.sidebar.markdown('# Control panel')

def get_cv_img(uploaded_file, img_mode=cv2.IMREAD_COLOR):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    _img = cv2.imdecode(file_bytes, img_mode)
    return cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)


def app_pano():
    sidebar_ui('./pano.md')
    cvfunc = CvFunc(mode='pano')

    input_file_list = st.file_uploader(
            label="Upload images",
            type=['png','jpg','jpeg'],
            accept_multiple_files=True
            )

    if input_file_list:
        local_img_list = cvfunc.check_img_orientation(input_file_list)
        st.info(f"Input images")
        st.image(local_img_list, width=200)

        _process_time = time()
        with st.spinner(text='Processing...'):
            pano_img = cvfunc.get_panorama(local_img_list)
        process_time = time() - _process_time

        if pano_img is not None:
            st.success(f"Panorama | "
            f"Size {pano_img.shape[1]}x{pano_img.shape[0]} | "
            f"Processing time: {process_time:.2f} sec")
            st.image(pano_img, channels='BGR')
            if st.button('Save'):
                timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
                file2save = f'pano_res-{timestamp}.jpg'
                cv2.imwrite(f'{file2save}', pano_img)
                st.write(f'{file2save} has been saved.')
        else:
            st.error("Stitch failed.")

def app_ortho():
    sidebar_ui('./pano.md')
    cvfunc = CvFunc(mode='ortho')

    input_file_list = st.file_uploader(
            label="Upload panorama",
            type=['png','jpg','jpeg'],
            accept_multiple_files=False
            )
    if input_file_list:
        st.info(f"Panorama")
        st.image(input_file_list )

    st.write("under construction...")

#@st.cache
def main():
    init_settings() #NOTE: must be first
    temp_note()

    # Set the pages
    st.header("Fish Pond App")
    pano_page = "Input images to panorama"
    ortho_page = "Panorama to orthophoto"
    app_mode = st.sidebar.selectbox(
        label="Choose app mode",
        options=[
            pano_page,
            ortho_page,
        ],
        index=0,
    )
    st.subheader(app_mode)

    if app_mode == pano_page:
        app_pano()
    elif app_mode == ortho_page:
        app_ortho()


if __name__=='__main__':
    main()
