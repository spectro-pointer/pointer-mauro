:

A=16/9
W=1024
H=576
#raspivid -n -ih -t 0 -ISO 800 -ex night -w $W -h $H -fps 25 -b 1000000 -o - | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
raspivid -n -ih -t 0 -ISO 100 -w $W -h $H -fps 25 -b 100000 -o - | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
