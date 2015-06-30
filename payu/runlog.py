"""payu.runlog
   ===========

   Experiment run logging manager

   :copyright: Copyright 2011 Marshall Ward, see AUTHORS for details.
   :license: Apache License, Version 2.0, see LICENSE for details.
"""

# Standard Library
import datetime
import os
import shlex
import subprocess as sp

# Local
from payu import envmod
from payu.fsops import DEFAULT_CONFIG_FNAME


class Runlog(object):

    def __init__(self, expt):

        self.expt = expt

        self.manifest = []
        self.create_manifest()

    def create_manifest(self):

        config_path = os.path.join(self.expt.control_path,
                                   DEFAULT_CONFIG_FNAME)

        if os.path.isfile(config_path):
            self.manifest.append(config_path)

        for model in self.expt.models:
            self.manifest.extend(os.path.join(model.control_path, f)
                                 for f in model.config_files)

    def commit(self):

        f_null = open(os.devnull, 'w')

        # Check if a repository exists
        cmd = 'git rev-parse'
        print(cmd)
        rc = sp.call(shlex.split(cmd), stdout=f_null, cwd=self.expt.control_path)
        if rc:
            cmd = 'git init'
            print(cmd)
            sp.check_call(shlex.split(cmd), stdout=f_null, cwd=self.expt.control_path)

        # Add configuration files
        for fname in self.manifest:
            cmd = 'git add {}'.format(fname)
            print(cmd)
            sp.check_call(shlex.split(cmd), stdout=f_null,cwd=self.expt.control_path)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_msg = '{}: Run {}'.format(timestamp, self.expt.counter)

        cmd = 'git commit -am "{}"'.format(commit_msg)
        print(cmd)
        try:
            sp.check_call(shlex.split(cmd), stdout=f_null,cwd=self.expt.control_path)
        except sp.CalledProcessError:
            print('TODO: Check if commit is unchanged')

        # Save the current git hash regardless of the success of the last commit
        cmd = 'git rev-parse HEAD'
        print(cmd)
        try:
            self.exptID = sp.check_output(shlex.split(cmd), cwd=self.expt.control_path)
        except sp.CalledProcessError:
            print('Failed to find git id in {}'.format(self.expt.control_path))
            self.exptID = None

        f_null.close()
