# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

import reframe as rfm
from hpctestlib.microbenchmarks.gpu.memory_bandwidth import *

import hpc2ntests.microbenchmarks.gpu.hooks as hooks


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
        'kebnekaise:gpu_2xK80', 'kebnekaise:gpu_4xK80', 'kebnekaise:gpu_2xV100',
        'kebnekaise:gpu_2xA6000', 'kebnekaise:4xA40', 'alvis', 'UmU-Cloud',
        'daint:gpu', 'dom:gpu', 'arolla:cn', 'tsa:cn',
        'ault:amdv100', 'ault:intelv100', 'ault:amda100', 'ault:amdvega'
    ]
    valid_prog_environs = ['PrgEnv-gnu', 'foss_with_cuda']

    # Increase runtime and memory usage
    #num_copies = 20
    copy_size = 2*1024**3-1 # 2GB ~= 1/6 of K80 memory

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
        'kebnekaise:4xA40': {
            'h2d': (12, -0.1, None, 'GB/s'),
            'd2h': (13, -0.1, None, 'GB/s'),
            'd2d': (533.0, -0.1, None, 'GB/s')
        },
        'kebnekaise:gpu_2xA6000': {
            'h2d': (12, -0.1, None, 'GB/s'),
            'd2h': (13, -0.1, None, 'GB/s'),
            'd2d': (636, -0.1, None, 'GB/s')
        },
        'UmU-Cloud:default': {
            'h2d': (25, -0.1, None, 'GB/s'),
            'd2h': (24, -0.1, None, 'GB/s'),
            'd2d': (1400, -0.1, None, 'GB/s')
        },
        'alvis:8xT4': {
            'h2d': (5.83, -0.1, None, 'GB/s'),
            'd2h': (6.14, -0.1, None, 'GB/s'),
            'd2d': (226.2, -0.1, None, 'GB/s')
        },
        'alvis:4xA40': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (533.0, -0.1, None, 'GB/s')
        },
        'alvis:4xA100_MEM256': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1234.3, -0.1, None, 'GB/s')
        },
        'alvis:4xA100_MEM512': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1234.3, -0.1, None, 'GB/s')
        },
        'alvis:4xA100_MEM768': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1234.3, -0.1, None, 'GB/s')
        },
        'alvis:4xA100fat': {
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
        'kebnekaise:gpu_2xK80', 'kebnekaise:gpu_4xK80', 'kebnekaise:gpu_2xV100',
        'kebnekaise:gpu_2xA6000', 'kebnekaise:4xA40', 'alvis',
        'tsa:cn', 'arola:cn', 'ault:amdv100', 'ault:intelv100',
        'ault:amda100', 'ault:amdvega'
    ]
    valid_prog_environs = ['PrgEnv-gnu', 'foss_with_cuda']
    num_tasks = 0
    tags = {'diagnostic', 'mch', 'craype', 'benchmark'}
    maintainers = ['AJ', 'SK']

    # Increase runtime and memory usage
    #num_copies = 20
    copy_size = 2*1024**3-1 # 2GB ~= 1/6 of K80 memory

    @run_before('performance')
    def set_references(self):
        '''The references depend on the parameter p2p.'''

        if self.p2p:
            self.reference = {
                'kebnekaise:gpu_2xK80': {
                    'bw':   (163, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_4xK80': {
                    'bw':   (9.5, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_2xV100': {
                    'bw':   (9.55, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_2xA6000': {
                    'bw':   (636, -0.05, None, 'GB/s'),
                },
                'kebnekaise:4xA40': {
                    'bw': (9.5, -0.05, None, 'GB/s'),
                },
                'alvis:4xA40': {
                    'bw': (54.3, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100_MEM256': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100_MEM512': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100_MEM768': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100fat': {
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
                    'bw': (30, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_4xK80': {
                    'bw': (65, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_2xV100': {
                    'bw': (12, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gpu_2xA6000': {
                    'bw': (12, -0.05, None, 'GB/s'),
                },
                'kebnekaise:4xA40': {
                    'bw': (31, -0.05, None, 'GB/s'),
                },
                'alvis:4xA40': {
                    'bw': (63.7, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100_MEM256': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100_MEM512': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100_MEM768': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
                'alvis:4xA100fat': {
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
