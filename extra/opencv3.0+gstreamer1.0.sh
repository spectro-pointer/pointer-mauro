:

# OpenCV installation for Ubuntu 12.04
# Installs OpenCV 3.0 on Ubuntu 12.04
# First install a developer environment to build OpenCV.
sudo apt-get -y install build-essential cmake pkg-config

# Install Image I/O libraries
sudo apt-get -y install libjpeg62-dev 
sudo apt-get -y install libtiff4-dev libjasper-dev

# Install the GTK dev library
sudo apt-get -y install  libgtk2.0-dev

# Install Video I/O libraries
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

# Optional - install support for Firewire video cameras
#sudo apt-get -y install libdc1394-22-dev

# Install video streaming libraries
sudo apt-get -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev 

# install the Python development environment and the Python Numerical library
sudo apt-get -y install python-dev python-numpy
 
# Optional - install the parallel code processing library (the Intel tbb library)
sudo apt-get -y install libtbb-dev

# install the Qt dev library
sudo apt-get -y install libqt4-dev

# Now download OpenCV 3.0 to wherever you want to compile the source
cd ~/src
sudo rm -rf opencv
sudo mkdir opencv
sudo chown $SUDO_USER opencv
git clone git://github.com/Itseez/opencv.git

# Create and build directory and onfigure OpenCV with cmake.
cd opencv
mkdir build
cd build
cmake \
    -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON \
    -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF -D WITH_QT=ON -D WITH_OPENGL=ON \
    -D BUILD_PERF_TESTS=OFF .. # Due to broken CUDA performance tests

# Compile it
make

# And finally, install OpenCV
sudo make install
