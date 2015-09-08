#!/bin/bash

# OpenCV installation for Ubuntu 12.04
# To install OpenCV 2.4.x on Ubuntu 12.04, first install
# a developer environment to build OpenCV.
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
#sudo apt-get -y install libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev 
sudo apt-get -y install libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev 

# install the Python development environment and the Python Numerical library
sudo apt-get -y install python-dev python-numpy
 
# Optional - install the parallel code processing library (the Intel tbb library)
sudo apt-get -y install libtbb-dev

# install the Qt dev library
sudo apt-get -y install libqt4-dev

# Now download OpenCV 2.4 to wherever you want to compile the source
cd ~/src
sudo wget -c "http://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.9/opencv-2.4.9.zip"
sudo chown $USER opencv-2.4.*.zip
sudo unzip opencv-2.4.*.zip
sudo chown -R $USER opencv-2.4.*/

# Create and build directory and onfigure OpenCV with cmake.
cd opencv-2.4.*
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D WITH_V4L=ON \
    -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=ON -D WITH_QT=ON -D WITH_OPENGL=ON ..

# Compile it
make

# And finally, install OpenCV
sudo make install
