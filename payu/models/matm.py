# coding: utf-8
"""payu.models.matm
   ================

   Driver interface to the MATM model.

   :copyright: Copyright 2011 Marshall Ward, see AUTHORS for details
   :license: Apache License, Version 2.0, see LICENSE for details
"""

# Standard Library
import os, shutil

# Local
from payu.models.model import Model
from payu.fsops import mkdir_p


class Matm(Model):

    def __init__(self, expt, name, config):
        super(Matm, self).__init__(expt, name, config)

        self.model_type = 'matm'
        self.default_exec = 'matm'

        # Default repo details
        self.repo_url = 'https://github.com/CWSL/matm.git'
        self.repo_tag = 'master'

        self.config_files = ['input_atm.nml',
                             'data_4_matm.table']

    def set_model_pathnames(self):
        super(Matm, self).set_model_pathnames()

        self.build_exec_path = os.path.join(self.codebase_path, 'build_nt62')
        self.work_input_path = os.path.join(self.work_path, 'INPUT')

    def archive(self):

        # Delete all symbolic links in work
        for f in os.listdir(self.work_path):
            f_path = os.path.join(self.work_path, f)
            if os.path.islink(f_path):
                os.remove(f_path)

        # Create an empty restart directory
        mkdir_p(self.restart_path)

        # Copy config files to restart
        for f in self.config_files:
            f_path = os.path.join(self.work_path, f)
            r_path = os.path.join(self.restart_path, f)
            shutil.copy2(f_path,r_path)

        # Remove the INPUT directory
        shutil.rmtree(self.work_input_path,ignore_errors=True)

    def collate(self):
        pass
