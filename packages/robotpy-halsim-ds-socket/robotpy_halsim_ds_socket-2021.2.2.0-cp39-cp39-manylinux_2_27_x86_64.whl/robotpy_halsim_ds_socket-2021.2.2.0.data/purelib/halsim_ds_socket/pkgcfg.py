# fmt: off
# This file is automatically generated, DO NOT EDIT

from os.path import abspath, join, dirname
_root = abspath(dirname(__file__))

libinit_import = "halsim_ds_socket._init_halsim_ds_socket"
depends = ['wpiHal']
pypi_package = 'robotpy-halsim-ds-socket'

def get_include_dirs():
    return [join(_root, "include"), join(_root, "rpy-include")]

def get_library_dirs():
    return []

def get_library_dirs_rel():
    return []

def get_library_names():
    return []

def get_library_full_names():
    return ['libhalsim_ds_socket.so']