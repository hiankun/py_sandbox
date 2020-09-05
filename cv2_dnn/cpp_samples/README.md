* For OpenCV 4.x, `pkg-config` support has to be turned on when installation.
  * ref: https://github.com/opencv/opencv/issues/13154
  * Usage:
    ```
    -DOPENCV_GENERATE_PKGCONFIG=ON
    -DOPENCV_PC_FILE_NAME=opencv4.pc 
    ```
* Use CMake to compile the source code.
  (see `src/CMakeLists.txt`)
