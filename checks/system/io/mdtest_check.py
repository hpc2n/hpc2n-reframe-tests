import getpass
import os

import reframe as rfm
import reframe.utility.sanity as sn


class MDtestBase(rfm.RunOnlyRegressionTest):
    base_dir = parameter(['/pfs/stor10/io-test',
                          '/scratch',
                          '/cephyr/NOBACKUP/priv/c3-staff/reframe/io-test',
                          '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test',
                          ])
    username = getpass.getuser()
    time_limit = '270m'
    maintainers = ['ÅS']
    tags = {'ops', 'maintenance'}

    @run_after('init')
    def set_description(self):
        self.descr = f'MDtest check ({self.base_dir})'

    @run_after('init')
    def add_fs_tags(self):
        self.tags |= {self.base_dir}

    @sanity_function
    def assert_output(self):
        return sn.assert_found(r'^\s+File creation\s+:?\s', self.stdout) and sn.assert_found(r'^\s+Tree removal\s+:?\s', self.stdout)

    @run_after('init')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'dir_create': sn.extractsingle(
                r'^\s+Directory creation\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<dir_create>\S+)\s+', self.stdout,
                'dir_create', float),
            'dir_stat': sn.extractsingle(
                r'^\s+Directory stat\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<dir_stat>\S+)\s+', self.stdout,
                'dir_stat', float),
            'dir_removal': sn.extractsingle(
                r'^\s+Directory removal\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<dir_removal>\S+)\s+', self.stdout,
                'dir_removal', float),
            'file_create': sn.extractsingle(
                r'^\s+File creation\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<file_create>\S+)\s+', self.stdout,
                'file_create', float),
            'file_stat': sn.extractsingle(
                r'^\s+File stat\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<file_stat>\S+)\s+', self.stdout,
                'file_stat', float),
            'file_read': sn.extractsingle(
                r'^\s+File read\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<file_read>\S+)\s+', self.stdout,
                'file_read', float),
            'file_removal': sn.extractsingle(
                r'^\s+File removal\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<file_removal>\S+)\s+', self.stdout,
                'file_removal', float),
            'tree_create': sn.extractsingle(
                r'^\s+Tree creation\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<tree_create>\S+)\s+', self.stdout,
                'tree_create', float),
            'tree_removal': sn.extractsingle(
                r'^\s+Tree removal\s+:?\s+[0-9.]+\s+[0-9.]+\s+(?P<tree_removal>\S+)\s+', self.stdout,
                'tree_removal', float),
        }

    @run_after('init')
    def set_modules(self):
        module = {
            'kebnekaise': ['gompi/2023b', 'IOR/4.0.0'],
            'alvis': ['IOR/3.3.0-gompi-2022a'],
        }
        self.modules = module.get(self.current_system.name, [])

    @run_after('init')
    def set_fs_information(self):
        # Setting some default values
        for data in self.fs.values():
            data.setdefault('nr_dirs_files_per_proc', '20000')
            data.setdefault('iterations', '3')
            data.setdefault('io_api', 'POSIX')
            data.setdefault('stride', '0')
            data.setdefault('unique_dir_per_task', True)
            data.setdefault('hierarch_depth', '3')
            data.setdefault('hierarch_branch', '3')
            data.setdefault('bytes_per_file', '0')
            data.setdefault('stonewall_timer', '300')
            data.setdefault(
                'reference',
                {
                    'dir_create': (0, -0.1, None, 'dirs/s'),
                    'dir_stat': (0, -0.1, None, 'dirs/s'),
                    'dir_removal': (0, -0.1, None, 'dirs/s'),
                    'file_create': (0, -0.1, None, 'files/s'),
                    'file_stat': (0, -0.1, None, 'files/s'),
                    'file_read': (0, -0.1, None, 'files/s'),
                    'file_removal': (0, -0.1, None, 'files/s'),
                    'tree_create': (0, -0.1, None, 'dirs/s'),
                    'tree_removal': (0, -0.1, None, 'dirs/s'),
                },
            )
            data.setdefault('dummy', {})  # entry for unknown systems

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
    def set_performance_reference(self):
        # Converting the references from each fs to per system.
        self.reference = {
            '*': self.fs[self.base_dir]['reference']
        }

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

    @run_before('run')
    def prepare_run_base(self):
        # Default umask is 0022, which generates file permissions -rw-r--r--
        # we want -rw-rw-r-- so we set umask to 0002
        os.umask(2)
        test_dir = os.path.join(self.base_dir, self.username, '.mdtest')
        target_dir = os.path.join(test_dir,
                                 f'.mdtest.{self.current_partition.name}')
        self.prerun_cmds = [f'mkdir -p {test_dir}']
        self.executable = 'mdtest'

        nr_files = self.fs[self.base_dir]['nr_dirs_files_per_proc']
        iterations = self.fs[self.base_dir]['iterations']
        stonewall_timer = self.fs[self.base_dir]['stonewall_timer']
        bytes_per_file = self.fs[self.base_dir]['bytes_per_file']
        hierarch_depth = self.fs[self.base_dir]['hierarch_depth']
        hierarch_branch = self.fs[self.base_dir]['hierarch_branch']
        unique_dir = self.fs[self.base_dir]['unique_dir_per_task']

        self.executable_opts = ['-Y', '-i', iterations, '-n', nr_files,
                                '-d', target_dir]
        if unique_dir:
            self.executable_opts += ['-u']
        if bytes_per_file != '0':
            self.executable_opts += ['-w', bytes_per_file, '-e', bytes_per_file]
        if hierarch_branch == '1':
            self.executable_opts += ['-W', stonewall_timer]
        else:
            self.executable_opts += ['-z', hierarch_depth, '-b', hierarch_branch]


