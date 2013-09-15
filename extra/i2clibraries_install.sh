:

BASE="$HOME/work/i2clibraries"
INSTALL="/usr/local/lib/python3.2/dist-packages/i2clibraries"

sudo mkdir -p $INSTALL
sudo cp -a $BASE/*.py $INSTALL
