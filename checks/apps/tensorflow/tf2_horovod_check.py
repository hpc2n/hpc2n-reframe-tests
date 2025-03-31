# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import contextlib
import reframe as rfm
import reframe.utility.osext as osext

from hpctestlib.ml.tensorflow.horovod import tensorflow_cnn_check

import os,sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../../..')))
import microbenchmarks.gpu.hooks as hooks

REFERENCE_SMALL_PERFORMANCE = {
    'alvis:8xT4': {
        'throughput_total': (1233, -0.05, None, 'images/s'),
        'throughput_iteration': (154, -0.05, None, 'images/s'),
    },
    'alvis:2xV100': {
        'throughput_total': (865, -0.05, None, 'images/s'),
        'throughput_iteration': (432, -0.05, None, 'images/s'),
    },
    'alvis:4xA100_MEM256': {
        'throughput_total': (2000, -0.05, None, 'images/s'),
        'throughput_iteration': (500, -0.05, None, 'images/s'),
    },
    'alvis:4xA100_MEM512': {
        'throughput_total': (2000, -0.05, None, 'images/s'),
        'throughput_iteration': (500, -0.05, None, 'images/s'),
    },
    'alvis:4xA100fat': {
        'throughput_total': (2000, -0.05, None, 'images/s'),
        'throughput_iteration': (500, -0.05, None, 'images/s'),
    },
    'kebnekaise:2xK80': {
        'throughput_total': (249, -0.05, None, 'images/s'),
        'throughput_iteration': (62, -0.05, None, 'images/s'),
    },
    'kebnekaise:4xK80': {
        'throughput_total': (499, -0.05, None, 'images/s'),
        'throughput_iteration': (62, -0.05, None, 'images/s'),
    },
    'kebnekaise:2xV100': {
        'throughput_total': (832, -0.05, None, 'images/s'),
        'throughput_iteration': (416, -0.05, None, 'images/s'),
    },
}

REFERENCE_LARGE_PERFORMANCE = {
    'alvis:8xT4': {
        'throughput_total': (1208, -0.05, None, 'images/s'),
        'throughput_iteration': (151, -0.05, None, 'images/s')
    },
    'alvis:2xV100': {
        'throughput_total': (3242, -0.05, None, 'images/s'),
        'throughput_iteration': (405, -0.05, None, 'images/s')
    },
    'alvis:4xA100_MEM256': {
        'throughput_total': (2000, -0.05, None, 'images/s'),
        'throughput_iteration': (500, -0.05, None, 'images/s')
    },
    'alvis:4xA100_MEM512': {
        'throughput_total': (2000, -0.05, None, 'images/s'),
        'throughput_iteration': (500, -0.05, None, 'images/s')
    },
    'alvis:4xA100fat': {
        'throughput_total': (2000, -0.05, None, 'images/s'),
        'throughput_iteration': (500, -0.05, None, 'images/s')
    },
    'kebnekaise:2xK80': {
        'throughput_total': (992, -0.05, None, 'images/s'),
        'throughput_iteration': (62, -0.05, None, 'images/s')
    },
    'kebnekaise:2xV100': {
        'throughput_total': (3328, -0.05, None, 'images/s'),
        'throughput_iteration': (416, -0.05, None, 'images/s')
    },
}


@rfm.simple_test
class snic_tensorflow_horovod_check(tensorflow_cnn_check):
    variant = parameter(['small', 'large'])
    batch_size = 64
    tags |= {'production'}
    maintainers = ['RS', 'TR', 'AS']
    valid_prog_environs = ['builtin']

    valid_systems = ['kebnekaise:%s' % x for x in ['2xK80', '4xK80', '2xV100']]
    valid_systems += ['alvis']

    @run_after('init')
    def set_modules(self):
        module = {
            'kebnekaise': ['fosscuda/2019b', 'Horovod/0.19.1-TensorFlow-2.1.0-Python-3.7.4'],
            'alvis': ['Horovod/0.23.0-fosscuda-2020b-TensorFlow-2.5.0'],
        }
        self.modules = module.get(self.current_system.name, [])

    @run_after('init')
    def prepare_test(self):
        horovod_version = {
            'kebnekaise': 'v0.19.1',
            'alvis': 'v0.23.0',
        }
        self.benchmark_version = horovod_version.get(self.current_system.name, '')
        super().prepare_test()

    @run_before('run')
    def set_num_gpus_per_node(self):
        hooks.set_num_gpus_per_node(self)

    @run_before('run')
    def set_num_task(self):
        # Settings for various systems. num_tasks is per-variant
        self.tasks_cpu_settings = {
            'alvis:2xV100': {
                'cpus_per_node': 16,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'alvis:4xV100': {
                'cpus_per_node': 32,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'alvis:8xT4': {
                'cpus_per_node': 32,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'alvis:4xA40': {
                'cpus_per_node': 64,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'alvis:4xA100_MEM256': {
                'cpus_per_node': 64,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'alvis:4xA100_MEM512': {
                'cpus_per_node': 64,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'alvis:4xA100fat': {
                'cpus_per_node': 64,
                'num_nodes': {'small': 1, 'large': 1},
            },
            'kebnekaise:2xK80': {
                'cpus_per_node': 28,
                'num_nodes': {'small': 1, 'large': 4},
            },
            'kebnekaise:4xK80': {
                'cpus_per_node': 28,
                'num_nodes': {'small': 1, 'large': 2},
            },
            'kebnekaise:2xV100': {
                'cpus_per_node': 28,
                'num_nodes': {'small': 1, 'large': 4},
            },
        }

        if self.variant == 'small':
            self.reference = REFERENCE_SMALL_PERFORMANCE
        else:
            self.reference = REFERENCE_LARGE_PERFORMANCE

        cp = self.current_partition.fullname
        # Use one task per GPU
        self.num_tasks_per_node = self.num_gpus_per_node
        self.num_cpus_per_task = int(self.tasks_cpu_settings.get(cp)['cpus_per_node'] / self.num_tasks_per_node)
        self.num_tasks = self.tasks_cpu_settings.get(cp)['num_nodes'][self.variant] * self.num_tasks_per_node

    @run_before('run')
    def setup_run(self):
        IB_HCA = {
            'kebnekaise': 'mlx5_0',
            'alvis': 'mlx5_0',
        }

        self.env_vars = {
            'NCCL_DEBUG': 'INFO',
            'NCCL_IB_HCA': IB_HCA.get(self.current_system.name),
            'NCCL_IB_CUDA_SUPPORT': '1',
            'OMP_NUM_THREADS': '$SLURM_CPUS_PER_TASK',
            'OMPI_MCA_mpi_warn_on_fork': '0',
        }
