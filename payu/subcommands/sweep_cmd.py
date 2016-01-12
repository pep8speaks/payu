# coding: utf-8

from payu.experiment import Experiment
from payu.laboratory import Laboratory
import payu.subcommands.args as args
import payu.debug

title = 'sweep'
parameters = {'description': 'Delete any temporary files from prior runs'}

arguments = [args.model, args.config, args.hard_sweep, args.laboratory, args.debug, args.verbose]


def runcmd(model_type, config_path, hard_sweep, lab_path, verbose, debug):

    lab = Laboratory(model_type, config_path, lab_path)
    expt = Experiment(lab)

    if verbose:
        payu.debug.verbose(True)
    if debug:
        payu.debug.dry_run(True)

    expt.sweep(hard_sweep)

runscript = runcmd
