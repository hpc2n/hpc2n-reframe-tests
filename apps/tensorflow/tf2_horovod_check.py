# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import contextlib
import reframe as rfm
import reframe.utility.osext as osext

from hpctestlib.ml.tensorflow.horovod import tensorflow_cnn_check

REFERENCE_SMALL_PERFORMANCE = {
    'dom:gpu': {
        'throughput': (1712, -0.05, None, 'images/s'),
        'throughput_per_gpu': (214, -0.05, None, 'images/s'),
    },
    'daint:gpu': {
        'throughput': (1712, -0.05, None, 'images/s'),
        'throughput_per_gpu': (214, -0.05, None, 'images/s')
    },
    'alvis:8xT4': {
        'throughput': (1233, -0.05, None, 'images/s'),
        'throughput_per_gpu': (154, -0.05, None, 'images/s'),
    },
    'alvis:2xV100': {
        'throughput': (865, -0.05, None, 'images/s'),
        'throughput_per_gpu': (432, -0.05, None, 'images/s'),
    },
    'alvis:4xA100': {
        'throughput': (559, -0.05, None, 'images/s'),
        'throughput_per_gpu': (2236, -0.05, None, 'images/s'),
    },
    'kebnekaise:gpu_1xK80': {
        'throughput': (124, -0.05, None, 'images/s'),
        'throughput_per_gpu': (62.4, -0.05, None, 'images/s'),
    },
    'kebnekaise:gpu_2xK80': {
        'throughput': (249, -0.05, None, 'images/s'),
        'throughput_per_gpu': (62.4, -0.05, None, 'images/s'),
    },
    'kebnekaise:gpu_4xK80': {
        'throughput': (494, -0.05, None, 'images/s'),
        'throughput_per_gpu': (62.4, -0.05, None, 'images/s'),
    },
    'kebnekaise:gpu_1xV100': {
        'throughput': (439, -0.05, None, 'images/s'),
        'throughput_per_gpu': (439, -0.05, None, 'images/s'),
    },
    'kebnekaise:gpu_2xV100': {
        'throughput': (832, -0.05, None, 'images/s'),
        'throughput_per_gpu': (416, -0.05, None, 'images/s'),
    },
}

REFERENCE_LARGE_PERFORMANCE = {
    'daint:gpu': {
        'throughput': (6848, -0.05, None, 'images/s'),
        'throughput_per_gpu': (214, -0.05, None, 'images/s')
    },
    'alvis:8xT4': {
        'throughput': (4847, -0.05, None, 'images/s'),
        'throughput_per_gpu': (151, -0.05, None, 'images/s')
    },
    'alvis:2xV100': {
        'throughput': (3242, -0.05, None, 'images/s'),
        'throughput_per_gpu': (405, -0.05, None, 'images/s')
    },
    'alvis:4xA100': {
        'throughput': (2233, -0.05, None, 'images/s'),
        'throughput_per_gpu': (558, -0.05, None, 'images/s')
    },
    'kebnekaise:gpu_2xK80': {
        'throughput': (493, -0.05, None, 'images/s'),
        'throughput_per_gpu': (61.6, -0.05, None, 'images/s')
    },
}


