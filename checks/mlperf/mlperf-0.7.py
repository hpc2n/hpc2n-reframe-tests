# Copyright 2021 High Performance Computing Center North (HPC2N)
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.osext as osext

from reframe.core.backends import getlauncher

class MLPerfInference_07_Base(rfm.RunOnlyRegressionTest):

    def __init__(self):
        self.descr = 'MLPerf Inference 0.7'

        self.valid_systems = ['kebnekaise:%s' % x for x in ['2xK80', '4xK80', '2xV100']]
        self.valid_systems += ['alvis']

        self.kebnekaise_single_socket = ['kebnekaise:%s' % x for x in ['1xK80', '1xV100']]
        self.valid_systems += self.kebnekaise_single_socket

        # This test uses no modules, just singularity from OS packages
        self.valid_prog_environs = ['builtin']

        self.time_limit = '1h'

        # Create some temp dirs where it can write stuff
        self.prerun_cmds = [
            'mkdir -p $TMPDIR/{dali,engines,logs,measurements,result,unet,bert}',
        ]

        dataset_base = '/mimer/NOBACKUP/groups/c3-staff/datasets/mlperf-v0.7-inference'
        # This is a container run
        self.container_platform = 'Singularity'
        self.container_platform.image = '/cephyr/users/akesa/Alvis/reframe/test-runs/mlperf-inference-lni-latest-trt-7234-cudnn-811.sif'
        self.container_platform.mount_points = [
            #(dataset_base + "/Language Processing/build", "/work/build"),
            (dataset_base + "/Language Processing", "/dataset"),
            (dataset_base + "/nvidia/models", "/work/build/models"),
            (dataset_base + "/nvidia/data", "/work/build/data"),
            (dataset_base + "/nvidia/preprocessed_data", "/work/build/preprocessed_data"),
            ("/cephyr/users/akesa/Alvis/reframe/test-runs/mlperf/0.7/configs", "/work/configs"),
            ("/cephyr/users/akesa/Alvis/reframe/test-runs/mlperf/0.7/system_list.py", "/work/code/common/system_list.py"),
            ("/cephyr/users/akesa/Alvis/reframe/test-runs/mlperf/0.7/main.py", "/work/code/main.py"),
            ("$TMPDIR/measurements", "/work/measurements"),
            ("$TMPDIR/engines", "/work/build/engines"),
            ("$TMPDIR/logs", "/work/build/logs"),
            ("$TMPDIR/result", "/work/build/result"),
        ]
        if self.benchmark == 'rnnt':
            self.container_platform.mount_points.append(("$TMPDIR/dali", "/work/build/bin/dali"))
        if self.benchmark == '3d-unet':
            self.container_platform.mount_points.append(("$TMPDIR/unet", "/work/build/brats_postprocessed_data"))
            self.time_limit = '6h'
        if self.benchmark == 'bert':
            self.container_platform.mount_points.append(("$TMPDIR/bert", "/work/build/bert"))
            # bert takes ~2h
            self.time_limit = '6h'
        if self.benchmark == 'resnet50':
            self.time_limit = '2h'

        self.container_platform.options = ['--pwd /work']
        self.container_platform.command = (
            'make run RUN_ARGS="--benchmarks=%s --scenarios=offline --config_ver=default --test_mode=SubmissionRun"' % self.benchmark
        )
        self.container_platform.with_cuda = True

        self.sanity_patterns = sn.all([
            sn.assert_found(rf'Scenario\s*:\s*Offline', self.stdout),
            sn.assert_found(rf'Mode\s*:\s*Submission', self.stdout),
            sn.assert_found(rf'Result\s+is\s*:\s*VALID', self.stdout),
            sn.assert_found(rf'Min\s+duration\s+satisfied\s*:\s*Yes', self.stdout),
            sn.assert_found(rf'Min\s+queries\s+satisfied\s*:\s*Yes', self.stdout),
            sn.assert_found(rf'Accuracy\s+test\s+PASSED', self.stdout),

        ])

        self.perf_patterns = {
            'samples_per_second': sn.extractsingle(
                rf'%s:\s+Samples\s+per\s+second:\s*(?P<samples_per_second>\S+)\s+and\s+Result\s+is\s*:\s*VALID' % self.benchmark,
                self.stdout, 'samples_per_second', float),
            'accuracy': sn.extractsingle(
                rf'%s:\s+Accuracy\s+=\s+(?P<accuracy>[.\d]+),\s+Threshold\s+=\s+' % self.benchmark, self.stdout, 'accuracy', float),
        }


    # Don't use srun for this
    @run_after('setup')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()


