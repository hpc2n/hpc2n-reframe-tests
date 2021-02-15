# HPC2N ReFrame setup

site_configuration = {
    'systems': [
        {
            'name': 'skalman',
            'descr': 'Generic system',
            'hostnames': ['skalman'],
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gnu'],
                },
            ],
        },
        {
            'name': 'alvis',
            'descr': 'Alvis cluster',
            'hostnames': ['alvis1', 'alvis2'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': '2xV100',
                    'descr': 'GPU 2xV100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2020-5-235', '-C 2xV100'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=V100:{num_gpus_per_node}'],
                        },
                    ],
                },
                {
                    'name': '4xV100',
                    'descr': 'GPU 4xV100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2020-5-235', '-C 4xV100'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=V100:{num_gpus_per_node}'],
                        },
                    ],
                },
                {
                    'name': '8xT4',
                    'descr': 'GPU 8xT4 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2020-5-235', '-C 8xT4'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=T4:{num_gpus_per_node}'],
                        },
                    ],
                },
                {
                    'name': '4xA100',
                    'descr': 'GPU 4xA100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2020-5-235', '-C 4xA100'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=A100:{num_gpus_per_node}'],
                        },
                    ],
                },
            ],
        },
        {
            'name': 'kebnekaise',
            'descr': 'Kebnekaise cluster',
            'hostnames': ['b-'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'local',
                    'descr': 'Locally on nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gnu', 'foss', 'intel'],
                },
                {
                    'name': 'bdw',
                    'descr': 'Broadwell compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-C broadwell', '-A sysop'],
                    'environs': ['gnu', 'foss', 'intel'],
                },
                {
                    'name': 'sky',
                    'descr': 'Skylake compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-C skylake', '-A sysop'],
                    'environs': ['gnu', 'foss', 'intel'],
                },
                {
                    'name': 'gpu_1xK80',
                    'descr': 'GPU 1xK80 half node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&2xK80', '--gres=gpu:k80:1'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                },
                {
                    'name': 'gpu_2xK80',
                    'descr': 'GPU 2xK80 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&2xK80', '--gres=gpu:k80:2', '--exclusive'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                },
                {
                    'name': 'gpu_4xK80',
                    'descr': 'GPU 4xK80 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&4xV80', '--gres=gpu:k80:4', '--exclusive'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                },
                {
                    'name': 'gpu_1xV100',
                    'descr': 'GPU 1xV00 half node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C skylake&2xV100', '--gres=gpu:v100:1'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                },
                {
                    'name': 'gpu_2xV100',
                    'descr': 'GPU 2xV00 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C skylake&2xV100', '--gres=gpu:v100:2', '--exclusive'],
                    'environs': ['gnu', 'foss', 'intel', 'fosscuda'],
                },
                {
                    'name': 'knl',
                    'descr': 'KNL compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-p knl', '-A sysop'],
                    'environs': ['gnu', 'foss', 'intel'],
                    'resources': [
                        {
                            'name': 'threads',
                            'options': ['--threads-per-core={threads}'],
                        },
                        {
                            'name': 'mode',
                            'options': ['--constraint={numa},{mcdram}'],
                        },
                        {
                            'name': 'hbm',
                            'options': ['--gres=hbm:{hbm_size}'],
                        },
                    ],
                },
                {
                    'name': 'lm',
                    'descr': 'Broadwell largememory compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-p largemem', '-A sysop'],
                    'environs': ['gnu', 'foss', 'intel'],
                },
            ],
        },
        {
            'name': 'generic',
            'descr': 'Generic system',
            'hostnames': ['.*'],
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin'],
                }
            ],
        },
    ],
    'environments': [
        {
            'name': 'gnu',
            'modules': ['foss'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'foss',
            'modules': ['foss'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intel',
            'modules': ['intel'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'fosscuda',
            'modules': ['fosscuda'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'builtin',
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
        },
    ],
    'logging': [
        {
            'handlers': [
                {
                    'type': 'stream',
                    'name': 'stdout',
                    'level': 'info',
                    'format': '%(message)s'
                },
                {
                    'type': 'file',
                    'level': 'debug',
                    'format': '[%(asctime)s] %(levelname)s: %(check_info)s: %(message)s',   # noqa: E501
                    'append': False
                }
            ],
            'handlers_perflog': [
                {
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': (
                        '%(check_job_completion_time)s|reframe %(version)s|'
                        '%(check_info)s|jobid=%(check_jobid)s|'
                        'nodelist=%(check_mynodelist)s|'
                        '%(check_perf_var)s=%(check_perf_value)s|'
                        'ref=%(check_perf_ref)s '
                        '(l=%(check_perf_lower_thres)s, '
                        'u=%(check_perf_upper_thres)s)|'
                        '%(check_perf_unit)s'
                    ),
                    'append': True
                }
            ]
        }
    ],
}
