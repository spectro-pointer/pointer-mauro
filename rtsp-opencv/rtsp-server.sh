:

raspivid -n -ih -t 0 -ISO 800 -ex night -w 720 -h 405 -fps 25 -b 200000 -o - | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/}' :demux=h264
