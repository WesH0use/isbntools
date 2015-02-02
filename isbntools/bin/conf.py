#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


from difflib import get_close_matches

from isbnlib.dev.helpers import ShelveCache

from isbntools._lab import sprint

from isbntools.app import quiet_errors, CONF_PATH, CACHE_FILE
from isbntools.conf import (reg_plugin, reg_apikey, mk_conf,
                            print_conf, reg_mod, reg_myopt)


def delcache():
    try:
        os.remove(os.path.join(CONF_PATH, CACHE_FILE))
    except:
        pass


def cachepath():
    try:
        print(os.path.join(CONF_PATH, CACHE_FILE))
    except:
        pass


def dumpcache():
    try:
        path_cache = os.path.join(CONF_PATH, CACHE_FILE)
        sc = ShelveCache(path_cache)
        for k in list(sc.keys()):
            sprint(repr(sc[k]))
    except:
        pass


VERBS = {'show': print_conf, 'make': mk_conf,
         'setkey': reg_apikey, 'regplugin': reg_plugin,
         'regmod': lambda x, y: reg_mod({x: y}),
         'setopt': reg_myopt, 'delcache': delcache, 'cachepath': cachepath,
         'dumpcache': dumpcache}


def usage():
    sys.stderr.write('Usage: isbn_conf COMMAND OPTIONS\n'
                     '\n'
                     'COMMAND    OPTIONS               DESCRIPTION\n'
                     '-------    --------------------  ----------------------------\n'
                     'show                             show the conf file\n'
                     'make                             make a conf file\n'
                     'setkey     SERVICE  APIKEY       sets an apikey\n'
                     'regplugin  SERVICE  [DIRECTORY]  registers a service\n'
                     'regmod     OPTION   VALUE        sets options for modules\n'
                     'setopt     OPTION   VALUE        sets options in MISC section\n'
                     'delcache                         deletes the metadata cache\n'
                     'cachepath                        show the path of the cache\n'
                     'dumpcache                        write the cache to sys.stdout\n'
                     )
    return 1


def main(args=None):
    sys.excepthook = quiet_errors
    try:
        args = sys.argv if not args else args
        nargv = len(args)
        if nargv > 4 or nargv == 1:
            raise
        cmd = get_close_matches(args[1], list(VERBS.keys()))[0]
        if nargv == 2:
            VERBS[cmd]()
        elif nargv > 2:
            VERBS[cmd](*args[2:])
    except:
        usage()