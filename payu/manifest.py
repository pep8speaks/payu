"""payu.manifest
   ===============

   Interface to a manifest file

   :copyright: Copyright 2011 Marshall Ward, see AUTHORS for details.
   :license: Apache License, Version 2.0, see LICENSE for details.
"""

# Python3 preparation
from __future__ import print_function, absolute_import

# Local
from payu import envmod
from payu.fsops import make_symlink

# External
from yamanifest.manifest import Manifest
from yamanifest.utils import find_files
import yamanifest as ym
from copy import deepcopy

import os


# fast_hashes = ['nchash','binhash']
fast_hashes = ['binhash']
full_hashes = ['md5']

class PayuManifest(Manifest):
    """
    A manifest object sub-classed from yamanifest object with some payu specific
    additions and enhancements
    """

    def __init__(self, path, hashes=None, **kwargs):
        super(PayuManifest, self).__init__(path, hashes, **kwargs)

    def check_fast(self, reproduce=False, **args):
        """
        Check hash value for all filepaths using a fast hash function and fall back to slower
        full hash functions if fast hashes fail to agree
        """
        hashvals = {}
        if not self.check_file(filepaths=self.data.keys(),hashvals=hashvals,hashfn=fast_hashes,shortcircuit=True,**args):
            # Run a fast check, if we have failures, deal with them here
            for filepath in hashvals:
                print("Check failed for {} {}".format(filepath,hashvals[filepath]))
                tmphash = {}
                if self.check_file(filepaths=filepath,hashfn=full_hashes,hashvals=tmphash,shortcircuit=False,**args):
                    # File is still ok, so replace fast hashes
                    print("Full hashes ({}) checked ok".format(full_hashes))
                    print("Updating fast hashes for {} in {}".format(filepath,self.path))
                    self.add_fast(filepath,force=True)
                else:
                    # File has changed, update hashes unless reproducing run
                    if not reproduce:
                        print("Updating entry for {} in {}".format(filepath,self.path))
                        self.add_fast(filepath,force=True)
                        self.add(filepath,hashfn=full_hashes,force=True)
                    else:
                        sys.stderr.write("Run cannot reproduce: manifest {} is not correct\n".format(self.path))
                        for fn in full_hashes:
                            sys.stderr.write("Hash {}: manifest: {} file: {}\n".format(fn,self.data[filepath]['hashes'][fn],tmphash[fn]))
                        sys.exit(1)

            # Write updates to version on disk
            self.dump()
            

    def add_fast(self, filepath, hashfn=fast_hashes, force=False):
        """
        Bespoke function to add filepaths but set shortcircuit to True, which means
        only the first calculatable hash will be stored. In this way only one "fast"
        hashing function need be called for each filepath
        """
        self.add(filepath, hashfn, force, shortcircuit=True)
        
    def make_links(self):
        """
        Payu integration function for creating symlinks in work directories which point
        back to the original file
        """
        print("Making links from manifest: {}".format(self.path))
        for filepath in self:
            # print("Linking {}".format(filepath))
            # Don't try and link to itself, which happens when there is a real
            # file in the work directory, and not a symbolic link
            if not os.path.realpath(filepath) == self.fullpath(filepath):
                make_symlink(self.fullpath(filepath), filepath)
