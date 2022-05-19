# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm

import hpc2ntests.microbenchmarks.gpu.hooks as hooks
from hpctestlib.microbenchmarks.gpu.memory_bandwidth import *


class SystemConfigCSCS(rfm.RegressionMixin):
    @run_after('init')
    def arola_tsa_valid_prog_environs(self):
        if self.current_system.name in ['arolla', 'tsa']:
            self.valid_prog_environs = ['PrgEnv-gnu-nompi']

    # Inject external hooks
    @run_after('setup')
    def set_gpu_arch(self):
        hooks.set_gpu_arch(self)

    @run_before('run')
    def set_num_gpus_per_node(self):
        hooks.set_num_gpus_per_node(self)

    @run_after('run')
    def set_nodelist(self):
        self.mynodelist = self.job.nodelist


@rfm.simple_test
class gpu_bandwidth_check(GpuBandwidth, SystemConfigCSCS):
    valid_systems = [
        'kebnekaise:gpu_2xK80', 'kebnekaise:gpu_4xK80', 'kebnekaise:gpu_2xV100', 'alvis',
        'daint:gpu', 'dom:gpu', 'arolla:cn', 'tsa:cn',
        'ault:amdv100', 'ault:intelv100', 'ault:amda100', 'ault:amdvega'
    ]
    valid_prog_environs = ['PrgEnv-gnu', 'fosscuda']

    # Increase runtime and memory usage
    #num_copies = 2000
    #copy_size = 1073741824*2

    num_tasks = 0
    reference = {
        'kebnekaise:gpu_2xK80': {
            'h2d': (11.2, -0.1, None, 'GB/s'),
            'd2h': (11.4, -0.1, None, 'GB/s'),
            'd2d': (167.5, -0.1, None, 'GB/s')
        },
        'kebnekaise:gpu_4xK80': {
            'h2d': (11.2, -0.1, None, 'GB/s'),
            'd2h': (11.4, -0.1, None, 'GB/s'),
            'd2d': (167.5, -0.1, None, 'GB/s')
        },
        'kebnekaise:gpu_2xV100': {
            'h2d': (12.6, -0.1, None, 'GB/s'),
            'd2h': (13.5, -0.1, None, 'GB/s'),
            'd2d': (816.4, -0.1, None, 'GB/s')
        },
        'alvis:NxT4': {
            'h2d': (5.83, -0.1, None, 'GB/s'),
            'd2h': (6.14, -0.1, None, 'GB/s'),
            'd2d': (226.2, -0.1, None, 'GB/s')
        },
        'alvis:NxA40': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (533.0, -0.1, None, 'GB/s')
        },
        'alvis:NxA100_MEM256': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1234.3, -0.1, None, 'GB/s')
        },
        'alvis:NxA100_MEM512': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1234.3, -0.1, None, 'GB/s')
        },
        'alvis:NxA100_MEM768': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1234.3, -0.1, None, 'GB/s')
        },
        'alvis:NxA100fat': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1485, -0.1, None, 'GB/s')
        },
        'daint:gpu': {
            'h2d': (11.881, -0.1, None, 'GB/s'),
            'd2h': (12.571, -0.1, None, 'GB/s'),
            'd2d': (499, -0.1, None, 'GB/s')
        },
        'dom:gpu': {
            'h2d': (11.881, -0.1, None, 'GB/s'),
            'd2h': (12.571, -0.1, None, 'GB/s'),
            'd2d': (499, -0.1, None, 'GB/s')
        },
        'tsa:cn': {
            'h2d': (12.000, -0.1, None, 'GB/s'),
            'd2h': (12.416, -0.1, None, 'GB/s'),
            'd2d': (777.000, -0.1, None, 'GB/s')
        },
        'ault:amda100': {
            'h2d': (25.500, -0.1, None, 'GB/s'),
            'd2h': (26.170, -0.1, None, 'GB/s'),
            'd2d': (1322.500, -0.1, None, 'GB/s')
        },
        'ault:amdv100': {
            'h2d': (13.189, -0.1, None, 'GB/s'),
            'd2h': (13.141, -0.1, None, 'GB/s'),
            'd2d': (777.788, -0.1, None, 'GB/s')
        },
        'ault:intelv100': {
            'h2d': (13.183, -0.1, None, 'GB/s'),
            'd2h': (13.411, -0.1, None, 'GB/s'),
            'd2d': (778.200, -0.1, None, 'GB/s')
        },
        'ault:amdvega': {
            'h2d': (14, -0.1, None, 'GB/s'),
            'd2h': (14, -0.1, None, 'GB/s'),
            'd2d': (575.700, -0.1, None, 'GB/s')
        },
    }
    tags = {'diagnostic', 'mch', 'craype', 'benchmark'}
    maintainers = ['AJ', 'SK']


@rfm.simple_test
class gpu_bandwidth_d2d_check(GpuBandwidthD2D, SystemConfigCSCS):
    valid_systems = [
        'kebnekaise:gpu_2xK80', 'kebnekaise:gpu_4xK80', 'kebnekaise:gpu_2xV100', 'alvis',
        'tsa:cn', 'arola:cn', 'ault:amdv100', 'ault:intelv100',
        'ault:amda100', 'ault:amdvega'
    ]
    valid_prog_environs = ['PrgEnv-gnu', 'fosscuda']
    num_tasks = 0
    tags = {'diagnostic', 'mch', 'craype', 'benchmark'}
    maintainers = ['AJ', 'SK']

    @run_before('performance')
    def set_references(self):
        '''The references depend on the parameter p2p.'''

        if self.p2p:
            self.reference = {
                'kebnekaise:gpu_2xK80': {
                    'bw':   (163, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_4xK80': {
                    'bw':   (163, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_2xV100': {
                    'bw':   (9.55, -0.05, None, 'GB/s'),
                },
                'alvis:NxA40': {
                    'bw': (54.3, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100_MEM256': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100_MEM512': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100_MEM768': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100fat': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'tsa:cn': {
                    'bw':   (163, -0.05, None, 'GB/s'),
                },
                'arola:cn': {
                    'bw':   (163, -0.05, None, 'GB/s'),
                },
                'ault:amda100': {
                    'bw':   (282.07, -0.1, None, 'GB/s'),
                },
                'ault:amdv100': {
                    'bw':   (5.7, -0.1, None, 'GB/s'),
                },
                'ault:intelv100': {
                    'bw':   (31.0, -0.1, None, 'GB/s'),
                },
                'ault:amdvega': {
                    'bw':   (11.75, -0.1, None, 'GB/s'),
                },
            }
        else:
            self.reference = {
                'kebnekaise:gpu_2xK80': {
                    'bw': (29.77, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_4xK80': {
                    'bw': (64.92, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_2xV100': {
                    'bw': (11.36, -0.05, None, 'GB/s'),
                },
                'alvis:NxA40': {
                    'bw': (63.7, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100_MEM256': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100_MEM512': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100_MEM768': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'alvis:NxA100fat': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'tsa:cn': {
                    'bw': (74, -0.05, None, 'GB/s'),
                },
                'arola:cn': {
                    'bw': (74, -0.05, None, 'GB/s'),
                },
                'ault:amda100': {
                    'bw': (54.13, -0.1, None, 'GB/s'),
                },
                'ault:amdv100': {
                    'bw': (7.5, -0.1, None, 'GB/s'),
                },
                'ault:intelv100': {
                    'bw': (33.6, -0.1, None, 'GB/s'),
                },
                'ault:amdvega': {
                    'bw':   (11.75, -0.1, None, 'GB/s'),
                },
            }
