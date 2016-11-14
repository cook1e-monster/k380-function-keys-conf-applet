#!/usr/bin/python
from os import system
from shutil import copytree
from config import base_dir
import errno

#udev permisions
def create_file():
    file_name = "99-keyboard.rules"
    path = "/etc/udev/rules.d/"

    print 'keyboards detected: '
    command = "ls /dev/hidraw*"
    system(command)

    input_text = "hidraw number (default value *): "
    value_input = raw_input(input_text)

    if value_input is None or value_input is "":
        hidraw = "*"
    else:
        hidraw = value_input

    print "create rule udev %s" % file_name

    file = open(path + file_name, 'w+')

    if hidraw is "*":
        text = 'KERNEL=="hidraw%s", SUBSYSTEM=="hidraw", ATTRS{address}=="*", MODE="0666"' % 0
        file.write(text)
        file.write('\n')

        text += 'KERNEL=="hidraw%s", SUBSYSTEM=="hidraw", ATTRS{address}=="*", MODE="0666"' % 1
        file.write(text)
        file.write('\n')

    else:
        text = 'KERNEL=="hidraw%s", SUBSYSTEM=="hidraw", ATTRS{address}=="*", MODE="0666"' % hidraw
        file.write(text)
        file.write('\n')

    file.close()

    if hidraw is "*":
        dir_dev = "/dev/hidraw%s" % 0
        dir_dev2 = "/dev/hidraw%s" % 1
        print "change permision in %s to 0666" % dir_dev
        print "change permision in %s to 0666" % dir_dev2

        command = "chmod 0666 %s" % dir_dev
        system(command)

        command = "chmod 0666 %s" % dir_dev2
        system(command)
    else:
        dir_dev = "/dev/hidraw%s" % hidraw
        print "change permision in %s to 0666" % dir_dev

        command = "chmod 0666 %s" % dir_dev
        system(command)

    return

#copi files
def copy_files():
    dest = '/opt/keyboard-applet/'

    input_text = "change path (default value %s): " % dest
    value_input = raw_input(input_text)

    if value_input is None or value_input is "":
        path = dest
    else:
        path = value_input

    print "create folder keyboard-applet in %s" % path

    try:
        copytree(base_dir, path)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

    print "add python %s applet.py in startup applications" % path

    return

create_file()
copy_files()
print 'final setup.'