@rfm.simple_test
class snic_tensorflow_horovod_check(tensorflow_cnn_check):
    variant = parameter(['small', 'large'])
    batch_size = 64
    tags |= {'production'}
    maintainers = ['RS', 'TR', 'AS']
    valid_prog_environs = ['builtin']

    valid_systems = ['daint:gpu']
    valid_systems += ['kebnekaise:gpu_%s' % x for x in ['2xK80', '4xK80', '2xV100']]
    valid_systems += ['alvis']

    kebnekaise_single_socket = ['kebnekaise:gpu_%s' % x for x in ['1xK80', '1xV100']]

    @run_after('init')
    def set_modules(self):
        module = {
            'kebnekaise': ['fosscuda/2019b', 'Horovod/0.19.1-TensorFlow-2.1.0-Python-3.7.4'],
            'alvis': ['Horovod/0.19.1-fosscuda-2019b-TensorFlow-2.1.0-Python-3.7.4'],
            'dom': [f'Horovod/0.21.0-CrayGNU-{osext.cray_cdt_version()}-tf-2.4.0'],
            'daint': [f'Horovod/0.21.0-CrayGNU-{osext.cray_cdt_version()}-tf-2.4.0'],
        }
        self.modules = module.get(self.current_system.name)

    @run_before('run')
    def set_num_task(self):
        # Settings for various systems. num_tasks is per-variant
        self.tasks_cpu_settings = {
            'alvis:2xV100': {
                'num_cpus_per_task': 8,
                'num_tasks_per_node': 2,
                'num_tasks': {'small': 2, 'large': 8},
            },
            'alvis:4xV100': {
                'num_cpus_per_task': 8,
                'num_tasks_per_node': 4,
                'num_tasks': {'small': 4, 'large': 12},
            },
            'alvis:8xT4': {
                'num_cpus_per_task': 4,
                'num_tasks_per_node': 8,
                'num_tasks': {'small': 8, 'large': 32},
            },
            'alvis:4xA100': {
                'num_cpus_per_task': 8,
                'num_tasks_per_node': 4,
                'num_tasks': {'small': 4, 'large': 4},
            },
            'alvis:4xA40': {
                'num_cpus_per_task': 16,
                'num_tasks_per_node': 4,
                'num_tasks': {'small': 4, 'large': 32},
            },
            'kebnekaise:gpu_1xK80': {
                'num_cpus_per_task': 7,
                'num_tasks_per_node': 2,
                'num_tasks': {'small': 2},
            },
            'kebnekaise:gpu_2xK80': {
                'num_cpus_per_task': 7,
                'num_tasks_per_node': 4,
                'num_tasks': {'small': 4, 'large': 8},
            },
            'kebnekaise:gpu_4xK80': {
                'num_cpus_per_task': 7,
                'num_tasks_per_node': 8,
                'num_tasks': {'small': 8, 'large': 32},
            },
            'kebnekaise:gpu_1xV100': {
                'num_cpus_per_task': 14,
                'num_tasks_per_node': 1,
                'num_tasks': {'small': 1},
            },
            'kebnekaise:gpu_2xV100': {
                'num_cpus_per_task': 14,
                'num_tasks_per_node': 2,
                'num_tasks': {'small': 2, 'large': 4},
            },
            'dom:gpu': {
                'num_cpus_per_task': 12,
                'num_tasks_per_node': 1,
                'num_tasks': {'small': 8},
            },
            'daint:gpu': {
                'num_cpus_per_task': 12,
                'num_tasks_per_node': 1,
                'num_tasks': {'small': 8, 'large': 32},
            },
        }

        if self.variant == 'small':
            self.valid_systems += ['dom:gpu'] + self.kebnekaise_single_socket
            self.reference = REFERENCE_SMALL_PERFORMANCE
        else:
            self.reference = REFERENCE_LARGE_PERFORMANCE

        cp = self.current_partition.fullname
        self.num_tasks_per_node = self.tasks_cpu_settings.get(cp)['num_tasks_per_node']
        self.num_cpus_per_task = self.tasks_cpu_settings.get(cp)['num_cpus_per_task']
        self.num_tasks = self.tasks_cpu_settings.get(cp)['num_tasks'][self.variant]

    @run_before('run')
    def setup_run(self):
        IB_HCA = {
            'kebnekaise': 'mlx5_0',
            'alvis': 'mlx5_2',
            'dom': 'ipogif0',
            'daint': 'ipogif0',
        }

        self.variables = {
            'NCCL_DEBUG': 'INFO',
            'NCCL_IB_HCA': IB_HCA.get(self.current_system.name),
            'NCCL_IB_CUDA_SUPPORT': '1',
            'OMP_NUM_THREADS': '$SLURM_CPUS_PER_TASK',
            'OMPI_MCA_mpi_warn_on_fork': '0',
        }

    @run_after('run')
    def set_nodelist(self):
        self.mynodelist = self.job.nodelist
