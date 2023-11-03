# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause


import reframe as rfm
from hpctestlib.microbenchmarks.gpu.gpu_burn import gpu_burn_check


class gpu_burn_check_base(gpu_burn_check):
    valid_prog_environs = ['foss_with_cuda']
    duration = 120

    # Since gpu_burn_check sets use_dp in "run_after('init')" we need to set it before that gets run
    def __init__(self):
        if self.precision == 'double':
            self.use_dp = True
        else:
            self.use_dp = False
        super().__init__()

    @run_before('run')
    def set_exclusive_access(self):
        self.time_limit = '1h'

        cs = self.current_system.name
        if cs == 'alvis':
            self.exclusive_access = False

@rfm.simple_test
class gpu_burn_check(gpu_burn_check_base):
    '''Run both single and double precision tests'''
    precision = parameter(['double', 'single'])

    tags = {'diagnostic', 'benchmark', 'maintenance'}
    maintainers = ['AJ', 'TM', 'AS']

    references = {
        'double': {
            'kebnekaise:2xK80': {
                'gpu_perf_min': (1000, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:4xK80': {
                'gpu_perf_min': (1000, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:2xV100': {
                'gpu_perf_min': (6300, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:2xA6000': {
                'gpu_perf_min': (538, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:4xA40': {
                # Teoretical peak is 584.6 Gflops/s
                'gpu_perf_min': (488, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:2xA100': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            'alvis:8xT4': {
                'gpu_perf_min': (250, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xV100': {
                'gpu_perf_min': (6800, -0.10, None, 'Gflop/s'),
            },
            'UmU-Cloud:default': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xA40': {
                'gpu_perf_min': (488, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xA100_MEM256': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xA100_MEM512': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xA100fat': {
                'gpu_perf_min': (18500, -0.10, None, 'Gflop/s'),
            },
            '*': {'gpu_temp_max': (0, None, None, 'degC')},
        },
        'single': {
            'kebnekaise:2xK80': {
                'gpu_perf_min': (2300, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:2xV100': {
                'gpu_perf_min': (13400, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:2xA6000': {
                'gpu_perf_min': (21000, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:4xA40': {
                'gpu_perf_min': (19500, -0.10, None, 'Gflop/s'),
            },
            'kebnekaise:2xA100': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            'UmU-Cloud:default': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            'alvis:8xT4': {
                'gpu_perf_min': (4000, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xV100': {
                'gpu_perf_min': (14300, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xA40': {
                'gpu_perf_min': (19200, -0.10, None, 'Gflop/s'),
            },
            'alvis:4xA100_MEM256': {
                'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
            },
            '*': {'gpu_temp_max': (0, None, None, 'degC')},
        },
    }

    @run_after('setup')
    def set_reference(self):
        self.reference = self.references[self.precision]

