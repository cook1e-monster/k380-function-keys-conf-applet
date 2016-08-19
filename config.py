from os import path
from inspect import getfile, currentframe

sudoPassword = 'your password'
base_dir = path.dirname(path.abspath(getfile(currentframe())))

#options - icons or icons2
icons = "icons2"
icon_path = '%s/%s' %(base_dir, icons)

#block function keys startup
auto_block = True
