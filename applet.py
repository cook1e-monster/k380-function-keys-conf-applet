#!/usr/bin/python
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from config import icon_path, base_dir, auto_block
import os, signal, subprocess, sys

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
def execute_command(action):

    file_name = base_dir + '/hidraw'
    mode = 'r' if os.path.exists(file_name) else 'w'

    try:
        with open(file_name, mode) as f:
            hidraw = f.read()
            print "read file " + file_name

        if not hidraw:
            print "no data in file " + file_name
            hidraw = 0

        with open(file_name, 'w') as dest:
            dest.write('0')

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        hidraw = 0

        with open(file_name, 'w') as dest:
            dest.write('0')

    except: #handle other exceptions such as attribute errors
        print "Unexpected error:", sys.exc_info()[0]












    #try:
    #    f = open(, 'r')
    #    hidraw = f.read()[0]
    #    f.close()
    #except ValueError as e:
    #    print e
    #    f = open(base_dir + '/hidraw', 'w+')
    #    f.write('0')
    #    f.close()



    os.chdir(base_dir) # cd path
    command = "./k380_conf -d /dev/hidraw%s -f %s" % (hidraw, action)

    c = os.system(command)

    print 'salida command %s' % c
    if c is not 0:
        hidraw = 0 if hidraw == '1' else 1

        print "hidraw is %s" % hidraw
        f = open(base_dir + '/hidraw', 'w+')
        f.write(str(hidraw))
        f.close()

        command = "./k380_conf -d /dev/hidraw%s -f %s" % (hidraw, action)

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
    execute_command('on')

def keyboard_off(_):
    #switch icon
    indicator.set_icon(icon_off)
    #message
    notify.Notification.new("<b>Keyboard Block Off</b>", "Block Fn Keys", None).show()
    #execute binary
    execute_command('off')


### main ###
def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    notify.init(APPINDICATOR_ID)

    if auto_block:
        keyboard_on("")

    gtk.main()

if __name__ == "__main__":
    main()
