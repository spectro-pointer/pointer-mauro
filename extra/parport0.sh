#!/bin/bash

P=/dev/parport0

echo -n "Installing device..."
sudo mknod $P c 99 0
sudo chgrp lp $P
sudo chmod g+rw $P
echo "done."
echo "Make sure user '$USER' is in group 'lp'."
