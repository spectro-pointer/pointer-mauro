:

IP="pi"

gst-launch-1.0 -v tcpclientsrc host=$IP port=5000 !gdpdepay ! rtph264depay !h264parse ! omxh264dec ! videoconvert !autovideosink sync=false
