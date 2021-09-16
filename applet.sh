#!/bin/sh

# copy this file in /usr/local/bin or /usr/bin

dir="" # installation directory
command="k380_conf -d /dev/hidraw$1 -f on"


$dir$command
