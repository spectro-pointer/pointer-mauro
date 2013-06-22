#!/bin/bash
# Takes a fram from the Quickcam Express webcam to identify North in the Compass

# start webcam
#modprobe quickcam

mkdir -p $BASE/capture

X=119
Y=174

while true
do
	date
	#TS=`date +%s`
	vgrabbj -U -R -o png -f $BASE/capture/latest.png 2>/dev/null
	# pressure
	convert $BASE/capture/latest.png -crop 35x14+$[X+65]+$Y $BASE/capture/latest-pcrop.png
	convert $BASE/capture/latest-pcrop.png -normalize $BASE/capture/latest-pnorm.png
	# temp
	convert $BASE/capture/latest.png -crop 35x14+$X+$Y $BASE/capture/latest-tcrop.png
	convert $BASE/capture/latest-tcrop.png -normalize $BASE/capture/latest-tnorm.png

	# seven segment ocr pressure
	for T in `seq 1 $T1 $T2`; do ssocr -d 3 -a -t $T closing shear 1 grayscale $BASE/capture/latest-pnorm.png; done 2>/dev/null | sort | uniq -c >$BASE/capture/latest-p.txt

	# seven segment ocr temperature
	for T in `seq 1 $T1 $T2`; do ssocr -d 3 -a -t $T closing shear 1 grayscale $BASE/capture/latest-tnorm.png; done 2>/dev/null | sort | uniq -c >$BASE/capture/latest-t.txt

	scp $BASE/capture/latest* root@xxiv:/var/www/shnoll/capture >/dev/null

	# get pressure value
	MB=`egrep '9[0-9]{2}$' $BASE/capture/latest-p.txt | sort -nk1 -nrk2 | tail -1 | awk '{print $2}'`
	[ -z "$MB" ] && MB=0
	echo "$MB mb"

	# get temperature value
	C=`egrep '[0-9]{3}$' $BASE/capture/latest-t.txt | sort -nk1 | tail -1 | awk '{print $2}'`
	[ -z "$C" ] && C=0
	if [ $C -gt 10 -a $C -lt 500 ]
	then
		C=`echo scale=1\; $C / 10 | bc -l`
		mysql -u$US -p$PASS $DB <<EOF
INSERT INTO \`temp\` (\`c\`, \`duration\`, \`interval\`, \`source\`) VALUES ('$C', '$DURATION', '$INTERVAL', 'clock');
EOF
	fi
	echo "$C ºC"

	if [ $MB -gt 800 ]
	then
	mysql -u$US -p$PASS $DB <<EOF
INSERT INTO \`pressure\` (\`mb\`, \`duration\`, \`interval\`) VALUES ('$MB', '$DURATION', '$INTERVAL');
EOF
	fi

	sleep $[DURATION - 2]
	sleep $[INTERVAL * 60]
done
