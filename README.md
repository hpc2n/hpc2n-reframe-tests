# reframe
ReFrame tests for HPC2N and C3SE

Simple use instructions:
 - mkdir reframe-rundir
 - cd reframe-rundir
 - clone the repo into this directory
 - ln -s hpc2n-checks/checks hpc2ntests
 - Load ReFrame module (4.0 or later)
 - PYTHONPATH=$PWD:$PYTHONPATH
 - list all available tests:
   reframe -C hpc2n-checks/config/hpc2n+c3se-settings.py -c hpc2n-checks -R -l
