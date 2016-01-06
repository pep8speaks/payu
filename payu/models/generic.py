# coding: utf-8
"""payu.models.matm
   ================

   Driver interface to a generic model.

   :copyright: Copyright 2011 Marshall Ward, see AUTHORS for details
   :license: Apache License, Version 2.0, see LICENSE for details
"""

# Standard Library
import os

# Local
from payu.models.model import Model

class Generic(Model):

    def __init__(self, expt, name, config):
        super(Generic, self).__init__(expt, name, config)

        self.model_type = 'generic'

    def set_model_pathnames(self):
        super(Generic, self).set_model_pathnames()

    def archive(self):
        pass

    def collate(self):
        pass
