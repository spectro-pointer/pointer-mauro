:

IP="pi"

#H264_DEC="omxh264dec" # Rpi (HW accelerated) H.264 decoder

#GSV=0.10
#H264_DEC="ffdec_h264" # gstreamer 0.10 H2.64 ffmpeg decoder (gstreamer0.10-ffmpeg)

GSV=1.0
H264_DEC="h264parse ! avdec_h264 ! videoconvert" # gstreamer 1.0 H.264 decoder pipeline

gst-launch-$GSV -v tcpclientsrc host=$IP port=5000 ! gdpdepay ! rtph264depay ! $H264_DEC ! autovideosink sync=false
