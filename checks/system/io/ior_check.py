# Copyright 2016-2022 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import getpass
import os

import reframe as rfm
import reframe.utility.sanity as sn


class IorCheck(rfm.RunOnlyRegressionTest):
    base_dir = parameter(['/pfs/stor10/io-test',
                          '/cephyr/NOBACKUP/priv/c3-alvis/reframe/io-test',
                          '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test',
                          ])
    username = getpass.getuser()
    time_limit = '15m'
    maintainers = ['SO', 'GLR', 'ÅS']
    tags = {'ops'}

    @run_after('init')
    def set_description(self):
        self.descr = f'IOR check ({self.base_dir})'

    @run_after('init')
    def add_fs_tags(self):
        self.tags |= {self.base_dir}

    @run_after('init')
    def set_fs_information(self):
        self.fs = {
            '/pfs/stor10/io-test': {
                'valid_systems': ['kebnekaise'],
                'kebnekaise': {
                    'num_tasks': 28,
                    'num_tasks_per_node': 28,
                },
                'reference': {
                    'write_bw': (5400, -0.1, None, 'MiB/s'),
                    'read_bw': (5300, -0.1, None, 'MiB/s'),
                },
            },
            '/cephyr/NOBACKUP/priv/c3-alvis/reframe/io-test': {
                'valid_systems': ['alvis'],
                'alvis:CPUonly': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'reference': {
                    'write_bw': (3100, -0.1, None, 'MiB/s'),
                    'read_bw': (2500, -0.1, None, 'MiB/s'),
                },
                'ior_block_size': '240g',
            },
            '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test': {
                'valid_systems': ['alvis'],
                'alvis:CPUonly': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'ior_block_size': '240g',
                'reference': {
                    'write_bw': (6700, -0.1, None, 'MiB/s'),
                    'read_bw': (6100, -0.1, None, 'MiB/s'),
                },
            },
        }

        # Setting some default values
        for data in self.fs.values():
            data.setdefault('ior_block_size', '24g')
            data.setdefault('ior_xfr_size', '4m')
            data.setdefault('ior_access_type', 'MPIIO')
            data.setdefault(
                'reference',
                {
                    'read_bw': (0, None, None, 'MiB/s'),
                    'write_bw': (0, None, None, 'MiB/s')
                }
            )
            data.setdefault('dummy', {})  # entry for unknown systems

    @run_after('init')
    def set_performance_reference(self):
        # Converting the references from each fs to per system.
        self.reference = {
            '*': self.fs[self.base_dir]['reference']
        }

    @run_after('init')
    def set_valid_systems(self):
        self.valid_systems = self.fs[self.base_dir]['valid_systems']

        cur_sys = self.current_system.name
        if cur_sys not in self.fs[self.base_dir]:
            cur_sys = 'dummy'

        vpe = 'valid_prog_environs'
        penv = self.fs[self.base_dir][cur_sys].get(vpe, ['builtin'])
        self.valid_prog_environs = penv


    @run_before('run')
    def set_tasks(self):
        cur_sys = self.current_system.name
        fullname = self.current_partition.fullname
        if cur_sys not in self.fs[self.base_dir]:
            cur_sys = 'dummy'
        if fullname not in self.fs[self.base_dir]:
            fullname = cur_sys

        tpn = self.fs[self.base_dir][cur_sys].get('num_tasks_per_node', 1)
        tpn = self.fs[self.base_dir][fullname].get('num_tasks_per_node', tpn)
        cpt = self.fs[self.base_dir][cur_sys].get('cpus_per_task', 1)
        cpt = self.fs[self.base_dir][fullname].get('cpus_per_task', cpt)
        nt = self.fs[self.base_dir][cur_sys].get('num_tasks', 1)
        nt = self.fs[self.base_dir][fullname].get('num_tasks', nt)
        self.num_tasks = nt
        self.tpn = tpn
        self.num_cpus_per_task = cpt

    @run_after('init')
    def set_modules(self):
        module = {
            'kebnekaise': ['foss/2021b', 'IOR/3.3.0'],
            'alvis': ['IOR/3.3.0-gompi-2022a'],
        }
        self.modules = module.get(self.current_system.name)

    @run_before('run')
    def prepare_run(self):
        # Default umask is 0022, which generates file permissions -rw-r--r--
        # we want -rw-rw-r-- so we set umask to 0002
        os.umask(2)
        test_dir = os.path.join(self.base_dir, self.username, '.ior')
        test_file = os.path.join(test_dir,
                                 f'.ior.{self.current_partition.name}')
        self.prerun_cmds = [f'mkdir -p {test_dir}']
        self.executable = 'ior'

        # executable options depends on the file system
        block_size = self.fs[self.base_dir]['ior_block_size']
        xfr_size = self.fs[self.base_dir]['ior_xfr_size']
        access_type = self.fs[self.base_dir]['ior_access_type']
        self.executable_opts += ['-F', '-C ', '-Q', str(self.tpn), '-t', xfr_size , '-D 240',
                                '-b', block_size, '-a', access_type,
                                '-o', test_file]


@rfm.simple_test
class IorWriteCheck(IorCheck):
    executable_opts = ['-w', '-k']
    tags |= {'write'}

    @sanity_function
    def assert_output(self):
        return sn.assert_found(r'^Max Write: ', self.stdout)

    @run_after('init')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'write_bw': sn.extractsingle(
                r'^Max Write:\s+(?P<write_bw>\S+) MiB/sec', self.stdout,
                'write_bw', float)
        }


@rfm.simple_test
class IorReadCheck(IorCheck):
    executable_opts = ['-r']
    tags |= {'read'}

    @sanity_function
    def assert_output(self):
        return sn.assert_found(r'^Max Read: ', self.stdout)

    @run_after('init')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'read_bw': sn.extractsingle(
                r'^Max Read:\s+(?P<read_bw>\S+) MiB/sec', self.stdout,
                'read_bw', float)
        }

    @run_after('init')
    def set_deps(self):
        variant = IorWriteCheck.get_variant_nums(base_dir=self.base_dir)[0]
        self.depends_on(IorWriteCheck.variant_name(variant))


@rfm.simple_test
class IorWriteReadCheck(IorCheck):
    executable_opts = ['-w', '-r']
    tags = {'ops', 'maintenance'}
    tags |= {'write', 'read'}

    @sanity_function
    def assert_output(self):
        return sn.assert_found(r'^Max Write: ', self.stdout) and sn.assert_found(r'^Max Read: ', self.stdout)

    @run_after('init')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'write_bw': sn.extractsingle(
                r'^Max Write:\s+(?P<write_bw>\S+) MiB/sec', self.stdout,
                'write_bw', float),
            'read_bw': sn.extractsingle(
                r'^Max Read:\s+(?P<read_bw>\S+) MiB/sec', self.stdout,
                'read_bw', float)
        }
