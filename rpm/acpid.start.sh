#!/bin/sh

for SCRIPT in /etc/acpi/start.d/*.sh; do
    if [ -x $SCRIPT ] ; then
	. $SCRIPT
    fi
done
