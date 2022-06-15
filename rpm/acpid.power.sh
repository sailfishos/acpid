#!/bin/sh

PATH=/sbin:/bin:/usr/bin

# Check that there is a power manager, otherwise shut down.
ps axo uid,cmd | \
awk '
    ($2 == "gnome-power-manager" || $2 == "/sbin/mce" || $2 == "kpowersave" || $2 == "xfce4-power-manager" || $2 ~ /meego-power-icon/ ) \
		{ found = 1; exit }
    END { exit !found }
' ||
  shutdown -h now

