:

BASE="$HOME/work/quick2wire-python-api"

sudo apt-get install python3
sudo apt-get install python3-setuptools

sudo apt-get install python-pip
sudo apt-get install python-virtualenv

cd $BASE
sudo python3 setup.py install
cd - >/dev/null
