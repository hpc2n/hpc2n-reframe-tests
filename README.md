# reframe
ReFrame tests for HPC2N and C3SE

Simple use instructions:
 - mkdir reframe-rundir
 - cd reframe-rundir
 - clone the repo into this directory
 - cd hpc2n-reframe-tests
 - Load ReFrame module (4.0 or later)
 - PYTHONPATH=$PWD/checks:$PYTHONPATH
 - list all available tests:
   reframe -C config/hpc2n+c3se-settings.py -l
