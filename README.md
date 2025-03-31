# reframe
ReFrame tests for HPC2N and C3SE

Simple use instructions:
 - mkdir reframe-rundir
 - cd reframe-rundir
 - clone the repo into this directory
 - cd hpc2n-reframe-tests
 - Load ReFrame module (4.2 or later)
 - list all available tests:
   reframe -C config/hpc2n+c3se-settings.py -l

To run maintenance tests:
reframe -C config/hpc2n+c3se-settings.py -r -t maintenance
This will run the tests that are tagged with maintenance on all node types (reframe partitions).

To run maintenance test on a specific node:
reframe -C config/hpc2n+c3se-settings.py -r -t maintenance --system alvis:<partition> -J nodelist=alvisx-y
See config/hpc2n+c3se-settings.py for partition names