@rfm.simple_test
class MDtestNode(MDtestBase):
    # Single node test
    tags |= {'full'}

    def __init__(self):
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
                'kebnekaise:2xl40s': {
                    'num_tasks': 48,
                    'num_tasks_per_node': 48,
                },
                'kebnekaise:6xl40s': {
                    'num_tasks': 60,
                    'num_tasks_per_node': 60,
                },
                'kebnekaise:8xa40': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'kebnekaise:4xh100': {
                    'num_tasks': 96,
                    'num_tasks_per_node': 96,
                },
                'reference': {
                    'dir_create': (13000, -0.1, None, 'dirs/s'),
                    'dir_stat': (23000, -0.1, None, 'dirs/s'),
                    'dir_removal': (14000, -0.1, None, 'dirs/s'),
                    'file_create': (6500, -0.1, None, 'files/s'),
                    'file_stat': (30000, -0.1, None, 'files/s'),
                    'file_read': (10000, -0.1, None, 'files/s'),
                    'file_removal': (15000, -0.1, None, 'files/s'),
                    'tree_create': (500, -0.1, None, 'dirs/s'),
                    'tree_removal': (400, -0.1, None, 'dirs/s'),
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
            },
            '/cephyr/NOBACKUP/priv/c3-staff/reframe/io-test': {
                'valid_systems': ['alvis'],
                'nr_dirs_files_per_proc': '1000',
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
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 63,
                    'num_tasks_per_node': 63,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 63,
                    'num_tasks_per_node': 63,
                },
                'reference': {
                    'dir_create': (3000, -0.1, None, 'dirs/s'),
                    'dir_stat': (60000, -0.1, None, 'dirs/s'),
                    'dir_removal': (1000, -0.1, None, 'dirs/s'),
                    'file_create': (4000, -0.1, None, 'files/s'),
                    'file_stat': (60000, -0.1, None, 'files/s'),
                    'file_read': (35000, -0.1, None, 'files/s'),
                    'file_removal': (1500, -0.1, None, 'files/s'),
                    'tree_create': (37, -0.1, None, 'dirs/s'),
                    'tree_removal': (9, -0.1, None, 'dirs/s'),
                },
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
                },
                'alvis:4xV100': {
                    'num_tasks': 32,
                    'num_tasks_per_node': 32,
                },
                'alvis:4xA40': {
                    'num_tasks': 64,
                    'num_tasks_per_node': 64,
                },
                'alvis:4xA100_MEM256': {
                    'num_tasks': 63,
                    'num_tasks_per_node': 63,
                },
                'alvis:4xA100_MEM512': {
                    'num_tasks': 63,
                    'num_tasks_per_node': 63,
                },
                'reference': {
                    'dir_create': (64000, -0.1, None, 'dirs/s'),
                    'dir_stat': (95000, -0.1, None, 'dirs/s'),
                    'dir_removal': (70000, -0.1, None, 'dirs/s'),
                    'file_create': (60000, -0.1, None, 'files/s'),
                    'file_stat': (120000, -0.1, None, 'files/s'),
                    'file_read': (55000, -0.1, None, 'files/s'),
                    'file_removal': (70000, -0.1, None, 'files/s'),
                    'tree_create': (250, -0.1, None, 'dirs/s'),
                    'tree_removal': (450, -0.1, None, 'dirs/s'),
                },
            },
        }


    @run_before('run')
    def prepare_run(self):
        # executable options depends on the file system
        io_api = self.fs[self.base_dir]['io_api']
        stride = self.fs[self.base_dir]['stride']
        self.executable_opts += ['-a', io_api,
                                '-N', stride]


