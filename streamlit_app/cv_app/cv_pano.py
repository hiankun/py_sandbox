import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageOps

class CvFunc():
    def __init__(self):
        pass

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

def description():
    content = get_textfile_content('./cv_pano.md')
    st.sidebar.markdown(content)
    st.sidebar.info(
            "This is a test.\n\n"
            "You need two '\\n' to start a new paragrpah.")

def init_settings():
    st.set_page_config(
            page_title='Panorama',
            page_icon='🌅',
            layout='wide',
            )

def get_cv_img(uploaded_file, img_mode=cv2.IMREAD_COLOR):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    _img = cv2.imdecode(file_bytes, img_mode)
    return cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)


@st.cache
def check_img_orientation(img_file_list, scale=None):
    """ Check the orientation of input images and try to correct it.
    The rotated images will be saved in the working folder.
    """
    _img_file_list = []
    for img_file in img_file_list:
        img = ImageOps.exif_transpose(
                Image.open(img_file))
        if scale:
            w,h = img.size
            img = img.resize((int(w*scale),int(h*scale)))
            print('xxxxxx', scale, (int(w*scale),int(h*scale)), img.size)
        img.save(img_file.name)
        _img_file_list.append(img_file.name)

    return _img_file_list

def main():
    cvfunc = CvFunc()
    init_settings()
    description()
    img_scale = st.sidebar.slider(
            label="Imag scale:", 
            min_value=0.1, 
            max_value=1.0, 
            value=1.0,
            step=0.1)

    input_file_list = st.file_uploader(
            label="Upload images",
            type=['png','jpg','jpeg'],
            accept_multiple_files=True
            )

    if input_file_list:
        local_img_list = check_img_orientation(input_file_list, img_scale)
        st.write("The uploaded/scaled images:")
        st.image(local_img_list, width=200)
        pano_img = cvfunc.get_panorama(local_img_list)
        if pano_img is not None:
            st.write(f"Result image:\nshape {pano_img.shape}")
            st.image(pano_img, channels='BGR')
            if st.button('Save'):
                cv2.imwrite('pano_res.png', pano_img)


if __name__=='__main__':
    main()
