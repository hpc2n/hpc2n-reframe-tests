# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import reframe as rfm
import reframe.utility.sanity as sn
import reframe.utility.typecheck as typ
import microbenchmarks.gpu.hooks as hooks

from reframe.core.backends import getlauncher

@rfm.simple_test
class nvidia_smi_check(rfm.RunOnlyRegressionTest):
    gpu_mode = parameter(['compute', 'ecc'])
    valid_systems = ['+nvgpu']
    valid_prog_environs = ['builtin']
    executable = 'nvidia-smi'
    executable_opts = ['-a', '-d']
    num_tasks = 1
    num_tasks_per_node = 1
    exclusive = True
    tags = {'maintenance', 'production', 'reboot'}
    maintainers = ['AS']
    mode_values = variable(typ.Dict[str, str], value={
        'accounting': 'Enabled',
        'compute': 'Default',
        'ecc': 'Enabled'
    })

    @run_before('run')
    def set_display_opt(self):
        self.executable_opts.append(self.gpu_mode.upper())

    @run_before('sanity')
    def set_sanity(self):
        modeval = self.mode_values[self.gpu_mode]
        if self.gpu_mode == 'ecc':
            patt = rf'Current\s+: {modeval}'
        else:
            patt = rf'{self.gpu_mode.capitalize()} Mode\s+: {modeval}'

        num_gpus_detected = sn.count(sn.findall(patt, self.stdout))
        num_gpus_all = self.num_tasks

        # We can't use an f-string here, because it will misinterpret the
        # placeholders for the sanity function message
        errmsg = ('{0} out of {1} GPU(s) have the correct %s mode' %
                  self.gpu_mode)
        self.sanity_patterns = sn.assert_eq(
            num_gpus_detected, num_gpus_all, errmsg
        )

    @run_after('setup')
    def set_launcher(self):
        self.job.launcher = getlauncher('local')()

    @run_before('run')
    def set_num_gpus_per_node(self):
        hooks.set_num_gpus_per_node(self)
        self.num_tasks = self.num_gpus_per_node
        self.num_tasks_per_node = self.num_gpus_per_node
