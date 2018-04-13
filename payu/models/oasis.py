# coding: utf-8
"""payu.models.oasis
   =================

   Driver interface to the oasis coupler.

   :copyright: Copyright 2011 Marshall Ward, see AUTHORS for details
   :license: Apache License, Version 2.0, see LICENSE for details
"""

# Standard Library
import os
import sys
import shlex
import shutil
import subprocess

# Extensions
import f90nml

# Local
import payu.calendar as cal
from payu.fsops import mkdir_p, make_symlink
from payu.models.model import Model
from payu.namcouple import Namcouple


class Oasis(Model):

    def __init__(self, expt, name, config):
        super(Oasis, self).__init__(expt, name, config)

        self.model_type = 'oasis'
        self.copy_restarts = False
        self.copy_inputs = False

        self.config_files = ['namcouple']

    def setup(self):
        super(Oasis, self).setup()

        # Copy OASIS data to the other submodels

        # TODO: Parse namcouple to determine filelist
        # TODO: Let users map files to models

        # Do not need to make these links if using existing restart manifest
        if not self.expt.have_restart_manifest:

            restart_files = []
    
            # Find all the coupler restart files that have been added
            # to the restart manifest
            for f in self.expt.restart_manifest:
                if f.startswith(self.work_path_local):
                    restart_files.append(os.path.relpath(f,self.work_path_local)) 

            restart_files_local = set()

            for model in self.expt.models:

                # Skip the oasis self-reference
                if model == self:
                    continue

                mkdir_p(model.work_path)
                for f_name in restart_files + self.config_files:
                    f_path = os.path.join(self.work_path, f_name)
                    f_sympath = os.path.join(model.work_path, f_name)
                    make_symlink(f_path, f_sympath)
                    restart_files_local.add(os.path.join(model.work_path_local,f_name))

            if restart_files_local:
                # Add to input manifest all at once (parallelised)
                self.expt.restart_manifest.add_fast(list(restart_files_local))

        # Do not need to make these links if using existing restart manifest
        if not self.expt.have_input_manifest:

            input_files = []

            # Find all the coupler restart files that have been added
            # to the restart manifest
            for f in self.expt.input_manifest:
                if f.startswith(self.work_path_local):
                    input_files.append(os.path.relpath(f,self.work_path_local)) 

            input_files_local = []

            for model in self.expt.models:

                # Skip the oasis self-reference
                if model == self:
                    continue

                mkdir_p(model.work_path)
                for f_name in input_files:
                    f_path = os.path.join(self.work_path, f_name)
                    f_sympath = os.path.join(model.work_path, f_name)
                    make_symlink(f_path, f_sympath)
                    input_files_local.append(os.path.join(model.work_path_local,f_name))

            if input_files_local:
                # Add to input manifest all at once (parallelised)
                self.expt.input_manifest.add_fast(input_files_local)

        if self.expt.runtime:
            # TODO: Implement runtime patch to namcouple
            pass

    def set_timestep(self, t_step):

        namcpl_path = os.path.join(self.work_path, 'namcouple')
        namcpl = Namcouple(namcpl_path, 'access')
        namcpl.set_ice_ocean_coupling_timestep(str(t_step))
        namcpl.write()

        for model in self.expt.models:

            if model.model_type in ('cice', 'cice5'):

                # Set namcouple timesteps

                ice_ts = model.config.get('timestep')
                if ice_ts:
                    model.set_oasis_timestep(ice_ts)

                # Set ACCESS coupler timesteps

                input_ice_path = os.path.join(model.work_path, 'input_ice.nml')
                input_ice = f90nml.read(input_ice_path)

                input_ice['coupling_nml']['dt_cpl_io'] = t_step

                input_ice.write(input_ice_path, force=True)

            elif model.model_type == 'matm':

                input_atm_path = os.path.join(model.work_path, 'input_atm.nml')
                input_atm = f90nml.read(input_atm_path)

                input_atm['coupling']['dt_atm'] = t_step

                input_atm.write(input_atm_path, force=True)

            elif model.model_type == 'mom':

                input_nml_path = os.path.join(model.work_path, 'input.nml')
                input_nml = f90nml.read(input_nml_path)

                input_nml['auscom_ice_nml']['dt_cpl'] = t_step
                input_nml['ocean_solo_nml']['dt_cpld'] = t_step

                input_nml.write(input_nml_path, force=True)

    def archive(self):

        # TODO: Determine the exchange files
        restart_files = ['a2i.nc', 'i2a.nc', 'i2o.nc', 'o2i.nc']

        mkdir_p(self.restart_path)
        for f in restart_files:
            f_src = os.path.join(self.work_path, f)
            f_dst = os.path.join(self.restart_path, f)

            if os.path.exists(f_src):
                shutil.copy2(f_src, f_dst)

        # Delete all symbolic links in work
        for f in os.listdir(self.work_path):
            f_path = os.path.join(self.work_path, f)
            if os.path.islink(f_path):
                os.remove(f_path)

    def collate(self):
        pass
