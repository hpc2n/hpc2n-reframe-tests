# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

#
# Hooks specific to the HPC2N GPU microbenchmark tests.
#


def set_gpu_arch(self):
    '''Set the compile options for the gpu microbenchmarks.'''

    cs = self.current_system.name
    cp = self.current_partition.fullname
    cn = self.current_partition.name
    self.gpu_arch = None

    # Nvidia options
    self.gpu_build = 'cuda'
    if cs in {'alvis', 'kebnekaise'}:
        if 'K80' in cn:
            self.gpu_arch = '37'
        if 'V100' in cn:
            self.gpu_arch = '70'
        if 'T4' in cn:
            self.gpu_arch = '75'
        if 'A40' in cn:
            self.gpu_arch = '86'
        if 'A100' in cn:
            self.gpu_arch = '80'
    elif cs in {'dom', 'daint'}:
        self.gpu_arch = '60'
        if self.current_environ.name not in {'PrgEnv-nvidia'}:
            self.modules = ['craype-accel-nvidia60', 'cdt-cuda']
        else:
            self.modules = ['cdt-cuda/21.05']

    elif cs in {'arola', 'tsa'}:
        self.gpu_arch = '70'
        self.modules = ['cuda/10.1.243']
    elif cs in {'ault'}:
        self.modules = ['cuda']
        if cp in {'ault:amdv100', 'ault:intelv100'}:
            self.gpu_arch = '70'
        elif cp in {'ault:amda100'}:
            self.gpu_arch = '80'

    # AMD options
    if cp in {'ault:amdvega'}:
        self.gpu_build = 'hip'
        self.modules = ['rocm']
        self.gpu_arch = 'gfx900,gfx906'


def set_num_gpus_per_node(self):
    '''Set the GPUs per node for the GPU microbenchmarks.'''

    cs = self.current_system.name
    cp = self.current_partition.fullname
    cn = self.current_partition.name

    if cs in {'alvis', 'kebnekaise'}:
        if cn in {'gpu_1xK80', 'gpu_2xV100'}:
            self.num_gpus_per_node = 2
        elif cn in {'gpu_2xK80', 'NxV100', 'NxA100'}:
            self.num_gpus_per_node = 4
        elif cn in {'gpu_4xK80', 'NxT4'}:
            self.num_gpus_per_node = 8
    elif cs in {'dom', 'daint'}:
        self.num_gpus_per_node = 1
    elif cs in {'arola', 'tsa'}:
        self.num_gpus_per_node = 8
    elif cp in {'ault:amda100', 'ault:intelv100'}:
        self.num_gpus_per_node = 4
    elif cp in {'ault:amdv100'}:
        self.num_gpus_per_node = 2
    elif cp in {'ault:amdvega'}:
        self.num_gpus_per_node = 3
    else:
        self.num_gpus_per_node = 1
