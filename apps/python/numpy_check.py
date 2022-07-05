# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm

from hpctestlib.python.numpy.numpy_ops import numpy_ops_check
from reframe.utility import find_modules

class snic_numpy_test(numpy_ops_check):
    valid_prog_environs = ['builtin']
    num_tasks_per_node = 1
    use_multithreading = False
    all_ref = {
        'haswell@12c': {
            'dot': (0.4, None, 0.05, 's'),
            'svd': (0.37, None, 0.05, 's'),
            'cholesky': (0.12, None, 0.05, 's'),
            'eigendec': (3.5, None, 0.05, 's'),
            'inv': (0.21, None, 0.05, 's'),
        },
        'broadwell@14c': {
            'dot': (0.3, None, 0.05, 's'),
            'svd': (0.35, None, 0.05, 's'),
            'cholesky': (0.1, None, 0.05, 's'),
            'eigendec': (4.14, None, 0.05, 's'),
            'inv': (0.16, None, 0.05, 's'),
        },
        'broadwell@28c': {
            'dot': (0.3, None, 0.05, 's'),
            'svd': (0.35, None, 0.05, 's'),
            'cholesky': (0.1, None, 0.05, 's'),
            'eigendec': (4.14, None, 0.05, 's'),
            'inv': (0.16, None, 0.05, 's'),
        },
        'broadwell@36c': {
            'dot': (0.3, None, 0.05, 's'),
            'svd': (0.35, None, 0.05, 's'),
            'cholesky': (0.1, None, 0.05, 's'),
            'eigendec': (4.14, None, 0.05, 's'),
            'inv': (0.16, None, 0.05, 's'),
        },
        'skylake@14c': {
            'dot': (0.3, None, 0.05, 's'),
            'svd': (0.35, None, 0.05, 's'),
            'cholesky': (0.1, None, 0.05, 's'),
            'eigendec': (4.14, None, 0.05, 's'),
            'inv': (0.16, None, 0.05, 's'),
        },
        'skylake@28c': {
            'dot': (0.3, None, 0.05, 's'),
            'svd': (0.35, None, 0.05, 's'),
            'cholesky': (0.1, None, 0.05, 's'),
            'eigendec': (4.14, None, 0.05, 's'),
            'inv': (0.16, None, 0.05, 's'),
        },
    }
    tags = {'production'}
    maintainers = ['RS', 'TR', 'AS']

    @run_after('init')
    def process_module_info(self):
        s, e, m = self.module_info
        self.valid_prog_environs = [e]
        self.modules = [m]

    @run_after('setup')
    def set_num_cpus_per_task(self):
        self.num_cpus_per_task = self.current_partition.processor.num_cores
        self.variables = {
            'OMP_NUM_THREADS': str(self.num_cpus_per_task),
        }

    @run_before('performance')
    def set_perf_ref(self):
        arch = self.current_partition.processor.arch
        pname = self.current_partition.fullname
        num_cores = self.current_partition.processor.num_cores
        self.reference = {
            pname: self.all_ref[f'{arch}@{num_cores}c']
        }

@rfm.simple_test
class c3se_numpy_test(snic_numpy_test):
    module_info = parameter(find_modules('SciPy-bundle', { r'.*': 'builtin' }))
    valid_systems = ['alvis']

@rfm.simple_test
class hpc2n_numpy_test(snic_numpy_test):
    module_info = parameter(find_modules('SciPy-bundle'))
    valid_systems = ['kebnekaise']
