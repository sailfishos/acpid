#!/bin/sh

PATH=/sbin:/bin:/usr/bin

grep -q open /proc/acpi/button/lid/*/state
if [ $? == 0 ]; then
	exit
fi
if [ "`who -r | awk '{print $2}'`" == "0" ]; then
	exit
fi

# Get the ID of the first active X11 session:
uid_session=$(
ck-list-sessions | \
awk '
/^Session[0-9]+:$/ { uid = active = x11 = "" ; next }
{ gsub(/'\''/, "", $3) }
$1 == "unix-user" { uid = $3 }
$1 == "active" { active = $3 }
$1 == "x11-display" { x11 = $3 }
active == "TRUE" && x11 != "" {
	print uid
	exit
}')

# Check that there is a power manager, otherwise shut down.
[ "$uid_session" ] &&
ps axo uid,cmd | \
awk '
    $1 == '$uid_session' &&
	($2 == "gnome-power-manager" || $2 == "kpowersave" || $2 == "xfce4-power-manager" || $2 ~ /meego-power-icon/ ) \
		{ found = 1; exit }
    END { exit !found }
' ||
  echo "mem" > /sys/power/state

