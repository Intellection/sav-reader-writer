# -*- coding: utf-8 -*-
"""
Download SPSS I/O libraries for mainframes (HP-UX, Solaris, AIX, zLinux)

These have to be downloaded separately because otherwise savReaderWriter 
exceeds the Pypi file size limit (60Mb or so)
"""
import os
import sys
import platform
import zipfile
from os.path import join, dirname, basename, abspath, pardir, isdir

if sys.version_info.major > 2:
    import urllib.request
    urlretrieve = urllib.request.urlretrieve
else:
    import urllib
    urlretrieve = urllib.urlretrieve


def spssio_foldername():
    arch = platform.architecture()[0]
    is_64bit = arch == "64bit"
    pf = sys.platform.lower()
    msg = ("Your platform (%r, %s) is either not supported, or does not " 
           "require that the SPSS I/Olibraries are downloaded separately")
    if is_64bit:
        if pf.startswith("lin")and os.uname()[-1] == "s390x":
            return 'zlinux64'
        elif pf.startswith("aix"):
            return 'aix64'
        elif pf.startswith("hp-ux"):
            return 'hpux_it'
        elif pf.startswith("sunos"):
            return 'sol64'
        else:
            raise EnvironmentError(msg % (pf, arch))
    else:
        raise EnvironmentError(msg % (pf, arch))
    
def download_progress(count, block_size, total_size):
   percent = int((count * block_size * 100) / total_size)
   s = '\r[{0}] {1}%'.format('#' * percent, percent)
   sys.stdout.write("\r" + s)
   sys.stdout.flush()

def unzip(local_file, dst_path):
    with zipfile.ZipFile(local_file) as zf:
        for item in zf.infolist():
            filename = basename(item.filename)
            if basename(dst_path) in item.filename:
                if isdir(join(dst_path, filename)):
                    continue
                with open(join(dst_path, filename), "wb") as outfile:
                    print("... extracting '%s' to '%s'" % (filename, dst_path))
                    outfile.write(zf.read(item))
    os.remove(local_file)

def main():
    dst_folder = spssio_foldername()
    #dst_folder = "hpux_it"
    py_path = dirname(abspath(__file__))
    dst_path = abspath(join(py_path, pardir, "spssio", dst_folder))
    remote_file = ("https://bitbucket.org/fomcl/savreaderwriter/downloads/"
                   "mainframe_libs.zip")
    local_file = join(dst_path, basename(remote_file))
    print("... Downloading '%s'" % remote_file)
    urlretrieve(remote_file, local_file, reporthook=download_progress)
    unzip(local_file, dst_path)
    print("Done!")
                
 
if __name__ == "__main__":
    main()