# Copyright 2021 High Performance Computing Center North (HPC2N)
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.osext as osext

from reframe.core.backends import getlauncher

@rfm.simple_test
class MLPerfBertInference(rfm.RunOnlyRegressionTest):

    def __init__(self):
        self.descr = 'MLPerf Bert'

        self.valid_systems = ['kebnekaise:gpu_%s' % x for x in ['2xK80', '4xK80', '2xV100']]
        self.valid_systems += ['alvis']

        self.kebnekaise_single_socket = ['kebnekaise:gpu_%s' % x for x in ['1xK80', '1xV100']]
        self.valid_systems += self.kebnekaise_single_socket

        # This test uses no modules, just singularity from OS packages
        self.valid_prog_environs = ['builtin']

        self.time_limit = '1h'
        # This is a container run
        self.container_platform = 'Singularity'
        self.container_platform.image = '/cephyr/NOBACKUP/priv/c3-alvis/mlperf-inference-lni-latest.sif'
        self.container_platform.mount_points = [
            ("/cephyr/NOBACKUP/priv/c3-alvis/datasets/mlperf-v0.7-inference/Language Processing/measurements", "/work/measurements"),
            ("/cephyr/NOBACKUP/priv/c3-alvis/datasets/mlperf-v0.7-inference/Language Processing/build", "/work/build"),
            ("/cephyr/NOBACKUP/priv/c3-alvis/datasets/mlperf-v0.7-inference/Language Processing", "/dataset"),
            ("/cephyr/NOBACKUP/priv/c3-alvis/datasets/mlperf-v0.7-inference/nvidia/models", "/work/build/models"),
            ("/cephyr/NOBACKUP/priv/c3-alvis/datasets/mlperf-v0.7-inference/nvidia/data", "/work/build/data"),
            ("/cephyr/NOBACKUP/priv/c3-alvis/datasets/mlperf-v0.7-inference/nvidia/preprocessed_data", "/work/build/preprocessed_data"),
        ]
        self.container_platform.options = ['--pwd /work']
        self.container_platform.command = (
            'make run RUN_ARGS="--benchmarks=bert --scenarios=offline --config_ver=default --test_mode=PerformanceOnly"'
        )
        self.container_platform.with_cuda = True

        self.reference = {
            'alvis:8xT4': {
                'samples_per_second': (3456, -0.05, None, 'samples/s'),
            },
        }

        self.sanity_patterns = sn.all([
            sn.assert_found(rf'Mode\s*:\s*Performance', self.stdout),
            sn.assert_found(rf'Result\s+is\s*:\s*VALID', self.stdout),
            sn.assert_found(rf'Min\s+duration\s+satisfied\s*:\s*Yes', self.stdout),
            sn.assert_found(rf'Min\s+queries\s+satisfied\s*:\s*Yes', self.stdout),

        ])

        self.perf_patterns = {
            'samples_per_second': sn.extractsingle(
                rf'bert:\s*Samples\s+per\s+second:\s*(?P<samples_per_second>\S+)\s+and\s+Result\s+is\s*:\s*VALID',
                self.stdout, 'samples_per_second', float),
        }

        self.tags = {'production'}
        self.maintainers = ['AS']

    # Don't use srun for this
    @run_after('setup')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    @run_after('run')
    def set_nodelist(self):
        self.mynodelist = self.job.nodelist
