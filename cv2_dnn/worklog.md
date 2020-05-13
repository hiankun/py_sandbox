# Test on RPi4 (buster)

__NOTE__: Disable OpenVINO before the installation.

```
sudo apt install libjasper-dev
sudo apt install libqtgui4 
sudo apt install libqt4-test
sudo apt install libatlas-base-dev 
pip3 install opencv-python
>>> (maybe not necessary) pip3 install opencv-contrib-python==4.1.1.26
sudo apt install libhdf5-dev 
```

error:
```
ImportError: /home/pi/.local/lib/python3.7/site-packages/cv2/cv2.cpython-37m-arm-linux-gnueabihf.so: undefined symbol: __atomic_fetch_add_8
```

solution:
In `~/.bashrc`, add the following line:
```
export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0
```

# TODO

* Install headless version of Buster and OpenCV.
* Try YOLOv3.

# Install OpenCV with GPU functions

* Follow the instruction of [How to use OpenCV’s “dnn” module with NVIDIA GPUs, CUDA, and cuDNN](
https://www.pyimagesearch.com/2020/02/03/how-to-use-opencvs-dnn-module-with-nvidia-gpus-cuda-and-cudnn/)
  * Download to `~/Documents/opencv/` and `~/Documents/opencv_contrib/`.
  * Try to install in conda enviroment but cannot find the installed lib.
  * Download cuDNN deb packages (runtime, dev, and doc) and install them using `sudo dpkg -i *.deb`.
  * Finally install it without using virtual enviroments.
  * The cmake commands are:
    ```
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
            -D CMAKE_INSTALL_PREFIX=/usr/local \
            -D INSTALL_PYTHON_EXAMPLES=ON \
            -D INSTALL_C_EXAMPLES=OFF \
            -D OPENCV_ENABLE_NONFREE=ON \
            -D WITH_CUDA=ON \
            -D WITH_CUDNN=ON \
            -D OPENCV_DNN_CUDA=ON \
            -D ENABLE_FAST_MATH=1 \
            -D CUDA_FAST_MATH=1 \
            -D CUDA_ARCH_BIN=6.1 \
            -D WITH_CUBLAS=1 \
            -D OPENCV_EXTRA_MODULES_PATH=/home/thk/Documents/opencv_contrib/modules \
            -D HAVE_opencv_python3=ON \
            -D BUILD_EXAMPLES=ON ..
    ```
* The final lib is in:
  `/usr/local/lib/python3.6/dist-packages/cv2/python-3.6`