@rfm.simple_test
class MLPerfInference_07(MLPerfInference_07_Base):
    # resnet50 ssd-resnet34 bert dlrm rnnt 3d-unet
    benchmark = parameter(['bert', 'resnet50', 'ssd-resnet34', 'rnnt', '3d-unet'])

    def __init__(self):
        super().__init__()
        references = {
            'bert': {
                'alvis:8xT4': {
                    'samples_per_second': (3456, -0.05, None, 'samples/s'),
                    'accuracy': (90.874, -0.01, None, 'accuracy'),
                },
                'alvis:4xA40': {
                    'samples_per_second': (6572, -0.00, None, 'samples/s'),
                    'accuracy': (90.874, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM256': {
                    'samples_per_second': (13465, -0.00, None, 'samples/s'),
                    'accuracy': (90.874, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM512': {
                    'samples_per_second': (13465, -0.00, None, 'samples/s'),
                    'accuracy': (90.874, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100fat': {
                    'samples_per_second': (13465, -0.00, None, 'samples/s'),
                    'accuracy': (90.874, -0.01, None, 'accuracy'),
                },
            },
            'resnet50': {
                'alvis:8xT4': {
                    'samples_per_second': (46130, -0.05, None, 'samples/s'),
                    'accuracy': (76.46, -0.01, None, 'accuracy'),
                },
                'alvis:4xA40': {
                    'samples_per_second': (74230, -0.00, None, 'samples/s'),
                    'accuracy': (76.46, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM256': {
                    'samples_per_second': (150512, -0.00, None, 'samples/s'),
                    'accuracy': (76.46, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM512': {
                    'samples_per_second': (150512, -0.00, None, 'samples/s'),
                    'accuracy': (76.46, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100fat': {
                    'samples_per_second': (150512, -0.00, None, 'samples/s'),
                    'accuracy': (76.46, -0.01, None, 'accuracy'),
                },
            },
            'ssd-resnet34': {
                'alvis:8xT4': {
                    'samples_per_second': (1086, -0.05, None, 'samples/s'),
                    'accuracy': (20.0, -0.01, None, 'accuracy'),
                },
                'alvis:4xA40': {
                    'samples_per_second': (1877, -0.00, None, 'samples/s'),
                    'accuracy': (20.0, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM256': {
                    'samples_per_second': (3947, -0.00, None, 'samples/s'),
                    'accuracy': (20.0, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM512': {
                    'samples_per_second': (3947, -0.00, None, 'samples/s'),
                    'accuracy': (20.0, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100fat': {
                    'samples_per_second': (3947, -0.00, None, 'samples/s'),
                    'accuracy': (20.0, -0.01, None, 'accuracy'),
                },
            },
            'dlrm': {
                'alvis:8xT4': {
                    'samples_per_second': (0, -0.05, None, 'samples/s'),
                    'accuracy': (80.25, -0.01, None, 'accuracy'),
                },
            },
            'rnnt': {
                'alvis:8xT4': {
                    'samples_per_second': (10630, -0.05, None, 'samples/s'),
                    'accuracy': (100-7.45225, -0.01, None, 'accuracy'),
                },
                'alvis:4xA40': {
                    'samples_per_second': (24200, -0.00, None, 'samples/s'),
                    'accuracy': (100-7.45225, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM256': {
                    'samples_per_second': (41722, -0.00, None, 'samples/s'),
                    'accuracy': (100-7.45225, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM512': {
                    'samples_per_second': (41722, -0.00, None, 'samples/s'),
                    'accuracy': (100-7.45225, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100fat': {
                    'samples_per_second': (41722, -0.00, None, 'samples/s'),
                    'accuracy': (100-7.45225, -0.01, None, 'accuracy'),
                },
            },
            '3d-unet': {
                'alvis:8xT4': {
                    'samples_per_second': (53, -0.05, None, 'samples/s'),
                    'accuracy': (0.853, -0.01, None, 'accuracy'),
                },
                'alvis:4xA40': {
                    'samples_per_second': (123, -0.00, None, 'samples/s'),
                    'accuracy': (0.853, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM256': {
                    'samples_per_second': (183, -0.00, None, 'samples/s'),
                    'accuracy': (0.853, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100_MEM512': {
                    'samples_per_second': (183, -0.00, None, 'samples/s'),
                    'accuracy': (0.853, -0.01, None, 'accuracy'),
                },
                'alvis:4xA100fat': {
                    'samples_per_second': (183, -0.00, None, 'samples/s'),
                    'accuracy': (0.853, -0.01, None, 'accuracy'),
                },
            },
        }

        self.reference = references[self.benchmark]

        self.tags = {'production'}
        self.maintainers = ['AS']

