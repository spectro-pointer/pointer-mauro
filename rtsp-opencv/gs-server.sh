:

#IFACE="eth0"
IFACE="wlan0"
IP=`ifconfig $IFACE | grep inet | awk '{print $2}' | cut -f2 -d:`

W=1080
H=720
FPS=25

#raspivid -t 0 -h $H -w $W -fps $FPS -b 200000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=$IP port=5000 
raspivid -n -ih -t 0 -ISO 800 -ex night -h $H -w $W -fps $FPS -b 200000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=$IP port=5000
