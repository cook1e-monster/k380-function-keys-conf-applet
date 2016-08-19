from os import path
from inspect import getfile, currentframe

sudoPassword = 'you password'
base_dir = path.dirname(path.abspath(getfile(currentframe())))
icon_path = '%s/%s' %(base_dir, 'icons')

#block function keys startup
auto_block = True
