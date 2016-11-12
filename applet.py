#!/usr/bin/python
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from config import icon_path, base_dir, auto_block
import os, signal, subprocess

#icons
icon_on = "%s/%s" %(icon_path, "switch_on.svg")
icon_off = "%s/%s" %(icon_path, "switch_off.svg")

APPINDICATOR_ID = 'keyboardindicator'
indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon_off, appindicator.IndicatorCategory.SYSTEM_SERVICES)

### Menu ###
def build_menu():
    menu = gtk.Menu()

    ### item ###
    item_on = gtk.MenuItem('On') # menu label
    item_on.connect('activate', keyboard_on) #actions
    menu.append(item_on) #add menu

    ### item ###
    item_off = gtk.MenuItem('Off') # menu label
    item_off.connect('activate', keyboard_off) #actions
    menu.append(item_off) #add menu

    ### item ###
    item_quit = gtk.MenuItem('Quit') # menu label
    item_quit.connect('activate', quit) #actions
    menu.append(item_quit) #add menu

    menu.show_all()
    return menu

### execute binary script ###
def executeWithRoot(action):
    os.chdir(base_dir) # cd path
    command = "./k380_conf -d /dev/hidraw0 -f %s" % action
    os.system(command)

### exit program ###
def quit(source):
    notify.uninit()
    gtk.main_quit()

### keyboard actions ###
def keyboard_on(_):
    #switch icon
    indicator.set_icon(icon_on)
    #message
    notify.Notification.new("<b>Keyboard Block On</b>", "Block Fn Keys", None).show()
    #execute binary
    executeWithRoot('on')

def keyboard_off(_):
    #switch icon
    indicator.set_icon(icon_off)
    #message
    notify.Notification.new("<b>Keyboard Block Off</b>", "Block Fn Keys", None).show()
    #execute binary
    executeWithRoot('off')


### main ###
def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    notify.init(APPINDICATOR_ID)

    if auto_block:
        keyboard_on(None)

    gtk.main()

if __name__ == "__main__":
    main()
