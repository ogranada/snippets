#!/bin/bash
# Copyright (c) 2009 Sebastian Wiesner <basti.wiesner@gmx.net>

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

# shortcut to set a dialog property
set_dialog_property() {
    qdbus ${1} org.freedesktop.DBus.Properties.Set \
        org.kde.kdialog.ProgressDialog "${2}" "${3}" > /dev/null
}

# start the dialog and store the DBus service and object path for
# communication
dialog=$(kdialog --progressbar 'Doing something')

# set maximum value, used to calculate filling level
set_dialog_property "${dialog}" maximum 100
# enable automatical closing, once maximum value is reached.  If not
# enabled, the dialog must be closed manually using the
# org.kde.kdialog.ProgressDialog.close method.
set_dialog_property "${dialog}" autoClose true
# enable cancel button.  Note, that this button is *not* affected by the
# autoClose property.  The dialog *never* closes automatically, if the
# cancel button is pressed.
qdbus ${dialog} org.kde.kdialog.ProgressDialog.showCancelButton true > /dev/null

for ((counter=1; counter <= 100; counter++)); do
    # check if the dialog was cancelled, and exit the loop in this case
    cancelled=$(qdbus $dialog org.kde.kdialog.ProgressDialog.wasCancelled)
    if [[ "${cancelled}" == "true" ]]; then
        echo "cancelled"
        # manually close the dialog
        qdbus ${dialog} org.kde.kdialog.ProgressDialog.close > /dev/null
        exit 1
    fi
    sleep 1
    # refresh value and label
    set_dialog_property "${dialog}" value "${counter}"
    qdbus ${dialog} org.kde.kdialog.ProgressDialog.setLabelText \
        "Step ${counter}" > /dev/null
done

