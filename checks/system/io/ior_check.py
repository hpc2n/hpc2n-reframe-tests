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
                          '/cephyr/NOBACKUP/priv/c3-staff/reframe/io-test',
                          '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test',
                          '/scratch',
                          ])
    username = getpass.getuser()
    time_limit = '60m'
    maintainers = ['SO', 'GLR', 'ÅS']
    tags = {'ops', 'production'}

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
                'kebnekaise:zen3': {
                    'num_tasks': 128,
                    'num_tasks_per_node': 128,
                },
                'kebnekaise:zen4': {
                    'num_tasks': 256,
                    'num_tasks_per_node': 256,
                },
                'kebnekaise:8xa40': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'kebnekaise:2xl40s': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'kebnekaise:6xl40s': {
                    'num_tasks': 60,
                    'num_tasks_per_node': 60,
                },
                'kebnekaise:4xh100': {
                    'num_tasks': 96,
                    'num_tasks_per_node': 96,
                },
                'ior_block_size': '480g',
                'reference': {
                    'write_bw': (5400, -0.1, None, 'MiB/s'),
                    'read_bw': (5300, -0.1, None, 'MiB/s'),
                },
            },
            '/scratch': {
                'valid_systems': ['kebnekaise'],
                'kebnekaise:zen4': {
                    'num_tasks': 256,
                    'num_tasks_per_node': 256,
                },
                'kebnekaise:2xl40s': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'kebnekaise:4xh100': {
                    'num_tasks': 96,
                    'num_tasks_per_node': 96,
                },
                'ior_block_size': '10g',
            },
            '/cephyr/NOBACKUP/priv/c3-staff/reframe/io-test': {
                'valid_systems': ['alvis'],
                'alvis:CPUonly': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:2xV100': {
                    'num_tasks': 16,
                    'num_tasks_per_node': 16,
                },
                'alvis:4xV100': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA40': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
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
                'alvis:2xV100': {
                    'num_tasks': 16,
                    'num_tasks_per_node': 16,
                    'ior_access_type': 'POSIX',
                },
                'alvis:4xV100': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                    'ior_access_type': 'POSIX',
                },
                'alvis:4xA40': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                    'ior_access_type': 'POSIX',
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
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
        self.num_tasks_per_node = tpn
        self.num_cpus_per_task = cpt

    @run_after('init')
    def set_modules(self):
        module = {
            'kebnekaise': ['gompi/2023b', 'IOR/4.0.0'],
            'alvis': ['IOR/3.3.0-gompi-2022a'],
        }
        self.modules = module.get(self.current_system.name, [])

    @run_before('run')
    def prepare_run(self):
        cur_sys = self.current_system.name
        fullname = self.current_partition.fullname
        if cur_sys not in self.fs[self.base_dir]:
            cur_sys = 'dummy'
        if fullname not in self.fs[self.base_dir]:
            fullname = cur_sys

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
        block_size = self.fs[self.base_dir][cur_sys].get('ior_block_size', block_size)
        block_size = self.fs[self.base_dir][fullname].get('ior_block_size', block_size)

        xfr_size = self.fs[self.base_dir]['ior_xfr_size']
        xfr_size = self.fs[self.base_dir][cur_sys].get('ior_xfr_size', xfr_size)
        xfr_size = self.fs[self.base_dir][fullname].get('ior_xfr_size', xfr_size)

        access_type = self.fs[self.base_dir]['ior_access_type']
        access_type = self.fs[self.base_dir][cur_sys].get('ior_access_type', access_type)
        access_type = self.fs[self.base_dir][fullname].get('ior_access_type', access_type)

        self.executable_opts += ['-F', '-C ', '-Q', str(self.num_tasks_per_node), '-t', xfr_size , '-D 1200',
                                '-b', block_size, '-a', access_type,
                                '-A -1',  # Refnumber used for matching the correct output lines
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
                r'^write\s+(?P<write_bw>\S+)\s+.*\s+-1$', self.stdout,
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
                r'^read\s+(?P<read_bw>\S+)\s+.*\s+-1$', self.stdout,
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
        return sn.assert_found(r'^write\s+.*\s+-1$', self.stdout) and sn.assert_found(r'^read\s+.*\s+-1$', self.stdout)

    @run_after('init')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'write_bw': sn.extractsingle(
                r'^write\s+(?P<write_bw>\S+)\s+.*\s+-1$', self.stdout,
                'write_bw', float),
            'read_bw': sn.extractsingle(
                r'^read\s+(?P<read_bw>\S+)\s+.*\s+-1$', self.stdout,
                'read_bw', float)
        }
