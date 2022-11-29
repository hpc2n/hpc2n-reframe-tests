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
            'hostnames': ['alvis'],
            'modules_system': 'lmod',
            'partitions': [
                {
                    'name': 'NxT4',
                    'descr': 'GPU T4',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2021-5-261', '-C 8xT4'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=T4:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'NxV100',
                    'descr': 'GPU V100',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2021-5-261', '-C 2xV100'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=V100:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'NxA100_MEM768',
                    'descr': 'GPU A100 nodes with 768G memory and 2x16 cores',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C MEM768'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=A100:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'NxA100_MEM256',
                    'descr': 'GPU A100 nodes with 256G memory and 2x32 cores',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C MEM256'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=A100:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'NxA100_MEM512',
                    'descr': 'GPU A100 nodes with 512G memory and 2x32 cores',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C MEM512'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=A100:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'NxA100fat',
                    'descr': 'GPU A100 fat nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 4xA100fat'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=A100fat:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': 'NxA40',
                    'descr': 'GPU A40',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C 4xA40'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'resources': [
                        {
                            'name': '_rfm_gpu',
                            'options': ['--gpus-per-node=A40:{num_gpus_per_node}'],
                        },
                    ],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '2xV100',
                    'descr': 'GPU 2xV100 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A SNIC2021-5-261', '-C 2xV100', '--gpus-per-node=V100:2'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'access': ['-A SNIC2021-5-261', '-C 4xV100', '--gpus-per-node=V100:4'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'access': ['-A SNIC2021-5-261', '-C 8xT4', '--gpus-per-node=T4:8'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                        },
                    ],
                },
                {
                    'name': '4xA100_MEM768',
                    'descr': 'GPU 4xA100 nodes with 768G memory and 2x16 cores',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A C3SE-STAFF', '-C MEM768', '--gpus-per-node=A100:4'],
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'foss_with_cuda', 'fosscuda', 'fosscuda_2019b', 'fosscuda_2020a', 'fosscuda_2020b', 'foss_2021a', 'intelcuda_2019b', 'intelcuda_2020a', 'intelcuda_2020b', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'foss_2021a', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_1xK80',
                    'descr': 'GPU 1xK80 half node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&2xK80', '--gres=gpu:k80:1'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_2xK80',
                    'descr': 'GPU 2xK80 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&2xK80', '--gres=gpu:k80:2', '--exclusive'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_4xK80',
                    'descr': 'GPU 4xK80 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&4xK80', '--gres=gpu:k80:4', '--exclusive'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_1xV100',
                    'descr': 'GPU 1xV00 half node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C skylake&2xV100', '--gres=gpu:v100:1'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_2xV100',
                    'descr': 'GPU 2xV00 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C skylake&2xV100', '--gres=gpu:v100:2', '--exclusive'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '2xA40',
                    'descr': 'GPU 2xA40 half node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&4xA40', '--gres=gpu:a40:2'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': '4xA40',
                    'descr': 'GPU 4xA40 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&4xA40', '--gres=gpu:a40:4', '--exclusive'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_1xA6000',
                    'descr': 'GPU 1xA6000 half node',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&2xA6000', '--gres=gpu:a6000:1'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'gpu_2xA6000',
                    'descr': 'GPU 2xA6000 nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-A sysop', '-p gpu', '-C broadwell&2xA6000', '--gres=gpu:a6000:2', '--exclusive'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_with_cuda', 'fosscuda', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
                    'container_platforms': [
                        {
                            'type': 'Singularity',
                            'modules': ['singularity'],
                        },
                    ],
                },
                {
                    'name': 'knl',
                    'descr': 'KNL compute nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': ['-p knl', '-A sysop'],
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
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
                    'environs': ['builtin', 'gnu', 'foss', 'intel', 'foss_2019a', 'foss_2019b', 'foss_2020a', 'foss_2020b', 'foss_2021a', 'intel_2019a', 'intel_2019b', 'intel_2020a', 'intel_2020b', 'intel_2021a', 'intel_2022a'],
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
            'target_systems': ['kebnekaise', 'alvis', 'UmU-Cloud'],
        },
        {
            'name': 'foss_2019a',
            'modules': ['foss/2019a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'foss_2019b',
            'modules': ['foss/2019b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'foss_2020a',
            'modules': ['foss/2020a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'foss_2020b',
            'modules': ['foss/2020b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'foss_2021a',
            'modules': ['foss/2021a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'UmU-Cloud'],
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
            'name': 'intel_2019a',
            'modules': ['intel/2019a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intel_2019b',
            'modules': ['intel/2019b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intel_2020a',
            'modules': ['intel/2020a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intel_2020b',
            'modules': ['intel/2020b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intel_2021a',
            'modules': ['intel/2021a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'UmU-Cloud'],
        },
        {
            'name': 'intel_2022a',
            'modules': ['intel/2022a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis', 'UmU-Cloud'],
        },
        {
            'name': 'foss_with_cuda',
            'modules': ['foss/2021b', 'UCX-CUDA'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis', 'UmU-Cloud'],
	    'features': ['cuda'],
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
            'name': 'fosscuda_2019a',
            'modules': ['fosscuda/2019a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'fosscuda_2019b',
            'modules': ['fosscuda/2019b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'fosscuda_2020a',
            'modules': ['fosscuda/2020a'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'fosscuda_2020b',
            'modules': ['fosscuda/2020b'],
            'cc': 'gcc',
            'cxx': 'g++',
            'ftn': 'gfortran',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intelcuda_2019b',
            'modules': ['intelcuda/2019b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['kebnekaise', 'alvis'],
        },
        {
            'name': 'intelcuda_2020a',
            'modules': ['intelcuda/2020a'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['alvis'],
        },
        {
            'name': 'intelcuda_2020b',
            'modules': ['intelcuda/2020b'],
            'cc': 'icc',
            'cxx': 'icpc',
            'ftn': 'ifort',
            'target_systems': ['alvis'],
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
