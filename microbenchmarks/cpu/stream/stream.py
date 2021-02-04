# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn


@rfm.required_version('>=2.14')
@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    def __init__(self):
        self.descr = 'STREAM Benchmark'
        self.exclusive_access = True
        self.valid_systems = ['kebnekaise:bdw', 'kebnekaise:sky', 'kebnekaise:knl',
                              'kebnekaise:lm']
        self.valid_prog_environs = ['foss', 'intel']

        self.use_multithreading = False

        self.prgenv_flags = {
            'foss': ['-fopenmp', '-O3', '-march=native', '-static'],
            'intel': ['-qopenmp', '-O3', '-xHost', '-static', '-qopt-prefetch-distance=64,8', '-qopt-streaming-cache-evict=0', '-qopt-streaming-stores always'],
        }

        if self.current_system.name in ['arolla', 'tsa']:
            self.exclusive_access = True
            self.valid_prog_environs = ['PrgEnv-gnu']

        self.build_locally = False
        self.sourcepath = 'stream.c'
        self.build_system = 'SingleSource'
        self.build_system.cppflags = ['-DDEFAULT_STREAM_ARRAY_SIZE=4676648960']
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.stream_cpus_per_task = {
            'kebnekaise:bdw': 24,
            'kebnekaise:sky': 24,
            'kebnekaise:gpu': 24,
            'kebnekaise:knl': 68,
        }
        self.variables = {
            'OMP_PLACES': 'threads',
            'OMP_PROC_BIND': 'spread'
        }
        self.sanity_patterns = sn.assert_found(
            r'Solution Validates: avg error less than', self.stdout)
        self.perf_patterns = {
            'copy': sn.extractsingle(r'^Copy:\s+(?P<copy>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'copy', float),
            'scale': sn.extractsingle(r'^Scale:\s+(?P<scale>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'scale', float),
            'add': sn.extractsingle(r'^Add:\s+(?P<add>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'add', float),
            'triad': sn.extractsingle(r'^Triad:\s+(?P<triad>[0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 'triad', float),
        }
        self.stream_bw_reference = {
            'foss': {
                'kebnekaise:bdw': {
                    'copy':  (93500, -0.05, 0.05, 'MB/s'),
                    'scale': (74000, -0.05, 0.05, 'MB/s'),
                    'add':   (81100, -0.05, 0.05, 'MB/s'),
                    'triad': (84400, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:sky': {
                    'copy':  (102200, -0.05, 0.05, 'MB/s'),
                    'scale': (107700, -0.05, 0.05, 'MB/s'),
                    'add':   (125100, -0.05, 0.05, 'MB/s'),
                    'triad': (127500, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:knl': {
                    'copy':  (249200, -0.05, 0.05, 'MB/s'),
                    'scale': (304700, -0.05, 0.05, 'MB/s'),
                    'add':   (332000, -0.05, 0.05, 'MB/s'),
                    'triad': (334700, -0.05, 0.05, 'MB/s'),
                },
            },
            'intel': {
                'kebnekaise:bdw': {
                    'copy':  (115700, -0.05, 0.05, 'MB/s'),
                    'scale': (85500, -0.05, 0.05, 'MB/s'),
                    'add':   (107900, -0.05, 0.05, 'MB/s'),
                    'triad': (111100, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:sky': {
                    'copy':  (141800, -0.05, 0.05, 'MB/s'),
                    'scale': (145800, -0.05, 0.05, 'MB/s'),
                    'add':   (137400, -0.05, 0.05, 'MB/s'),
                    'triad': (146100, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:knl': {
                    'copy':  (270000, -0.05, 0.05, 'MB/s'),
                    'scale': (270000, -0.05, 0.05, 'MB/s'),
                    'add':   (324000, -0.05, 0.05, 'MB/s'),
                    'triad': (320000, -0.05, 0.05, 'MB/s'),
                },
            },
        }
        self.tags = {'production'}
        self.maintainers = ['ÅS']

    @rfm.run_after('setup')
    def prepare_test(self):
        self.num_cpus_per_task = self.stream_cpus_per_task.get(
            self.current_partition.fullname, 1)
        self.variables['OMP_NUM_THREADS'] = str(self.num_cpus_per_task)
        envname = self.current_environ.name

        self.build_system.cflags = self.prgenv_flags.get(envname, ['-O3'])
        if envname == 'PrgEnv-pgi':
            self.variables['OMP_PROC_BIND'] = 'true'

        try:
            self.reference = self.stream_bw_reference[envname]
        except KeyError:
            self.reference = self.stream_bw_reference['foss']
