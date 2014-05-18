# -*- coding: utf-8 -*-

"""
Helper module to work with files
"""

import re
import os
import logging
from .exceptions import FileNotFoundError

MAXLEN = 100
ILEGAL = r'<>:"/\|?*'
LOGGER = logging.getLogger(__name__)


class File(object):
    """
    Allows easy manipulation of files on the SAME directory
    """

    def __init__(self, fp):
        """
        Sets and validates the basic properties
        """
        if not self.exists(fp):
            raise FileNotFoundError(fp)
        self.path = os.path.dirname(fp) or os.getcwd()
        self.basename = os.path.basename(fp)
        self.name, self.ext = os.path.splitext(self.basename)

    def siblings(self):
        """
        Collection of other files and folders in the same folder
        """
        return [f for f in os.listdir(self.path) if f != self.basename]

    @staticmethod
    def exists(fp):
        """
        Checks if a given filepath exists
        """
        if not os.path.isfile(fp):
            LOGGER.critical("This file %s doesn't exist", fp)
            return False
        return True

    @staticmethod
    def mkwinsafe(name, space=' '):
        """
        Deletes the most common characters not allowed in Windows filenames
        """
        space = space if space not in ILEGAL else ' '
        name = ''.join(c for c in name if c not in ILEGAL)\
               .replace(' ', space).strip()
        name = re.sub(r'\s\s+', ' ', name) if space == ' ' else name
        return name[:MAXLEN]

    @staticmethod
    def validate(basename):
        """
        Minimum checks for a basename
        """
        if basename != os.path.basename(basename):
            LOGGER.critical("This %s is not a basename!", basename)
            return False
        name, ext = os.path.splitext(basename)
        if len(name) == 0:
            LOGGER.critical("Not a valid name (lenght 0)!")
            return False
        if len(ext) == 0:
            LOGGER.critical("Not a valid extension (lenght 0)!")
            return False
        return True

    def baserename(self, new_basename):
        """
        Renames the file to a 'safe' basename
        """
        if not self.validate(new_basename):
            return False
        name, ext = os.path.splitext(new_basename)
        name = self.mkwinsafe(name)
        new_basename = name + ext
        if new_basename == self.basename:
            return True
        if new_basename not in self.siblings():
            try:
                os.rename(self.basename, new_basename)
            except OSError as e:
                LOGGER.critical("%s", e.message)
                return False
            self.basename = new_basename
            self.name = name
            self.ext = ext
            return True
        else:
            LOGGER.info("This file %s already exists in the directory!",
                        new_basename)
            return False
