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

