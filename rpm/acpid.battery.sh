#!/bin/sh

. /etc/sysconfig/acpi
. /usr/share/acpi/power-funcs

if [ x$1 = xstop ] ; then
  # When  stop, we go to the AC state regardless of the actual power state.
  RUN_SCRIPT_DIR=/etc/acpi/ac.d

  # However, if we have a stored power state, and that power state is already
  # AC, then we don't need to do anything, and we exit immediately.
  if [ -f "$POWERSTATE" ]; then
    OLDSTATE=$(cat $POWERSTATE) 
    if [ "$OLDSTATE" = "AC" ] ; then  
      exit 0
    fi
  fi
else
  # Get the power state (AC/BATTERY) into STATE
  getState;

  # Compare the power state with a stored state and exit if the state is the
  # same. If not, then store the power state for comparison the next time
  # around.
  checkStateChanged;

  if [ "$STATE" = "BATTERY" ] ; then
    RUN_SCRIPT_DIR=/etc/acpi/battery.d
  else
    RUN_SCRIPT_DIR=/etc/acpi/ac.d
  fi
fi

for SCRIPT in $RUN_SCRIPT_DIR/*.sh; do
    if [ -f $SCRIPT ] ; then
	. $SCRIPT
    fi
done

