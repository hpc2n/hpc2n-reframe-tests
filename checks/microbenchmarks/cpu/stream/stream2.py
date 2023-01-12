# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.udeps as udeps

from reframe.core.backends import getlauncher


class StreamTest2Base(rfm.RunOnlyRegressionTest):
    '''Base class of new Streams test'''

    def __init__(self):
        self.exclusive_access = True
        if self.current_system.name in {'alvis', 'UmU-Cloud'}:
            self.exclusive_access = False
        self.valid_systems = ['kebnekaise:%s' % x for x in ['bdw', 'sky', 'knl', 'lm']]
        self.valid_systems += ['alvis', 'UmU-Cloud']
        self.valid_prog_environs = ['%s%s_%s' % (tc, c, tv) for tc in ['foss', 'intel']
            for c in ['', 'cuda']
            for tv in ['2019a', '2019b', '2020a', '2020b', '2021a', '2022a']]
        self.num_tasks = 1
        self.num_tasks_per_node = 1
        self.depends_on('StreamTest2Build', udeps.by_env)

        self.tags = {'production', 'reboot', 'maintenance'}
        self.maintainers = ['ÅS']


@rfm.simple_test
class StreamTest2(StreamTest2Base):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    def __init__(self):
        super().__init__()

        self.descr = 'STREAM Benchmark'

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

        self.stream_cpus_per_task = {
            'kebnekaise:local': 28,
            'kebnekaise:bdw': 28,
            'kebnekaise:sky': 28,
            'kebnekaise:gpu': 28,
            'kebnekaise:knl': 68,
            'kebnekaise:lm': 72,
            'UmU-Cloud:default': 64,
            'alvis:8xT4': 32,
            'alvis:2xV100': 16,
            'alvis:4xV100': 32,
            'alvis:4xA100_MEM256': 64,
            'alvis:4xA100_MEM512': 64,
            'alvis:4xA100fat': 64,
            'alvis:4xA40': 64,
        }
        self.thread_reduction = {
            # Due to the wekanode process we need to reduce number of OMP threads on A100 nodes
            'alvis:4xA100_MEM256': 2,
            'alvis:4xA100_MEM512': 2,
            'alvis:4xA100fat': 2,
        }
        # Size of array in Mi-elements (*1024^2), total memory usage is size * 1024^2 * 8 * 3
        self.stream_array = {
            'kebnekaise:local': 4500,
            'kebnekaise:bdw': 4500,
            'kebnekaise:sky': 4500,
            'kebnekaise:gpu': 4500,
            'kebnekaise:knl': 6800,
            'kebnekaise:lm': 24000, # 121000, for using the whole memory, but that takes forever.
            'UmU-Cloud:default': 21200,
            'alvis:8xT4': 22900,
            'alvis:2xV100': 30900,
            'alvis:4xV100': 30900,
            # Due to the wekanode process we need to reduce memory on A100 nodes
            'alvis:4xA100_MEM256': 9800,
            'alvis:4xA100_MEM512': 20000,
            'alvis:4xA100fat': 41000,
            'alvis:4xA40': 10400,
        }
        self.use_omp_binding = {
            # Due to the wekanode process we can't use OMP binding on A100 nodes
            'alvis:4xA100_MEM256': False,
            'alvis:4xA100_MEM512': False,
            'alvis:4xA100fat': False,
        }
        self.default_variables = {
            'OMP_PLACES': 'threads',
            'OMP_PROC_BIND': 'spread'
        }
        self.stream_bw_reference = {
            'foss': {
                'kebnekaise:bdw': {
                    'copy':  (86000, -0.05, 0.05, 'MB/s'),
                    'scale': (86000, -0.05, 0.05, 'MB/s'),
                    'add':   (90000, -0.05, 0.05, 'MB/s'),
                    'triad': (90000, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:sky': {
                    'copy':  (121000, -0.05, 0.05, 'MB/s'),
                    'scale': (121000, -0.05, 0.05, 'MB/s'),
                    'add':   (112500, -0.05, 0.05, 'MB/s'),
                    'triad': (112500, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:knl': {
                    'copy':  (57000, -0.05, 0.05, 'MB/s'),
                    'scale': (56000, -0.05, 0.05, 'MB/s'),
                    'add':   (63000, -0.05, 0.05, 'MB/s'),
                    'triad': (63000, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:lm': {
                    'copy':  (191500, -0.05, 0.05, 'MB/s'),
                    'scale': (191500, -0.05, 0.05, 'MB/s'),
                    'add':   (198000, -0.05, 0.05, 'MB/s'),
                    'triad': (198000, -0.05, 0.05, 'MB/s'),
                },
                'UmU-Cloud:default': {
                    'copy':  (166000, -0.05, 0.05, 'MB/s'),
                    'scale': (166000, -0.05, 0.05, 'MB/s'),
                    'add':   (182000, -0.05, 0.05, 'MB/s'),
                    'triad': (182000, -0.05, 0.05, 'MB/s'),
                },
                'alvis:8xT4': {
                    'copy':  (135000, -0.05, 0.05, 'MB/s'),
                    'scale': (135000, -0.05, 0.05, 'MB/s'),
                    'add':   (152000, -0.05, 0.05, 'MB/s'),
                    'triad': (152000, -0.05, 0.05, 'MB/s'),
                },
                'alvis:4xA40': {
                    'copy':  (283600, -0.05, 0.05, 'MB/s'),
                    'scale': (282600, -0.05, 0.05, 'MB/s'),
                    'add':   (294000, -0.05, 0.05, 'MB/s'),
                    'triad': (294200, -0.05, 0.05, 'MB/s'),
                },
            },
            'intel': {
                'kebnekaise:bdw': {
                    'copy':  (120500, -0.05, 0.05, 'MB/s'),
                    'scale': (120500, -0.05, 0.05, 'MB/s'),
                    'add':   (111300, -0.05, 0.05, 'MB/s'),
                    'triad': (111300, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:sky': {
                    'copy':  (156000, -0.05, 0.05, 'MB/s'),
                    'scale': (156000, -0.05, 0.05, 'MB/s'),
                    'add':   (119300, -0.05, 0.05, 'MB/s'),
                    'triad': (122200, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:knl': {
                    'copy':  (57000, -0.05, 0.05, 'MB/s'),
                    'scale': (57000, -0.05, 0.05, 'MB/s'),
                    'add':   (57900, -0.05, 0.05, 'MB/s'),
                    'triad': (57900, -0.05, 0.05, 'MB/s'),
                },
                'kebnekaise:lm': {
                    'copy':  (233000, -0.05, 0.05, 'MB/s'),
                    'scale': (228000, -0.05, 0.05, 'MB/s'),
                    'add':   (225000, -0.05, 0.05, 'MB/s'),
                    'triad': (230000, -0.05, 0.05, 'MB/s'),
                },
                'UmU-Cloud:default': {
                    'copy':  (166000, -0.05, 0.05, 'MB/s'),
                    'scale': (166000, -0.05, 0.05, 'MB/s'),
                    'add':   (182000, -0.05, 0.05, 'MB/s'),
                    'triad': (182000, -0.05, 0.05, 'MB/s'),
                },
                'alvis:4xA40': {
                    'copy':  (311600, -0.05, 0.05, 'MB/s'),
                    'scale': (310700, -0.05, 0.05, 'MB/s'),
                    'add':   (312800, -0.05, 0.05, 'MB/s'),
                    'triad': (311500, -0.05, 0.05, 'MB/s'),
                },
                'alvis:4xA100_MEM256': {
                    'copy':  (285000, -0.1, 0.05, 'MB/s'),
                    'scale': (290000, -0.1, 0.05, 'MB/s'),
                    'add':   (290000, -0.1, 0.05, 'MB/s'),
                    'triad': (290000, -0.1, 0.05, 'MB/s'),
                },
                'alvis:4xA100_MEM512': {
                    'copy':  (285000, -0.1, 0.05, 'MB/s'),
                    'scale': (290000, -0.1, 0.05, 'MB/s'),
                    'add':   (290000, -0.1, 0.05, 'MB/s'),
                    'triad': (290000, -0.1, 0.05, 'MB/s'),
                },
                'alvis:4xA100fat': {
                    'copy':  (285000, -0.1, 0.05, 'MB/s'),
                    'scale': (290000, -0.1, 0.05, 'MB/s'),
                    'add':   (290000, -0.1, 0.05, 'MB/s'),
                    'triad': (290000, -0.1, 0.05, 'MB/s'),
                },
            },
        }

    @require_deps
    def set_executable(self, StreamTest2Build):
        self.executable = os.path.join(
            StreamTest2Build().stagedir, 'StreamTest2Build'
        )
        mem_sz = self.stream_array.get(self.current_partition.fullname, 2500)*1024*1024
        self.executable_opts = ["-s", "%s" % mem_sz]

    @run_after('setup')
    def prepare_test(self):
        self.num_cpus_per_task = self.stream_cpus_per_task.get(
            self.current_partition.fullname, 1)
        self.extra_resources = {
            'threads': {'threads': 4},
        }

        omp_threads = self.num_cpus_per_task
        if self.current_partition.fullname == 'kebnekaise:knl':
            omp_threads *= 4
        
        thread_reduction = self.thread_reduction.get(self.current_partition.fullname, 0)
        use_omp_binding = self.use_omp_binding.get(self.current_partition.fullname, True)
        if use_omp_binding:
            self.variables = self.default_variables
        self.variables['OMP_NUM_THREADS'] = str(omp_threads-thread_reduction)

        envname = self.current_environ.name
        tc_name = envname.split('_')[0].replace("cuda", "")

        try:
            self.reference = self.stream_bw_reference[tc_name]
        except KeyError:
            self.reference = self.stream_bw_reference['foss']

    # Stream is serial or OpenMP and should not be started by srun.
    # Especially on the KNLs where that may cause bad thread placement.
    @run_after('setup')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    @run_after('run')
    def set_nodelist(self):
        self.mynodelist = self.job.nodelist


#@rfm.parameterized_test(*([n] for n in range(100)))
class StreamTest2Multirun(StreamTest2):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    nruns = parameter([n] for n in range(100))

    def __init__(self):
        super().__init__()

@rfm.simple_test
class StreamTest2Build(rfm.CompileOnlyRegressionTest):
    def __init__(self):
        self.descr = 'STREAM Benchmark Build test'
        self.valid_systems = ['kebnekaise:%s' % x for x in ['bdw', 'sky', 'knl', 'lm']]
        self.valid_systems += ['alvis', 'UmU-Cloud']
        self.valid_prog_environs = ['%s%s_%s' % (tc, c, tv) for tc in ['foss', 'intel']
            for c in ['', 'cuda']
            for tv in ['2019a', '2019b', '2020a', '2020b', '2021a', '2022a']]

        static = '-static' if self.current_system.name != 'alvis' else ''
        self.prgenv_flags = {
            'foss': ['-fopenmp', '-O3', '-march=native', static],
            'intel': ['-qopenmp', '-O3', '-xHost', '-ip', '-ansi-alias', '-fno-alias', static, '-qopt-prefetch-distance=64,8', '-qopt-streaming-cache-evict=0', '-qopt-streaming-stores always'],
        }

        self.build_locally = False
        self.sourcepath = 'stream.c'
        self.build_system = 'SingleSource'

        self.sanity_patterns = sn.assert_not_found('error', self.stderr)

    @run_after('setup')
    def prepare_test(self):
        envname = self.current_environ.name
        tc_name = envname.split('_')[0].replace("cuda", "")
        self.build_system.cflags = self.prgenv_flags.get(tc_name, ['-O3'])
