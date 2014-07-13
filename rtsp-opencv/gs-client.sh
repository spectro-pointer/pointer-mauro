:

gst-launch-1.0 -v tcpclientsrc host= 192.168.2.100 port=5000 !gdpdepay ! rtph264depay !h264parse ! omxh264dec ! videoconvert !autovideosink sync=false
