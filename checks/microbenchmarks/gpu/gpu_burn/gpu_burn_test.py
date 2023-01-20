# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause


import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.osext as osext
from reframe.core.exceptions import SanityError

from hpctestlib.microbenchmarks.gpu.gpu_burn import gpu_burn_check
import microbenchmarks.gpu.hooks as hooks


class gpu_burn_check_base(gpu_burn_check):
    def __init__(self):
        self.valid_systems = [
            'kebnekaise:2xK80', 'kebnekaise:4xK80', 'kebnekaise:2xV100',
            'kebnekaise:2xA6000', 'kebnekaise:4xA40',
            'UmU-Cloud',
            'alvis',
            'daint:gpu', 'dom:gpu', 'arolla:cn', 'tsa:cn', 'ault:amdv100',
            'ault:intelv100', 'ault:amda100', 'ault:amdvega'
        ]

        self.valid_prog_environs = ['foss_with_cuda']

        if self.precision == 'double':
            self.use_dp = True
        else:
            self.use_dp = False
        self.duration = 120

        self.num_tasks = 0

    # Inject external hooks
    @run_after('setup')
    def set_gpu_arch(self):
        hooks.set_gpu_arch(self)

    @run_before('run')
    def set_num_gpus_per_node(self):
        hooks.set_num_gpus_per_node(self)

    @run_before('run')
    def set_exclusive_access(self):
        self.time_limit = '1h'

        cs = self.current_system.name
        if cs == 'alvis':
            self.exclusive_access = False
        else:
            self.exclusive_access = True
        if cs in {'kebnekaise', 'alvis', 'UmU-Cloud'}:
            self.num_tasks_per_node = 1

    @run_before('performance')
    def report_slow_nodes(self):
        '''Report the base perf metrics and also all the slow nodes.'''

        # Only report the nodes that don't meet the perf reference
        with osext.change_dir(self.stagedir):
            key = f'{self.current_partition.fullname}:gpu_perf_min'
            if key in self.reference:
                regex = r'\[(\S+)\] GPU\s+\d\(OK\): (\d+) GF/s'
                nids = set(sn.extractall(regex, self.stdout, 1))

                # Get the references
                ref, lt, ut, *_ = self.reference[key]

                # Flag the slow nodes
                for nid in nids:
                    try:
                        node_perf = self.min_perf(nid)
                        val = node_perf.evaluate(cache=True)
                        sn.assert_reference(val, ref, lt, ut).evaluate()
                    except SanityError:
                        self.perf_variables[nid] = node_perf

@rfm.simple_test
class gpu_burn_check(gpu_burn_check_base):
    '''Run both single and double precision tests'''
    precision = parameter(['double', 'single'])

    def __init__(self):
        super().__init__()

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
                'alvis:NxT4': {
                    'gpu_perf_min': (250, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxV100': {
                    'gpu_perf_min': (6800, -0.10, None, 'Gflop/s'),
                },
                'UmU-Cloud:default': {
                    'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA40': {
                    'gpu_perf_min': (488, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA100_MEM256': {
                    'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA100_MEM512': {
                    'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA100_MEM768': {
                    'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA100fat': {
                    'gpu_perf_min': (18500, -0.10, None, 'Gflop/s'),
                },
                'dom:gpu': {
                    'gpu_perf_min': (4115, -0.10, None, 'Gflop/s'),
                },
                'daint:gpu': {
                    'gpu_perf_min': (4115, -0.10, None, 'Gflop/s'),
                },
                'arolla:cn': {
                    'gpu_perf_min': (5861, -0.10, None, 'Gflop/s'),
                },
                'tsa:cn': {
                    'gpu_perf_min': (5861, -0.10, None, 'Gflop/s'),
                },
                'ault:amda100': {
                    'gpu_perf_min': (15000, -0.10, None, 'Gflop/s'),
                },
                'ault:amdv100': {
                    'gpu_perf_min': (5500, -0.10, None, 'Gflop/s'),
                },
                'ault:intelv100': {
                    'gpu_perf_min': (5500, -0.10, None, 'Gflop/s'),
                },
                'ault:amdvega': {
                    'gpu_perf_min': (3450, -0.10, None, 'Gflop/s'),
                },
                '*': {'temp': (0, None, None, 'degC')},
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
                'UmU-Cloud:default': {
                    'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxT4': {
                    'gpu_perf_min': (4000, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxV100': {
                    'gpu_perf_min': (14300, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA40': {
                    'gpu_perf_min': (19200, -0.10, None, 'Gflop/s'),
                },
                'alvis:NxA100_MEM256': {
                    'gpu_perf_min': (18100, -0.10, None, 'Gflop/s'),
                },
                '*': {'temp': (0, None, None, 'degC')},
            },
        }

        self.reference = references[self.precision]

        self.tags = {'diagnostic', 'benchmark', 'craype'}
        self.maintainers = ['AJ', 'TM', 'AS']

