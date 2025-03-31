# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

import reframe as rfm
from hpctestlib.microbenchmarks.gpu.memory_bandwidth import *

sys.path.append(os.path.abspath(os.path.join(__file__, '../../..')))
import microbenchmarks.gpu.hooks as hooks


class SystemConfigHPC2N(rfm.RegressionMixin):
    # Inject external hooks
    @run_after('setup')
    def set_gpu_arch(self):
        hooks.set_gpu_arch(self)

    @run_before('run')
    def set_num_gpus_per_node(self):
        hooks.set_num_gpus_per_node(self)


@rfm.simple_test
class gpu_bandwidth_check(GpuBandwidth, SystemConfigHPC2N):
    valid_systems = ['+gpu']
    valid_prog_environs = ['+cuda', '+hip']


    tags = {'diagnostic', 'mch', 'benchmark', 'maintenance'}
    maintainers = ['AJ', 'SK', 'AS']

    # Increase runtime and memory usage
    #num_copies = 20
    copy_size = 4*1024**3 # 4GB ~= 1/3 of K80 memory

    num_tasks = 0

    reference = {
        'kebnekaise:2xK80': {
            'h2d': (11.2, -0.1, None, 'GB/s'),
            'd2h': (11.4, -0.1, None, 'GB/s'),
            'd2d': (167.5, -0.1, None, 'GB/s')
        },
        'kebnekaise:4xK80': {
            'h2d': (11.2, -0.1, None, 'GB/s'),
            'd2h': (11.4, -0.1, None, 'GB/s'),
            'd2d': (167.5, -0.1, None, 'GB/s')
        },
        'kebnekaise:2xV100': {
            'h2d': (12.6, -0.1, None, 'GB/s'),
            'd2h': (13.5, -0.1, None, 'GB/s'),
            'd2d': (816.4, -0.1, None, 'GB/s')
        },
        'kebnekaise:4xA40': {
            'h2d': (12, -0.1, None, 'GB/s'),
            'd2h': (13, -0.1, None, 'GB/s'),
            'd2d': (533.0, -0.1, None, 'GB/s')
        },
        'kebnekaise:2xA6000': {
            'h2d': (12, -0.1, None, 'GB/s'),
            'd2h': (13, -0.1, None, 'GB/s'),
            'd2d': (636, -0.1, None, 'GB/s')
        },
        'kebnekaise:2xA100': {
            'h2d': (22, -0.1, None, 'GB/s'),
            'd2h': (25, -0.1, None, 'GB/s'),
            'd2d': (1435, -0.1, None, 'GB/s')
        },
        'kebnekaise:gen4-l40s': {
            'h2d': (25, -0.1, None, 'GB/s'),
            'd2h': (25, -0.1, None, 'GB/s'),
            'd2d': (626, -0.1, None, 'GB/s')
        },
        'kebnekaise:gen4-h100': {
            'h2d': (48, -0.1, None, 'GB/s'),
            'd2h': (47, -0.1, None, 'GB/s'),
            'd2d': (2472, -0.1, None, 'GB/s')
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
        'alvis:4xA100fat': {
            'h2d': (23.57, -0.1, None, 'GB/s'),
            'd2h': (24.53, -0.1, None, 'GB/s'),
            'd2d': (1485, -0.1, None, 'GB/s')
        },
    }


@rfm.simple_test
class gpu_bandwidth_d2d_check(GpuBandwidthD2D, SystemConfigHPC2N):
    valid_systems = ['+gpu']
    valid_prog_environs = ['+cuda', '+hip']

    tags = {'diagnostic', 'mch', 'benchmark', 'maintenance'}
    maintainers = ['AJ', 'SK', 'AS']

    # Increase runtime and memory usage
    #num_copies = 20
    copy_size = 4*1024**3 # 4GB ~= 1/3 of K80 memory

    num_tasks = 0

    @run_before('performance')
    def set_references(self):
        '''The references depend on the parameter p2p.'''

        if self.p2p:
            self.reference = {
                'kebnekaise:2xK80': {
                    'bw':   (163, -0.05, None, 'GB/s'),
                },
                'kebnekaise:4xK80': {
                    'bw':   (9.5, -0.05, None, 'GB/s'),
                },
                'kebnekaise:2xV100': {
                    'bw':   (9.55, -0.05, None, 'GB/s'),
                },
                'kebnekaise:2xA6000': {
                    'bw':   (636, -0.05, None, 'GB/s'),
                },
                'kebnekaise:4xA40': {
                    'bw': (9.5, -0.05, None, 'GB/s'),
                },
                'kebnekaise:2xA100': {
                    'bw': (10.5, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gen4-l40s': {
                    'bw': (372, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gen4-h100': {
                    'bw': (372, -0.05, None, 'GB/s'),
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
                'alvis:4xA100fat': {
                    'bw': (262.69, -0.05, None, 'GB/s'),
                },
            }
        else:
            self.reference = {
                'kebnekaise:2xK80': {
                    'bw': (30, -0.05, None, 'GB/s'),
                },
                'kebnekaise:4xK80': {
                    'bw': (65, -0.05, None, 'GB/s'),
                },
                'kebnekaise:2xV100': {
                    'bw': (12, -0.05, None, 'GB/s'),
                },
                'kebnekaise:2xA6000': {
                    'bw': (12, -0.05, None, 'GB/s'),
                },
                'kebnekaise:4xA40': {
                    'bw': (31, -0.05, None, 'GB/s'),
                },
                'kebnekaise:2xA100': {
                    'bw': (17, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gen4-l40s': {
                    'bw': (10, -0.05, None, 'GB/s'),
                },
                'kebnekaise:gen4-h100': {
                    'bw': (70, -0.05, None, 'GB/s'),
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
                'alvis:4xA100fat': {
                    'bw': (61.8, -0.05, None, 'GB/s'),
                },
            }
