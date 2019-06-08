
  - For a list of bug fixes, see 
    https://github.com/radical-cybertools/radical.synapse/issues?q=is%3Aissue+is%3Aclosed+sort%3Aupdated-desc
  - For a list of open issues and known problems, see
    https://github.com/radical-cybertools/radical.synapse/issues?q=is%3Aissue+is%3Aopen+


0.62.0 Release                                                        2019-06-08
--------------------------------------------------------------------------------

   - use OpenMP by default


0.50.0 Release                                                        2018-10-26
--------------------------------------------------------------------------------

   - fix OpenMP configuration during setup


0.46.3 Release                                                        2017-10-27
--------------------------------------------------------------------------------

   - hotfix release to resolve a titan deployment issue


0.46.2 Release                                                        2017-05-12
--------------------------------------------------------------------------------

   - prelimiary support for openMP in compute_asm atoms
   - prelimiary support for multiprocessing in compute_asm atoms


0.44 Release                                                          2016-07-29
--------------------------------------------------------------------------------

   - add hackish setup script to be used in RP CU pre-execs 
   - fix a couple of bugs 
   - implement busy timer 
   - implement named file I/O 
   - make bufsize for disk I/O tunable 
   - more resilience on partial I/O 
   - print warning on empty emulation load 
   - revert to dict based samples, stability, cleanup 


0.43 Release                                                          2016-05-13
--------------------------------------------------------------------------------

  - support file based samples for profile and emulation


0.42 Release                                                          2016-05-09
--------------------------------------------------------------------------------

  - installation fixes, minor other changes


0.41 Release                                                          2016-02-23
--------------------------------------------------------------------------------

  - add walltime sampler
  - replace multiprocessing.Queue with Queue.Queue (former breaks on Gordon)


0.40 Release                                                          2016-02-10
--------------------------------------------------------------------------------

  - add a CHANGES.md :)
  - make RADICAL_SYNAPSE_WATCHMODE default to None on emulate()

--------------------------------------------------------------------------------

