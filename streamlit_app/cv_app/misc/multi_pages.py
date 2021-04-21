# https://github.com/whitphx/streamlit-webrtc/blob/master/app.py
import streamlit as st
from pathlib import Path
from streamlit_webrtc import (
    ClientSettings,
    VideoTransformerBase,
    WebRtcMode,
    webrtc_streamer,
)

HERE = Path(__file__).parent

WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": True},
)

def app_video_filters():
    pass

def app_object_detection():
    pass

def app_streaming():
    """ Media streamings """
    MEDIAFILES = {
        "big_buck_bunny_720p_2mb.mp4": {
            "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_2mb.mp4",  # noqa: E501
            "local_file_path": HERE / "data/big_buck_bunny_720p_2mb.mp4",
            "type": "video",
        },
        "big_buck_bunny_720p_10mb.mp4": {
            "url": "https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_10mb.mp4",  # noqa: E501
            "local_file_path": HERE / "data/big_buck_bunny_720p_10mb.mp4",
            "type": "video",
        },
        "file_example_MP3_700KB.mp3": {
            "url": "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3",  # noqa: E501
            "local_file_path": HERE / "data/file_example_MP3_700KB.mp3",
            "type": "audio",
        },
        "file_example_MP3_5MG.mp3": {
            "url": "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_5MG.mp3",  # noqa: E501
            "local_file_path": HERE / "data/file_example_MP3_5MG.mp3",
            "type": "audio",
        },
    }
    media_file_label = st.radio(
        "Select a media file to stream", tuple(MEDIAFILES.keys())
    )
    media_file_info = MEDIAFILES[media_file_label]
    download_file(media_file_info["url"], media_file_info["local_file_path"])

    def create_player():
        return MediaPlayer(str(media_file_info["local_file_path"]))

        # NOTE: To stream the video from webcam, use the code below.
        # return MediaPlayer(
        #     "1:none",
        #     format="avfoundation",
        #     options={"framerate": "30", "video_size": "1280x720"},
        # )

    WEBRTC_CLIENT_SETTINGS.update(
        {
            "media_stream_constraints": {
                "video": media_file_info["type"] == "video",
                "audio": media_file_info["type"] == "audio",
            }
        }
    )

    webrtc_streamer(
        key=f"media-streaming-{media_file_label}",
        mode=WebRtcMode.RECVONLY,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        player_factory=create_player,
    )


def app_sendonly():
    pass

def app_loopback():
    """ Simple video loopback """
    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_transformer_factory=None,  # NoOp
    )

def main():
    st.header("WebRTC demo")

    object_detection_page = "Real time object detection (sendrecv)"
    video_filters_page = (
        "Real time video transform with simple OpenCV filters (sendrecv)"
    )
    streaming_page = (
        "Consuming media files on server-side and streaming it to browser (recvonly)"
    )
    sendonly_page = "WebRTC is sendonly and images are shown via st.image() (sendonly)"
    loopback_page = "Simple video loopback (sendrecv)"
    app_mode = st.sidebar.selectbox(
        label="Choose the app mode",
        options=[
            object_detection_page,
            video_filters_page,
            streaming_page,
            sendonly_page,
            loopback_page,
        ],
        index=4,
    )
    st.subheader(app_mode)

    if app_mode == video_filters_page:
        app_video_filters()
    elif app_mode == object_detection_page:
        app_object_detection()
    elif app_mode == streaming_page:
        app_streaming()
    elif app_mode == sendonly_page:
        app_sendonly()
    elif app_mode == loopback_page:
        app_loopback()


if __name__ == "__main__":
    main()
