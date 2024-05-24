# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.udeps as udeps

from reframe.core.backends import getlauncher


class build_stream(rfm.CompileOnlyRegressionTest):
    descr = 'Build STREAM Benchmark'

    build_locally = False
    sourcepath = 'stream.c'
    build_system = 'SingleSource'

    @run_before('compile')
    def prepare_build(self):
        static = '-static' if self.current_system.name != 'alvis' and self.current_system.name != 'vera' else ''
        self.prgenv_flags = {
            'foss': ['-fopenmp', '-O3', '-march=native', static],
            'intel': ['-qopenmp', '-O3', '-xHost', '-ip', '-ansi-alias', '-fno-alias', static, '-qopt-prefetch-distance=64,8', '-qopt-streaming-cache-evict=0', '-qopt-streaming-stores always'],
        }

        envname = self.current_environ.name.split('_')[0]
        self.build_system.cflags = self.prgenv_flags.get(envname, ['-O3'])

    @sanity_function
    def validate_build(self):
        return sn.assert_not_found('error', self.stderr)


class StreamTest2Base(rfm.RunOnlyRegressionTest):
    '''Base class of new Streams test'''

    num_tasks = 1
    num_tasks_per_node = 1

    tags = {'production'}
    maintainers = ['ÅS']

    stream_binary = fixture(build_stream, scope='environment')

    @sanity_function
    def validate_solution(self):
        return sn.assert_found(r'Solution Validates: avg error less than', self.stdout)

