:

echo -n "Installing i2c libraries..."
./i2clibraries_install.sh
echo "done."

echo -n "Installing quick2wire api..."
./quick2wire_install.sh
echo "done."

echo -n "Probing kernel modules..."
sudo modprobe i2c-bcm2708
sudo modprobe i2c-dev
echo "done."

echo -n "Configurin kernel modules loading at boot..."
sudo sh -c "echo i2c-bcm2708 >>/etc/modules"
sudo sh -c "echo i2c-dev >>/etc/modules"
echo "done."
