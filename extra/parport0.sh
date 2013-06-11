#!/bin/bash

ID=`id -u`
[ $ID -ne 0 ] && echo "Needs root." && exit 1

P=/dev/parport0

echo -n "Installing device..."
mknod $P c 99 0
chgrp lp $P
chmod g+rw $P
echo "done."
echo "Make sure user '$SUDO_USER' is in group 'lp'."
