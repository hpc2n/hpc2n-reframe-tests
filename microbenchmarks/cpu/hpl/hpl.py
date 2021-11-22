# Copyright 2016-2021 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# ReFrame Project Developers. See the top-level LICENSE file for details.
#
# SPDX-License-Identifier: BSD-3-Clause

import os
import re

import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
import reframe.utility.udeps as udeps

from reframe.core.backends import getlauncher


class HPLBase(rfm.RunOnlyRegressionTest):
    '''Base class of new HPL test'''

    def __init__(self):
        self.executable = 'xhpl'

        self.perf_patterns = {
            'GFlops': sn.max(sn.extractall(
                rf'^\S+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\.\d+\s+(\d+\.\d+e\+\d+)$',
                self.stdout, 1, float)),
        }

        self.tags = {'production', 'reboot', 'maintenance'}
        self.maintainers = ['ÅS']

    @run_after('init')
    def apply_module_info(self):
        module_info = util.find_modules('HPL')
        for s, e, m in module_info:
            if 'foss_' in e:
                self.valid_systems = [s]
                self.valid_prog_environs = [e]
                self.modules = [m]

    @run_after('setup')
    def setup_HPL_data(self):
        '''Create the HPL.dat input file'''

        N = self.values.get('N', 1000)
        if not isinstance(N, list):
            N = [N]
        NB = self.values.get('NB', 100)
        if not isinstance(NB, list):
            NB = [NB]
        P = self.values.get('P', 1)
        if not isinstance(P, list):
            P = [P]
        Q = self.values.get('Q', 1)
        if not isinstance(Q, list):
            Q = [Q]

        Ns = len(N)
        N = ' '.join(map(str, N))
        NBs = len(NB)
        NB = ' '.join(map(str, NB))
        PQs = len(P)
        if len(Q) != PQs:
            raise ValueError('Number of Ps != number of Qs')
        for idx, v in enumerate(P):
            nt = max(v*Q[idx], 1)

        self.num_cases = Ns*NBs*PQs
        self.num_tasks = nt

        self.sanity_patterns = sn.assert_eq(sn.extractsingle(r'^\s+(\d+)\s+tests completed and passed residual checks,', self.stdout, 1, int), self.num_cases)

        P = ' '.join(map(str, P))
        Q = ' '.join(map(str, Q))

        regex_subs = [
            (r'^[\d\s]+# of problems sizes', f"{Ns} # of problems sizes"),
            (r'^[\d\s]+Ns', f"{N} Ns"),
            (r'^[\d\s]+# of NBs', f"{NBs} # of NBs"),
            (r'^[\d\s]+NBs', f"{NB} NBs"),
            (r'^[\d\s]+# of process grids', f"{PQs} # of process grids"),
            (r'^[\d\s]+Ps', f"{P} Ps"),
            (r'^[\d\s]+Qs', f"{Q} Qs"),
        ]
        compiled_regex_subs = [(re.compile(regex), subtxt) for (regex, subtxt) in regex_subs]

        with open(os.path.join(self.stagedir, 'HPL.dat'), 'w') as H:
            with open(os.path.join(self.prefix, self.sourcesdir, 'HPL.dat.tmpl')) as f:
                for line in f:
                    for regex, subtxt in compiled_regex_subs:
                        match = regex.search(line)
                        if match:
                            line = regex.sub(subtxt, line)
                    H.write(line)

@rfm.simple_test
class HPLBaseSingleNode_Fixed(HPLBase):
    '''HPL on single nodes'''

    def __init__(self):
        super().__init__()

        self.hpl_settings = {
            'kebnekaise:bdw': {'N': 107520, 'NB': 192, 'P': 7, 'Q': 4},
            'kebnekaise:skx': {'N': 107520, 'NB': 192, 'P': 7, 'Q': 4},
        }

        self.reference = {
            'kebnekaise:bdw': {
                'GFlops': (871, -0.05, 0.05, 'GFlops/s'),
            }
            'kebnekaise:skx': {
                'GFlops': (871, -0.05, 0.05, 'GFlops/s'),
            }
        }

    @run_after('setup')
    def prepare_test(self):
        self.values = self.hpl_settings.get(self.current_partition.fullname, {})

