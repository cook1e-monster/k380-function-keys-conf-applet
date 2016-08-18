from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
import signal
import os
import subprocess
from gi.repository import Notify as notify

icons_path = 'icons/'
icon_on = os.path.abspath(icons_path + "switch_on.svg")
icon_off = os.path.abspath(icons_path + "switch_off.svg")

APPINDICATOR_ID = 'myappindicator'
indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(icon_off), appindicator.IndicatorCategory.SYSTEM_SERVICES)

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

def quit(source):
    notify.uninit()
    gtk.main_quit()

def keyboard_on(_):
    indicator.set_icon(icon_on)
    notify.Notification.new("<b>Keyboard Block On</b>", "Block Fn Keys", None).show()
    os.chdir('/opt/k380-function-keys-conf/')
    subprocess.call(['sudo', "./k380_conf", "-d", "/dev/hidraw1", "-f", "on"])

def keyboard_off(_):
    indicator.set_icon(icon_off)
    notify.Notification.new("<b>Block Off</b>", "Block Fn Keys", None).show()
    #os.chdir('/opt/k380-function-keys-conf/')
    subprocess.call(['sudo', "./k380_conf", "-d", "/dev/hidraw1", "-f", "off"])

def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    notify.init(APPINDICATOR_ID)
    gtk.main()

if __name__ == "__main__":
    main()