@rfm.simple_test
class StreamTest2(StreamTest2Base):
    '''This test checks the stream test:
       Function    Best Rate MB/s  Avg time     Min time     Max time
       Triad:          13991.7     0.017174     0.017153     0.017192
    '''

    descr = 'STREAM Benchmark'

    valid_systems = ['kebnekaise:%s' % x for x in ['bdw', 'sky', 'knl', 'lm', 'zen3', 'gen4-cpu', 'gen4-l40s', 'gen4-h100']]
    valid_systems += ['aigert']
    valid_systems += ['alvis', 'vera', 'UmU-Cloud']
    valid_prog_environs = ['%s_%s' % (tc, tv) for tc in ['foss', 'intel']
        for tv in ['2021b', '2022a', '2023b']]

    stream_cpus_per_task = {
        'kebnekaise:local': 28,
        'kebnekaise:bdw': 28,
        'kebnekaise:sky': 28,
        'kebnekaise:gpu': 28,
        'kebnekaise:knl': 68,
        'kebnekaise:lm': 72,
        'kebnekaise:zen3': 128,
        'kebnekaise:gen4-cpu': 256,
        'kebnekaise:gen4-l40s': 48,
        'kebnekaise:gen4-h100': 96,
        'aigert:zen4': 256,
        'UmU-Cloud:default': 64,
        'vera:skylake': 32,
        'alvis:8xT4': 32,
        'alvis:2xV100': 16,
        'alvis:4xV100': 32,
        'alvis:4xA100_MEM256': 64,
        'alvis:4xA100_MEM512': 64,
        'alvis:4xA100fat': 64,
        'alvis:4xA40': 64,
    }
    thread_reduction = {
        # Due to the wekanode process we need to reduce number of OMP threads on A100 nodes
        'alvis:4xA100_MEM256': 2,
        'alvis:4xA100_MEM512': 2,
        'alvis:4xA100fat': 2,
    }
    # Size of array in Mi-elements (*1024^2), total memory usage is size * 1024^2 * 8 * 3
    stream_array = {
        'kebnekaise:local': 4500,
        'kebnekaise:bdw': 4500,
        'kebnekaise:sky': 4500,
        'kebnekaise:gpu': 4500,
        'kebnekaise:knl': 6800,
        'kebnekaise:lm': 24000, # 121000, for using the whole memory, but that takes forever.
        'kebnekaise:zen3': 42000,
        'kebnekaise:gen4-cpu': 26000,
        'kebnekaise:gen4-l40s': 13000,
        'kebnekaise:gen4-h100': 26000,
        'aigert:zen4': 30000,
        'UmU-Cloud:default': 21200,
        'vera:skylake': 3600,
        'alvis:8xT4': 22900,
        'alvis:2xV100': 30900,
        'alvis:4xV100': 30900,
        # Due to the wekanode process we need to reduce memory on A100 nodes
        'alvis:4xA100_MEM256': 9800,
        'alvis:4xA100_MEM512': 20000,
        'alvis:4xA100fat': 41000,
        'alvis:4xA40': 10400,
    }
    use_omp_binding = {
        # Due to the wekanode process we can't use OMP binding on A100 nodes
        'alvis:4xA100_MEM256': False,
        'alvis:4xA100_MEM512': False,
        'alvis:4xA100fat': False,
    }
    default_variables = {
        'OMP_PLACES': 'threads',
        'OMP_PROC_BIND': 'spread'
    }
    stream_bw_reference = {
        'foss': {
            'kebnekaise:bdw': {
                'Copy':  (86000, -0.05, 0.05, 'MB/s'),
                'Scale': (86000, -0.05, 0.05, 'MB/s'),
                'Add':   (97000, -0.05, 0.05, 'MB/s'),
                'Triad': (97000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:sky': {
                'Copy':  (121000, -0.05, 0.05, 'MB/s'),
                'Scale': (121000, -0.05, 0.05, 'MB/s'),
                'Add':   (112500, -0.05, 0.05, 'MB/s'),
                'Triad': (112500, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:knl': {
                'Copy':  (57000, -0.05, 0.05, 'MB/s'),
                'Scale': (56000, -0.05, 0.05, 'MB/s'),
                'Add':   (63000, -0.05, 0.05, 'MB/s'),
                'Triad': (63000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:lm': {
                'Copy':  (180000, -0.05, 0.05, 'MB/s'),
                'Scale': (180000, -0.05, 0.05, 'MB/s'),
                'Add':   (200000, -0.05, 0.05, 'MB/s'),
                'Triad': (200000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:zen3': {
                'Copy':  (200000, -0.05, 0.05, 'MB/s'),
                'Scale': (200000, -0.05, 0.05, 'MB/s'),
                'Add':   (230000, -0.05, 0.05, 'MB/s'),
                'Triad': (230000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:gen4-cpu': {
                'Copy':  (430000, -0.05, 0.05, 'MB/s'),
                'Scale': (430000, -0.05, 0.05, 'MB/s'),
                'Add':   (500000, -0.05, 0.05, 'MB/s'),
                'Triad': (500000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:gen4-l40s': {
                'Copy':  (393000, -0.05, 0.05, 'MB/s'),
                'Scale': (393000, -0.05, 0.05, 'MB/s'),
                'Add':   (437000, -0.05, 0.05, 'MB/s'),
                'Triad': (437000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:gen4-h100': {
                'Copy':  (466000, -0.05, 0.05, 'MB/s'),
                'Scale': (466000, -0.05, 0.05, 'MB/s'),
                'Add':   (522000, -0.05, 0.05, 'MB/s'),
                'Triad': (522000, -0.05, 0.05, 'MB/s'),
            },
            'aigert:zen4': {
                'Copy':  (455000, -0.05, 0.05, 'MB/s'),
                'Scale': (455000, -0.05, 0.05, 'MB/s'),
                'Add':   (520000, -0.05, 0.05, 'MB/s'),
                'Triad': (520000, -0.05, 0.05, 'MB/s'),
            },
            'UmU-Cloud:default': {
                'Copy':  (166000, -0.05, 0.05, 'MB/s'),
                'Scale': (166000, -0.05, 0.05, 'MB/s'),
                'Add':   (182000, -0.05, 0.05, 'MB/s'),
                'Triad': (182000, -0.05, 0.05, 'MB/s'),
            },
            'vera:skylake': {
                'Copy':  (121000, -0.05, 0.05, 'MB/s'),
                'Scale': (121000, -0.05, 0.05, 'MB/s'),
                'Add':   (112500, -0.05, 0.05, 'MB/s'),
                'Triad': (112500, -0.05, 0.05, 'MB/s'),
            },
            'alvis:8xT4': {
                'Copy':  (135000, -0.05, 0.05, 'MB/s'),
                'Scale': (135000, -0.05, 0.05, 'MB/s'),
                'Add':   (152000, -0.05, 0.05, 'MB/s'),
                'Triad': (152000, -0.05, 0.05, 'MB/s'),
            },
            'alvis:4xA40': {
                'Copy':  (220000, -0.05, 0.05, 'MB/s'),
                'Scale': (220000, -0.05, 0.05, 'MB/s'),
                'Add':   (250000, -0.05, 0.05, 'MB/s'),
                'Triad': (250000, -0.05, 0.05, 'MB/s'),
            },
            'alvis:4xA100_MEM256': {
                'Copy':  (215000, -0.05, 0.05, 'MB/s'),
                'Scale': (215000, -0.05, 0.05, 'MB/s'),
                'Add':   (260000, -0.05, 0.05, 'MB/s'),
                'Triad': (260000, -0.05, 0.05, 'MB/s'),
            },
            'alvis:4xA100_MEM512': {
                'Copy':  (215000, -0.05, 0.05, 'MB/s'),
                'Scale': (215000, -0.05, 0.05, 'MB/s'),
                'Add':   (260000, -0.05, 0.05, 'MB/s'),
                'Triad': (260000, -0.05, 0.05, 'MB/s'),
            },
            'alvis:4xA100fat': {
                'Copy':  (215000, -0.05, 0.05, 'MB/s'),
                'Scale': (215000, -0.05, 0.05, 'MB/s'),
                'Add':   (260000, -0.05, 0.05, 'MB/s'),
                'Triad': (260000, -0.05, 0.05, 'MB/s'),
            },
        },
        'intel': {
            'kebnekaise:bdw': {
                'Copy':  (120000, -0.05, 0.05, 'MB/s'),
                'Scale': (120000, -0.05, 0.05, 'MB/s'),
                'Add':   (130000, -0.05, 0.05, 'MB/s'),
                'Triad': (130000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:sky': {
                'Copy':  (156000, -0.05, 0.05, 'MB/s'),
                'Scale': (156000, -0.05, 0.05, 'MB/s'),
                'Add':   (119300, -0.05, 0.05, 'MB/s'),
                'Triad': (122200, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:knl': {
                'Copy':  (57000, -0.05, 0.05, 'MB/s'),
                'Scale': (57000, -0.05, 0.05, 'MB/s'),
                'Add':   (57900, -0.05, 0.05, 'MB/s'),
                'Triad': (57900, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:lm': {
                'Copy':  (230000, -0.05, 0.05, 'MB/s'),
                'Scale': (230000, -0.05, 0.05, 'MB/s'),
                'Add':   (250000, -0.05, 0.05, 'MB/s'),
                'Triad': (250000, -0.05, 0.05, 'MB/s'),
            },
            'kebnekaise:zen3': {
                'Copy':  (200000, -0.05, 0.05, 'MB/s'),
                'Scale': (200000, -0.05, 0.05, 'MB/s'),
                'Add':   (230000, -0.05, 0.05, 'MB/s'),
                'Triad': (230000, -0.05, 0.05, 'MB/s'),
            },
            'UmU-Cloud:default': {
                'Copy':  (166000, -0.05, 0.05, 'MB/s'),
                'Scale': (166000, -0.05, 0.05, 'MB/s'),
                'Add':   (182000, -0.05, 0.05, 'MB/s'),
                'Triad': (182000, -0.05, 0.05, 'MB/s'),
            },
            'vera:skylake': {
                'Copy':  (165000, -0.05, 0.05, 'MB/s'),
                'Scale': (165000, -0.05, 0.05, 'MB/s'),
                'Add':   (172000, -0.05, 0.05, 'MB/s'),
                'Triad': (172000, -0.05, 0.05, 'MB/s'),
            },
            'alvis:8xT4': {
                'Copy':  (185000, -0.05, 0.05, 'MB/s'),
                'Scale': (185000, -0.05, 0.05, 'MB/s'),
                'Add':   (190000, -0.05, 0.05, 'MB/s'),
                'Triad': (190000, -0.05, 0.05, 'MB/s'),
            },
            'alvis:4xA40': {
                'Copy':  (311600, -0.05, 0.05, 'MB/s'),
                'Scale': (310700, -0.05, 0.05, 'MB/s'),
                'Add':   (312800, -0.05, 0.05, 'MB/s'),
                'Triad': (311500, -0.05, 0.05, 'MB/s'),
            },
            'alvis:4xA100_MEM256': {
                'Copy':  (285000, -0.1, 0.05, 'MB/s'),
                'Scale': (290000, -0.1, 0.05, 'MB/s'),
                'Add':   (290000, -0.1, 0.05, 'MB/s'),
                'Triad': (290000, -0.1, 0.05, 'MB/s'),
            },
            'alvis:4xA100_MEM512': {
                'Copy':  (285000, -0.1, 0.05, 'MB/s'),
                'Scale': (290000, -0.1, 0.05, 'MB/s'),
                'Add':   (290000, -0.1, 0.05, 'MB/s'),
                'Triad': (290000, -0.1, 0.05, 'MB/s'),
            },
            'alvis:4xA100fat': {
                'Copy':  (285000, -0.1, 0.05, 'MB/s'),
                'Scale': (290000, -0.1, 0.05, 'MB/s'),
                'Add':   (290000, -0.1, 0.05, 'MB/s'),
                'Triad': (290000, -0.1, 0.05, 'MB/s'),
            },
        },
    }

    @run_after('setup')
    def prepare_test(self):
        '''Setup test parameters and reference values'''

        self.num_cpus_per_task = self.stream_cpus_per_task.get(
            self.current_partition.fullname, 1)
        # This is for the knl threads-per-core resource
        self.extra_resources = {
            'threads': {'threads': 4},
        }

        omp_threads = self.num_cpus_per_task
        if self.current_partition.fullname == 'kebnekaise:knl':
            omp_threads *= 4
        
        thread_reduction = self.thread_reduction.get(self.current_partition.fullname, 0)
        use_omp_binding = self.use_omp_binding.get(self.current_partition.fullname, True)
        if use_omp_binding:
            self.env_vars = self.default_variables
        self.env_vars['OMP_NUM_THREADS'] = str(omp_threads-thread_reduction)

        envname = self.current_environ.name.split('_')[0]

        self.reference = self.stream_bw_reference.get(envname, {})

    @run_after('setup')
    def setup_exclusive(self):
        self.exclusive_access = True
        if self.current_system.name in {'alvis', 'vera', 'UmU-Cloud'}:
            self.exclusive_access = False

    # Stream is serial or OpenMP and should not be started by srun.
    # Especially on the KNLs where that may cause bad thread placement.
    @run_after('setup')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    @performance_function('MB/s')
    def extract_bw(self, kind='Copy'):
        '''Generic performance extraction function.'''

        if kind not in ('Copy', 'Scale', 'Add', 'Triad'):
            raise ValueError(f'illegal value in argument kind ({kind!r})')

        return sn.extractsingle(rf'^{kind}:\s+([0-9.]+)\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$',
                                      self.stdout, 1, float)

    @run_before('performance')
    def set_perf_variables(self):
        '''Build the dictionary with all the performance variables.'''

        self.perf_variables = {
            'Copy': self.extract_bw(),
            'Scale': self.extract_bw('Scale'),
            'Add': self.extract_bw('Add'),
            'Triad': self.extract_bw('Triad'),
        }

    @run_before('run')
    def set_executable(self):
        self.executable = os.path.join(
            self.stream_binary.stagedir,
            self.stream_binary.executable
        )
        mem_sz = self.stream_array.get(self.current_partition.fullname, 2500)*1024*1024
        self.executable_opts = ["-s", "%s" % mem_sz]


@rfm.simple_test
class StreamTest2Maintenance(StreamTest2):
    '''Maintenance version of StreamTest2'''

    valid_prog_environs = ['intel_2022a']

    tags = {'maintenance'}
