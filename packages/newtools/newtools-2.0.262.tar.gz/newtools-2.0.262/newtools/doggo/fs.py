# (c) 2012-2020 Deductive, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

"""

Cross-platform supports for reading, writing, copying, deleting, etc... files from S3 or local

.. parsed-literal::

             ,--._______,-.
           ,','  ,    .  ,_`-.
          / /  ,' , _` ``. |  )       `-..
         (,';'""`/ '"`-._ ` `/ ______    \\
           : ,o.-`- ,o.  )`` -'      `---.))
           : , d8b ^-.   '|   `.      `    `.
           |/ __:_     `. |  ,  `       `    \
           | ( ,-.`-.    ;'  ;   `       :    ;
           | |  ,   `.      /     ;      :    \
           ;-'`:::._,`.__),'             :     ;
          / ,  `-   `--                  ;     |
         /  `                   `       ,      |
        (    `     :              :    ,`      |
         `   `.    :     :        :  ,'  `    :
          `    `|-- `     ` ,'    ,-'     :-.-';
          :     |`--.______;     |        :    :
           :    /           |    |         |   \
           |    ;           ;    ;        /     ;
         _/--' |   -hrr-   :`-- /         `_:_:_|
       ,',','  |           |___ \
       `^._,--'           / , , .)
                          `-._,-'
"""

import shutil
import os
from glob import glob
import re
from newtools.optional_imports import s3fs
from newtools.aws import S3Location
from .doggo import FileDoggo


class DoggoFileSystem:
    """
    Implements common file operations using either S3 or local file system depending on whether the path
    begins "s3://"

    """
    __s3fs = None

    def __init__(self, session=None):
        s3fs.S3FileSystem.read_timeout = 600
        self.__s3fs = s3fs.S3FileSystem(session=session)

    @property
    def _s3fs(self):
        """
        S3FS caching does not respect other applications updating S3 so therefore we invalidate
        the cache before using

        :return: the S3FS File system
        """
        self.__s3fs.invalidate_cache()
        return self.__s3fs

    def is_s3(self, path1, path2=None):
        """
        Returns true if the passed path is on S3

        :param path1: the first path to check
        :param path2: the second path to check
        :raises NotImplementedError: if only one of the two paths in on S3
        :return: True if both are S3, False if neither are, and raises an exception for mixed types
        """
        p1_is_s3 = path1.startswith("s3://")
        p2_is_s3 = p1_is_s3 if path2 is None else path2.startswith("s3://")

        if path2 is not None:
            return p1_is_s3 and p2_is_s3
        else:
            return p1_is_s3

    def _check_folders(self, path):
        if not self.is_s3(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

    def cp(self, source, destination):
        """
        Copies a file or folder, per shutil copy() or shutil.copytree() depending on
        if source is a /folder/ or a /file.extension

        :param source: source path, folders must be specified by trailing '/'
        :param destination: destination path, folders must be specified by trailing '/'
        """

        if not self.exists(source):
            raise FileNotFoundError('The specified source file/folder cannot be located')

        is_directory = source.endswith('/')

        if self.is_s3(source, destination):
            return self._s3fs.cp(source, destination)

        elif not self.is_s3(source) and self.is_s3(destination):
            return self._s3fs.put(lpath=source,
                                  rpath=destination,
                                  recursive=True)

        elif self.is_s3(source) and not self.is_s3(destination):
            return self._s3fs.get(lpath=destination,
                                  rpath=source,
                                  recursive=is_directory)

        else:
            if is_directory:
                return shutil.copytree(source, destination)
            else:
                self._check_folders(destination)
                return shutil.copy(source, destination)

    def mv(self, source, destination):
        """
        Moves a file per shutil.move() except that it does not copy WITHIN.
        i.e. /location/folderA/ >> /destination/folderA/
        rather than
        i.e. /location/folderA/ >> /destination/folderA/folderA/

        :param source: source path, folders must be specified by trailing '/'
        :param destination: destination path, folders must be specified by trailing '/'
        """

        if not self.exists(source):
            raise FileNotFoundError('The specified source file/folder cannot be located')

        is_directory = source.endswith('/')

        if self.is_s3(source, destination):
            return self._s3fs.mv(source, destination)

        elif not self.is_s3(source) and self.is_s3(destination):
            self._s3fs.put(lpath=source,
                           rpath=destination,
                           recursive=True)
            if is_directory:
                return shutil.rmtree(source)
            else:
                return os.remove(source)

        elif self.is_s3(source) and not self.is_s3(destination):
            self._s3fs.get(lpath=destination,
                           rpath=source,
                           recursive=is_directory)
            return self._s3fs.rm(source, recursive=is_directory)

        else:
            if is_directory:
                shutil.copytree(source, destination)
                return shutil.rmtree(source)

            else:
                self._check_folders(destination)
                shutil.copy(source, destination)
                return os.remove(source)

    def exists(self, path):
        """
        Returns true if a path exists, per os.path.exists()

        :param path: the path to check
        :return: True if the path exists, otherwise False
        """
        if self.is_s3(path):
            return self._s3fs.exists(path)
        else:
            return os.path.exists(path)

    def size(self, path):
        """
        Returns the size of a file per os.path.getsize()

        :param path: the path to check
        :return: the size of the file at this path
        """
        if self.is_s3(path):
            return self._s3fs.size(path)
        else:
            return os.path.getsize(path)

    def rm(self, path, **kwargs):
        """
        Removes a file, per os.remove()

        :param path: the file to remove
        """
        if self.is_s3(path):
            return self._s3fs.rm(path, **kwargs)
        else:
            return os.remove(path)

    def glob(self, glob_string):
        """
        Searched for a file per glob.glob(recursive=True)


        :param glob_string: the path to search
        :return:
        """
        if self.is_s3(glob_string):
            return [S3Location(a) for a in self._s3fs.glob(glob_string)]
        else:
            return glob(glob_string, recursive=True)

    def open(self, path, mode, *args, **kwargs):
        """
        Opens a file, per open()

        :param path: the path to open
        :param mode: the mode to open in
        :param args: any arguments in the FileDoggo class
        :param kwargs: any keyword arguments for the FileDoggo class
        :return: a file handle
        """
        if "w" in mode:
            self._check_folders(path)
        return FileDoggo(path, mode, *args, **kwargs)

    def join(self, path, *paths):
        """
        Joins to paths per os.path.join()
        :param path: the first path
        :param paths: the paths to joins
        :return:
        """
        if self.is_s3(path):
            return S3Location(path).join(*paths)
        else:
            return os.path.join(path, *paths)

    def split(self, path):
        """
        Splits a path into prefix and file, per os.path.split()
        :param path:
        :return:
        """
        if self.is_s3(path):
            loc = S3Location(path)
            if loc.prefix is not None:
                return S3Location(loc.bucket).join(loc.prefix), loc.file
            else:
                return S3Location(loc.bucket), loc.file
        else:
            return os.path.split(path)
