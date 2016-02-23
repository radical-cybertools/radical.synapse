
Synapse - SYNthetic Application ProfileS and Emulation 
======================================================

Goal: emulate an applications runtime behavior as realistically as possible

    * emulate the application's execution structure (components and relations)
    * consume same amount of resources (CPU, Mem, Disk, Network)

At the same time, a Synapse instance is also parameterizable, so as to vary its
structure and resource consumption -- without needing to tweak an application
code.  Parameterization can be static, dynamic, according to some distribution,
etc.

Initial parameters are obtained by profiling applications
(`radical.synapse.profile`).  Synapse runs are also profiled again, to
verify correct emulation -- see [figure 1][experiments/synapse_mandelbrot_boskop.png]

Figure 1: Mandelbrot as master-worker implementation -- measure TTC on a single
worker instance with varying problem size (sub-image size), and compare to
a synapse emulation of the same worker.  The synapse data include times for the
individually contributing load types (disk, mem, cpu).  For small problem sizes,
noise in the load generation, startup overhead and self-profiling overhead are
clearly visible -- for larger problems that quickly *constant* overhead is
negligible (>10 seconds ttc).

Profiling
---------

Uses linux command line tools (not always available):


    *   `/usr/bin/time -v` for max memory consumption: 

        ```
        $ /usr/bin/time -v      python -c 'for i in range (1,10000000): j = i*3.1415926'
        	Command being timed: "python -c  for i in range (1,10000000): j = i*3.1415926"
        	User time (seconds): 1.84
        	System time (seconds): 0.46
        	Percent of CPU this job got: 46%
        	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:05.00
            ...
        	Maximum resident set size (kbytes): 322072
            ...
        ```

        * memory consumption reports seem correct - but do not detail
          distribution over time, looks like one chunk.
        * wallclocktime includes profiling time, better to measure wallclock
          separately
        * alternative if code can be instrumented (`synapse.utils.get_mem_usage`), 
          which evaluates `/proc/[pid]/status`.


    *   `/usr/bin/time -f %e` for TTC:

        ```
        $ /usr/bin/time -f %e python -c 'for i in range (1,10000000): j = i*3.1415926'
        1.82
        ```


    *   `/usr/bin/perf stat` for CPU utilization (needs kernel support):

        ```
        $ /usr/bin/perf stat            python -c 'for i in range (1,10000000): j = i*3.1415926'
         Performance counter stats for 'python -c  for i in range (1,10000000): j = i*3.1415926':
        
               1928.356169 task-clock                #    0.993 CPUs utilized          
                       185 context-switches          #    0.096 K/sec                  
                        64 CPU-migrations            #    0.033 K/sec                  
                    80,648 page-faults               #    0.042 M/sec                  
             6,158,591,568 cycles                    #    3.194 GHz                     [83.25%]
             2,427,203,057 stalled-cycles-frontend   #   39.41% frontend cycles idle    [83.25%]
             1,758,381,453 stalled-cycles-backend    #   28.55% backend  cycles idle    [66.65%]
             8,898,332,744 instructions              #    1.44  insns per cycle        
                                                     #    0.27  stalled cycles per insn [83.26%]
             2,037,169,952 branches                  # 1056.428 M/sec                   [83.44%]
                28,412,079 branch-misses             #    1.39% of all branches         [83.51%]
        
               1.941766011 seconds time elapsed
        ```

        * 8 instructions ~~ 1 FLOP (architecture dependent)
        * CPU efficiency not yet evaluated, will be added soon-ish
        * it is difficult to emulate exact CPU consumption structure 
          (branching, cache misses, idle cycles) -- using assembler 
          instead of C helps a little...
        * `perf` is quick (only reads kernel counters)


    *   `cat /proc/[pid]/io` for disk I/O counters:

        ```
        $ python -c 'for i in range (1,10000000): j = i*3.1415926' &  cat /proc/$!/io
        [3] 2110
        rchar: 7004
        wchar: 0
        syscr: 13
        syscw: 0
        read_bytes: 0
        write_bytes: 0
        cancelled_write_bytes: 0
        ```

        * timing is problematic, needs constant watching, as it disappears with
          the process
        * works ok if code can be instrumented (`synapse.utils.get_io_usage`)

    *   complete profile command:

        `sh -c '/usr/bin/time -v /usr/bin/perf stat /usr/bin/time -f %e python mandelbrot.py'`

    *   For applications under our control (mandelbrot.py), we also use some 

    *   For self_profiling, we use `getrusage(2)`, which is embedded into the
        synapse atoms.


Emulation:
----------

The synapse incarnation of the above would be:

```
import time
import radical.synapse as rs


start = time.time ()
rsa_c = rs.atoms.Compute ()
rsa_m = rs.atoms.Memory  ()
rsa_s = rs.atoms.Storage ()

rsa_c.run (info={'n'   : 1100})   # consume  1.1 GFlop Cycles
rsa_m.run (info={'n'   :  322})   # allocate 0.3 GByte memory
rsa_s.run (info={'n'   :    0,    # write    0.0 GByte to disk
                 'mode': 'w',     # write mode!
                 'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})

# atoms are now working in separate threads - wait for them.

info_c = rsa_c.wait ()
info_m = rsa_m.wait ()
info_s = rsa_s.wait ()
stop   = time.time ()

# info now contains self-profiled information for the atoms
print "t_c: %.2f" % info_c['timer']
print "t_m: %.2f" % info_m['timer']
print "t_s: %.2f" % info_s['timer']
print "ttc: %.2f" % (stop - start)
```

which will result in something like:

```
t_c: 1.84
t_m: 1.38
t_s: 0.03
ttc: 1.85
```

Atom Implementation
-------------------

    * framework / controller in python (see example above)

    * atom cores as small snippets of C and Assembler code

      Python code has significant overhead, and is hard to predict what
      operation result in how many instructions.  Controlling memory consumption
      is even more difficult -- thus the decision for C/ASM

    * code is ANSI-C, and compiled on the fly -- tiny overhead on first 
      invocation:
      ```
      $ /usr/bin/time -f %e cc -O0 synapse/atoms/synapse_storage.c 
      0.06
      ```
      (same for all atoms, dominated by CC startup and parsing)

    * for actual code, see `synapse/atoms/synapse_{compute,memory,storage}.c` 
      -- very small and accessible (IMHO), `rusage` report is about 30% of it,
      in total about 60 unique lines of code:
      ```
      $ sloccount synapse/atoms/synapse_{compute,memory,storage}.c | grep ansic
      ansic:          170 (100.00%)

      $ cat synapse/atoms/synapse_{compute,memory,storage}.c | sort -u | grep -v print > t.c ; sloccount t.c | grep ansic
      ansic:           60 (100.00%)
      ```   

    * alternative assembler based compute atom can better reproduce CPU
      utilization -- still not tunable though.  

    * code may grow for better tuning (memory and disk I/O chunksize, CPU 
      intruction types, etc)


Future Plans
------------

    * complete network atom (can already to basic point-to-point)
    * add MPI atom
    * improve composability, via control files
    * add support for statistic load distributions (simple, on python level)