@rfm.simple_test
class MDtestSingle(MDtestBase):
    # Single thread test
    tags |= {'single'}

    def __init__(self):
        self.fs = {
            '/pfs/stor10/io-test': {
                'valid_systems': ['kebnekaise'],
                'nr_dirs_files_per_proc': '100000',
                'iterations': '5',
                'reference': {
                    'dir_create': (1900, -0.1, None, 'dirs/s'),
                    'dir_stat': (2100, -0.1, None, 'dirs/s'),
                    'dir_removal': (1800, -0.1, None, 'dirs/s'),
                    'file_create': (900, -0.1, None, 'files/s'),
                    'file_stat': (950, -0.1, None, 'files/s'),
                    'file_read': (1100, -0.1, None, 'files/s'),
                    'file_removal': (1700, -0.1, None, 'files/s'),
                    'tree_create': (850, -0.1, None, 'dirs/s'),
                    'tree_removal': (1200, -0.1, None, 'dirs/s'),
                },
            },
            '/scratch': {
                'valid_systems': ['kebnekaise'],
                'nr_dirs_files_per_proc': '100000',
                'iterations': '5',
            },
            '/cephyr/NOBACKUP/priv/c3-staff/reframe/io-test': {
                'valid_systems': ['alvis'],
                'nr_dirs_files_per_proc': '100000',
                'iterations': '5',
                'reference': {
                    'dir_create': (1700, -0.1, None, 'dirs/s'),
                    'dir_stat': (155000, -0.1, None, 'dirs/s'),
                    'dir_removal': (1700, -0.1, None, 'dirs/s'),
                    'file_create': (3400, -0.1, None, 'files/s'),
                    'file_stat': (138000, -0.1, None, 'files/s'),
                    'file_read': (138000, -0.1, None, 'files/s'),
                    'file_removal': (3300, -0.1, None, 'files/s'),
                    'tree_create': (3600, -0.1, None, 'dirs/s'),
                    'tree_removal': (900, -0.1, None, 'dirs/s'),
                },
            },
            '/mimer/NOBACKUP/groups/c3-staff/reframe/io-test': {
                'valid_systems': ['alvis'],
                'nr_dirs_files_per_proc': '100000',
                'iterations': '5',
                'reference': {
                    'dir_create': (2500, -0.1, None, 'dirs/s'),
                    'dir_stat': (16000, -0.1, None, 'dirs/s'),
                    'dir_removal': (2000, -0.1, None, 'dirs/s'),
                    'file_create': (2500, -0.1, None, 'files/s'),
                    'file_stat': (27000, -0.1, None, 'files/s'),
                    'file_read': (32000, -0.1, None, 'files/s'),
                    'file_removal': (2500, -0.1, None, 'files/s'),
                    'tree_create': (1200, -0.1, None, 'dirs/s'),
                    'tree_removal': (700, -0.1, None, 'dirs/s'),
                },
            },
        }
