from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from config import sudoPassword, icon_path, base_dir
import os, signal, subprocess

icon_on = "%s/%s" %(icon_path, "switch_on.svg")
icon_off = "%s/%s" %(icon_path, "switch_off.svg")

APPINDICATOR_ID = 'keyboardindicator'
indicator = appindicator.Indicator.new(APPINDICATOR_ID, icon_off, appindicator.IndicatorCategory.SYSTEM_SERVICES)

def build_menu():
    menu = gtk.Menu()

    item_on = gtk.MenuItem('On')
    item_on.connect('activate', keyboard_on)
    menu.append(item_on)

    item_off = gtk.MenuItem('Off')
    item_off.connect('activate', keyboard_off)
    menu.append(item_off)


    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def executeWithRoot(action):
    os.chdir(base_dir)
    command = "./k380_conf -d /dev/hidraw1 -f %s" % action
    os.system('echo %s|sudo -S %s' % (sudoPassword, command))

def quit(source):
    notify.uninit()
    gtk.main_quit()

def keyboard_on(_):
    indicator.set_icon(icon_on)
    notify.Notification.new("<b>Keyboard Block On</b>", "Block Fn Keys", None).show()
    executeWithRoot('on')

def keyboard_off(_):
    indicator.set_icon(icon_off)
    notify.Notification.new("<b>Block Off</b>", "Block Fn Keys", None).show()
    executeWithRoot('off')

def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    notify.init(APPINDICATOR_ID)
    gtk.main()

if __name__ == "__main__":
    main()
