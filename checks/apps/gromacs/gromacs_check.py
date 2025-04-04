# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
from hpctestlib.sciapps.gromacs.benchmarks import gromacs_check


@rfm.simple_test
class hpc2n_gromacs_check(gromacs_check):
    modules = ['foss/2021b', 'GROMACS']
    maintainers = ['@victorusu']
    use_multithreading = False
    extra_resources = {
        'switches': {
            'num_switches': 1
        }
    }
    executable_opts += ['-dlb yes', '-ntomp 1', '-npme -1']
    valid_prog_environs = ['builtin']

    # HPC2N-specific parameterization
    num_nodes = parameter([1, 2, 4, 6, 8, 16], loggable=True)
    allref = {
        1: {
            'sm_60': {
                'HECBioSim/Crambin': (195.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (78.0, None, None, 'ns/day'),   # noqa: E501
                'HECBioSim/hEGFRDimer': (8.5, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (9.2, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (3.0, None, None, 'ns/day'),
            },
            'broadwell': {
                'HECBioSim/Crambin': (116.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (38.0, None, None, 'ns/day'),   # noqa: E501
                'HECBioSim/hEGFRDimer': (4.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (8.0, None, None, 'ns/day'),
            },
            'zen2': {
                'HECBioSim/Crambin': (320.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (120.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (16.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (31.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (7.0, None, None, 'ns/day'),
            },
            'x86_64_v4': {
                'HECBioSim/Crambin': (745.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (322.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (46.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (67.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (18.0, None, None, 'ns/day'),
            },
        },
        2: {
            'sm_60': {
                'HECBioSim/Crambin': (202.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (111.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (15.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (18.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (6.0, None, None, 'ns/day'),
            },
            'broadwell': {
                'HECBioSim/Crambin': (200.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (65.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (8.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (13.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (4.0, None, None, 'ns/day'),
            },
            'zen2': {
                'HECBioSim/Crambin': (355.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (210.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (31.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (53.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (13.0, None, None, 'ns/day'),
            },
            'x86_64_v4': {
                'HECBioSim/Crambin': (355.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (210.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (31.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (53.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (13.0, None, None, 'ns/day'),
            },
        },
        4: {
            'sm_60': {
                'HECBioSim/Crambin': (200.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (133.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (22.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (28.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (10.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (5.0, None, None, 'ns/day'),
            },
            'broadwell': {
                'HECBioSim/Crambin': (260.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (111.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (15.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (23.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (7.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (3.0, None, None, 'ns/day'),
            },
            'zen2': {
                'HECBioSim/Crambin': (340.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (230.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (56.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (80.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (25.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (11.0, None, None, 'ns/day'),
            },
            'x86_64_v4': {
                'HECBioSim/Crambin': (340.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (230.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (56.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (80.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (25.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (11.0, None, None, 'ns/day'),
            },
        },
        6: {
            'sm_60': {
                'HECBioSim/Crambin': (213.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (142.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (28.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (29.346, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (13.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (8.0, None, None, 'ns/day'),
            },
            'broadwell': {
                'HECBioSim/Crambin': (308.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (127.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (22.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (29.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (9.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (5.0, None, None, 'ns/day'),
            },
            'zen2': {
                'HECBioSim/Glutamine-Binding-Protein': (240.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (75.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (110.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (33.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (13.0, None, None, 'ns/day'),
            },
            'x86_64_v4': {
                'HECBioSim/Glutamine-Binding-Protein': (240.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (75.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (110.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (33.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (13.0, None, None, 'ns/day'),
            },
        },
        8: {
            'sm_60': {
                'HECBioSim/Crambin': (206.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (149.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (37.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (39.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (16.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (9.0, None, None, 'ns/day'),
            },
            'broadwell': {
                'HECBioSim/Crambin': (356.0, None, None, 'ns/day'),
                'HECBioSim/Glutamine-Binding-Protein': (158.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (28.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (39.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (11.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (6.0, None, None, 'ns/day'),
            },
            'zen2': {
                'HECBioSim/Glutamine-Binding-Protein': (250.0, None, None, 'ns/day'),   # noqa: E501
                'HECBioSim/hEGFRDimer': (80.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (104.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (43.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (20.0, None, None, 'ns/day'),
            },
            'x86_64_v4': {
                'HECBioSim/Glutamine-Binding-Protein': (250.0, None, None, 'ns/day'),   # noqa: E501
                'HECBioSim/hEGFRDimer': (80.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (104.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (43.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (20.0, None, None, 'ns/day'),
            },
        },
        16: {
            'sm_60': {
                'HECBioSim/Glutamine-Binding-Protein': (154.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (43.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (41.889, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (21.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (14.0, None, None, 'ns/day'),
            },
            'broadwell': {
                'HECBioSim/Glutamine-Binding-Protein': (200.0, None, None, 'ns/day'),  # noqa: E501
                'HECBioSim/hEGFRDimer': (44.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (31.47, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (19.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (10.0, None, None, 'ns/day'),
            },
            'zen2': {
                'HECBioSim/hEGFRDimer': (82.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (70.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (49.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (25.0, None, None, 'ns/day'),
            },
            'x86_64_v4': {
                'HECBioSim/hEGFRDimer': (82.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerSmallerPL': (70.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRDimerPair': (49.0, None, None, 'ns/day'),
                'HECBioSim/hEGFRtetramerPair': (25.0, None, None, 'ns/day'),
            },
        }
    }

    @run_after('init')
    def setup_filtering_criteria(self):
        # Update test's description
        self.descr += f' ({self.num_nodes} node(s))'

        # Setup system filtering
        valid_systems = {
            'cpu': {
                1: ['+cpu'],
                2: ['+cpu'],
                4: ['+cpu'],
                6: ['+cpu'],
                8: ['+cpu'],
                16: ['+cpu'],
            },
            'gpu': {
                1: ['+gpu'],
                2: ['+gpu'],
                4: ['+gpu'],
                6: ['+gpu'],
                8: ['+gpu'],
                16: ['+gpu'],
            }
        }
        try:
            self.valid_systems = valid_systems[self.nb_impl][self.num_nodes]
        except KeyError:
            self.valid_systems = []

        # Setup prog env. filtering
        if self.current_system.name in ('eiger', 'pilatus'):
            self.valid_prog_environs = ['cpeGNU']

        if self.num_nodes in (6, 16):
            self.tags |= {'production'}
            if (self.nb_impl == 'gpu' and
                self.bench_name == 'HECBioSim/hEGFRDimerSmallerPL'):
                self.tags |= {'maintenance'}

    @run_before('run')
    def setup_run(self):
        self.skip_if_no_procinfo()

        # Setup GPU run
        if self.nb_impl == 'gpu':
            self.num_gpus_per_node = 1
            self.variables = {'CRAY_CUDA_MPS': '1'}

        proc = self.current_partition.processor
        gpu_devices = self.current_partition.select_devices('gpu')

        # Choose arch; we set explicitly the GPU arch, since there is no
        # auto-detection
        arch = proc.arch
        if gpu_devices:
            arch = gpu_devices[0].arch

        try:
            found = self.allref[self.num_nodes][arch][self.bench_name]
        except KeyError:
            self.skip(f'Configuration with {self.num_nodes} node(s) of '
                      f'{self.bench_name!r} is not supported on {arch!r}')

        # Setup performance references
        self.reference = {
            '*': {
                'perf': self.allref[self.num_nodes][arch][self.bench_name]
            }
        }

        # Setup parallel run
        self.num_tasks_per_node = proc.num_cores
        self.num_tasks = self.num_nodes * self.num_tasks_per_node
