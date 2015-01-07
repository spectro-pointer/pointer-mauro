:

#S="subkeys.pgp.net"
S="keyserver.ubuntu.com"

MACHINE=`uname -m`

if [ "$MACHINE" = "armv6l" ]
then
	# pi gstreamer 1.0 runtime
	K="F0DAA5410C667A3E"
	gpg --keyserver $S --recv-keys $K && gpg --export $K | apt-key add -
	sudo sh -c "echo 'deb http://vontaene.de/raspbian-updates/ . main' >/etc/apt/sources.list.d/gstreamer.list"
	sudo apt-get update
	sudo apt-get install -y --force-yes gstreamer1.0
else # Ubuntu
	# gstreamer runtime
	sudo apt-get install -y gstreamer1.0-libav gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-good gstreamer1.0-tools
fi
