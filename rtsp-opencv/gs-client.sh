:

IP="pi"
#H264_DEC="omxh264dec" # rpi H.264 decoder
H264_DEC="avdec_h264"

gst-launch-1.0 -v tcpclientsrc host=$IP port=5000 ! gdpdepay ! rtph264depay !h264parse ! $H264_DEC ! videoconvert !autovideosink sync=false
