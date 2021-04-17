[2021-04-18]

# Setup conda env

* The following steps to avoid confliction between libraries:
    ```
    conda create -n streamlit_env
    conda activate streamlit_env
    conda install -c conda-forge streamlit opencv geopandas matplotlib
    pip install streamlit-webrtc
    ```
