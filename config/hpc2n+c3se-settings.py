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
            'name': 'vera',
            'descr': 'Vera cluster',
            'hostnames': ['vera'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'skylake',
                    'descr': 'Skylake nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C SKYLAKE&MEM96&NOGPU'],
                    'max_jobs': 100,
                    'features': ['cpu', 'intelcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'icelake',
                    'descr': 'Icelake nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C ICELAKE&MEM512&NOGPU'],
                    'max_jobs': 100,
                    'features': ['cpu', 'intelcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
            ],
        },
        {
            'name': 'alvis',
            'descr': 'Alvis cluster',
            'hostnames': ['alvis'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': '2xV100',
                    'descr': 'GPU 2xV100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 2xV100', '--gpus-per-node=V100:2'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_70',
                            'num_devices': 2
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '4xV100',
                    'descr': 'GPU 4xV100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 4xV100', '--gpus-per-node=V100:4'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_70',
                            'num_devices': 4
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '8xT4',
                    'descr': 'GPU 8xT4 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 8xT4', '--gpus-per-node=T4:8'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_75',
                            'num_devices': 8
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '4xA100_MEM256',
                    'descr': 'GPU 4xA100 nodes with 256G memory and 2x32 cores',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C MEM256', '--gpus-per-node=A100:4'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '4xA100_MEM512',
                    'descr': 'GPU 4xA100 nodes with 512G memory and 2x32 cores',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C MEM512', '--gpus-per-node=A100:4'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_80',
                            'num_devices': 4
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '4xA100fat',
                    'descr': 'GPU 4xA100 fat nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 4xA100fat', '--gpus-per-node=A100fat:4'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_80',
                            'num_devices': 4
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '4xA40',
                    'descr': 'GPU 4xA40 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 4xA40', '--gpus-per-node=A40:4'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_86',
                            'num_devices': 4
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'CPUonly',
                    'descr': 'CPU only nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C NOGPU'],
                    'max_jobs': 4,
                    'features': ['cpu', 'intelcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
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
                    'max_jobs': 4,
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'bdw',
                    'descr': 'Broadwell compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-C broadwell', '-A sysop'],
                    'max_jobs': 100,
                    'features': ['cpu', 'intelcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'sky',
                    'descr': 'Skylake compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-C skylake', '-A sysop'],
                    'max_jobs': 100,
                    'features': ['cpu', 'intelcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'zen3',
                    'descr': 'Zen3 compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-C zen3', '-A sysop'],
                    'max_jobs': 100,
                    'features': ['cpu', 'amdcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2021b', 'foss_2022a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'zen4',
                    'descr': 'Zen4 compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen4'],
                    'max_jobs': 100,
                    'features': ['cpu', 'amdcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_2021b', 'foss_2023b'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '2xv100',
                    'descr': 'GPU 2xV100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C skylake&2xV100', '--gpus-per-node=v100:2', '--exclusive'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_70',
                            'num_devices': 2
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '2xa6000',
                    'descr': 'GPU 2xA6000 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen3&2xA6000', '--gpus-per-node=a6000:2', '--exclusive'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_86',
                            'num_devices': 2
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '8xa40',
                    'descr': 'GPU 8xA40',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen4&8xA40', '--gpus-per-node=a40:8'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_86',
                            'num_devices': 8
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '2xa100',
                    'descr': 'GPU 2xA100 node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen3&2xA100', '--gpus-per-node=a100:2', '--exclusive'],
                    'max_jobs': 100,
                    'features': ['gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'foss_2021b', 'foss_2022a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_80',
                            'num_devices': 2
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '2xl40s',
                    'descr': 'Zen4 2xL40s gpu nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen4&l40s', '--gpus-per-node=l40s:2'],
                    'max_jobs': 100,
                    'features': ['cpu', 'amdcpu', 'gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021b', 'foss_2023b'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_89',
                            'num_devices': 2,
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '6xl40s',
                    'descr': 'Zen4 6xL40s gpu nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen4&l40s', '--gpus-per-node=l40s:6'],
                    'max_jobs': 100,
                    'features': ['cpu', 'amdcpu', 'gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021b', 'foss_2023b'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_89',
                            'num_devices': 6,
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '4xh100',
                    'descr': 'Zen4 4xH100 gpu nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen4&H100', '--gpus-per-node=h100:4'],
                    'max_jobs': 100,
                    'features': ['cpu', 'amdcpu', 'gpu', 'nvgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'foss_2021b', 'foss_2023b'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'arch': 'sm_90',
                            'num_devices': 4,
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '2xmi100',
                    'descr': 'GPU 2xMI100 node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-C zen3&2xMI100', '--gpus-per-node=mi100:2', '--exclusive'],
                    'max_jobs': 100,
                    'features': ['gpu', 'amdgpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'foss_2021b', 'foss_2022a', 'intel_2022a'],
                    'devices': [
                        {
                            'type': 'gpu',
                            'num_devices': 2
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'lm',
                    'descr': 'Broadwell largememory compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-p largemem', '-A sysop'],
                    'max_jobs': 100,
                    'features': ['cpu', 'intelcpu'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'foss_2021b', 'foss_2022a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
            ],
        },
        {
            'name': 'UmU-Cloud',
            'descr': 'UmU part of SNIC Cloud system',
            'hostnames': ['u-cn-'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin', 'foss', 'foss_2021a', 'foss_with_cuda', 'intel_2021a', 'intel_2022a'],
                    'max_jobs': 1,
                }
            ],
        },
        {
            'name': 'aigert',
            'descr': 'HPC2N WLCG compute cluster',
            'hostnames': ['g-cn'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'zen4',
                    'descr': 'AMD zen4c nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p grid' '-C zen4'],
                    'max_jobs': 100,
                    'environs': ['builtin', 'foss', 'foss_2023b'],
                },
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
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'foss',
            'modules': ['foss'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud', 'aigert'],
        },
        {
            'name': 'foss_2019a',
            'modules': ['foss/2019a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'foss_2019b',
            'modules': ['foss/2019b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'foss_2020a',
            'modules': ['foss/2020a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'foss_2020b',
            'modules': ['foss/2020b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'foss_2021a',
            'modules': ['foss/2021a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud'],
        },
        {
            'name': 'foss_2021b',
            'modules': ['foss/2021b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud'],
        },
        {
            'name': 'foss_2022a',
            'modules': ['foss/2022a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud'],
        },
        {
            'name': 'foss_2023b',
            'modules': ['foss/2023b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud', 'aigert'],
        },
        {
            'name': 'intel',
            'modules': ['intel'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'intel_2019a',
            'modules': ['intel/2019a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'intel_2019b',
            'modules': ['intel/2019b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'intel_2020a',
            'modules': ['intel/2020a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'intel_2020b',
            'modules': ['intel/2020b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera'],
        },
        {
            'name': 'intel_2021a',
            'modules': ['intel/2021a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud'],
        },
        {
            'name': 'intel_2021b',
            'modules': ['intel/2021b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud'],
        },
        {
            'name': 'intel_2022a',
            'modules': ['intel/2022a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'vera', 'UmU-Cloud'],
        },
        {
            'name': 'foss_with_cuda',
            'modules': ['foss/2023b', 'UCX-CUDA/1.15.0-CUDA-12.4.0'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise'],
            'features': ['cuda'],
        },
        {
            'name': 'foss_with_cuda',
            'modules': ['foss/2021b', 'UCX-CUDA/1.11.2-GCCcore-11.2.0-CUDA-11.4.1'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['alvis'],
            'features': ['cuda'],
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
                        'nodelist=%(check_job_nodelist)s|'
                        '%(check_perfvalues)s'
                    ),
                    'format_perfvars': (
                        '%(check_perf_value)s,%(check_perf_unit)s,'
                        '%(check_perf_ref)s,%(check_perf_lower_thres)s,'
                        '%(check_perf_upper_thres)s,'
                    ),
                    'append': True
                }
            ]
        }
    ],
    'modes': [
        {
            'name': 'maintenance',
            'options': [
                '--tag=maintenance',
                '-Sstrict_check=1',
                '-Jreservation=maintenance',
                '--perflogdir=/cephyr/NOBACKUP/priv/c3-staff/reframe/maintenance/perflogs',
                '--report-file=/cephyr/NOBACKUP/priv/c3-staff/reframe/maintenance/reports/maint_report_{sessionid}.json',
                '--stage=/cephyr/NOBACKUP/priv/c3-staff/reframe/maintenance/stage',
                '--output=/cephyr/NOBACKUP/priv/c3-staff/reframe/maintenance/output',
                '--save-log-files',
                '--session-extras=mode=maintenance',
            ],
            'target_systems': ['alvis', 'vera'],
        },
        {
            'name': 'production',
            'options': [
                '--tag=production',
                '-Sstrict_check=1',
                '--perflogdir=/cephyr/NOBACKUP/priv/c3-staff/reframe/production/perflogs',
                '--report-file=/cephyr/NOBACKUP/priv/c3-staff/reframe/production/reports/prod_report_{sessionid}.json',
                '--stage=/cephyr/NOBACKUP/priv/c3-staff/reframe/production/stage',
                '--output=/cephyr/NOBACKUP/priv/c3-staff/reframe/production/output',
                '--save-log-files',
                '--session-extras=mode=production',
            ],
            'target_systems': ['alvis', 'vera'],
        },
        {
            'name': 'maintenance',
            'options': [
                '--tag=maintenance',
                '-Sstrict_check=1',
                '-Jreservation=maintenance',
                '--perflogdir=/pfs/data/reframe/maintenance/perflogs',
                '--report-file=/pfs/data/reframe/maintenance/reports/maint_report_{sessionid}.json',
            ],
            'target_systems': ['kebnekaise'],
        },
        {
            'name': 'production',
            'options': [
                '--tag=production',
                '-Sstrict_check=1',
                '--perflogdir=/pfs/data/reframe/production/perflogs',
                '--report-file=/pfs/data/reframe/production/reports/prod_report_{sessionid}.json',
            ],
            'target_systems': ['kebnekaise'],
        },
    ],
    'general': [
        {
            'check_search_path': ['checks/'],
            'check_search_recursive': True,
            'remote_detect': True,
        },
    ],
    'storage': [
        {
            'enable': True,
            'sqlite_db_file': '/cephyr/NOBACKUP/priv/c3-staff/reframe/results.db',
            'target_systems': ['alvis', 'vera'],
        }
    ],
}
