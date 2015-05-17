#!/usr/bin/env gnuplot

print "experiment  : " . experiment
print "max runtime : " . max_runtime
print "max time    : " . max_time
print "samples     : " . max_tasks
print "mode        : " . mode


ntasks = 100
flops  = 100000
rtime  = 25

term   = 'png'
term_t = term.'cairo'


    set key box Right right

    # runtime
    set style line 100 lt 1 lc rgb '#FF3300' pt 6 ps 1.0 lw 2

    # io read/write
    set style line 201 lt 1 lc rgb '#000066' pt 6 ps 1.0 lw 2
    set style line 202 lt 1 lc rgb '#6666FF' pt 6 ps 1.0 lw 2
    set style line 211 lt 1 lc rgb '#000066' pt 6 ps 0.0 lw 1.5
    set style line 212 lt 1 lc rgb '#6666FF' pt 6 ps 0.0 lw 1.5

    # mem rss/size/peak
    set style line 301 lt 1 lc rgb '#006600' pt 6 ps 1.0 lw 2
    set style line 302 lt 1 lc rgb '#339933' pt 6 ps 1.0 lw 2
    set style line 303 lt 1 lc rgb '#66FF66' pt 6 ps 1.0 lw 2
    set style line 311 lt 1 lc rgb '#006600' pt 6 ps 0.0 lw 1.5
    set style line 312 lt 1 lc rgb '#339933' pt 6 ps 0.0 lw 1.5
    set style line 313 lt 1 lc rgb '#66FF66' pt 6 ps 0.0 lw 1.5

  # set style line 103 lt 1 lc rgb '#AA6666' pt 6 ps 0.4 lw 1
  # set style line 104 lt 1 lc rgb '#FF9944' pt 7 ps 0.6 lw 3
  # set style line 105 lt 2 lc rgb '#AA6666' pt 7 ps 0.6 lw 3
  # set style line 106 lt 1 lc rgb '#AA6666' pt 7 ps 0.6 lw 2
  #
  # set style line 200 lt 1 lc rgb '#99FF44' pt 7 ps 3.0 lw 2
  # set style line 201 lt 1 lc rgb '#66AA66' pt 6 ps 0.4 lw 1
  # set style line 202 lt 1 lc rgb '#99FF44' pt 7 ps 0.6 lw 2
  # set style line 203 lt 1 lc rgb '#66AA66' pt 6 ps 0.4 lw 1
  # set style line 204 lt 1 lc rgb '#99FF44' pt 7 ps 0.6 lw 3
  # set style line 205 lt 2 lc rgb '#66AA66' pt 7 ps 0.6 lw 3
  # set style line 206 lt 1 lc rgb '#66AA66' pt 7 ps 0.6 lw 2
  #
  # set style line 300 lt 1 lc rgb '#9944FF' pt 7 ps 1.0 lw 2
  # set style line 301 lt 1 lc rgb '#6666AA' pt 6 ps 0.4 lw 1
  # set style line 302 lt 1 lc rgb '#9944FF' pt 7 ps 0.6 lw 2
  # set style line 303 lt 1 lc rgb '#6666AA' pt 6 ps 0.4 lw 1
  # set style line 304 lt 1 lc rgb '#9944FF' pt 7 ps 0.6 lw 3
  # set style line 305 lt 2 lc rgb '#6666AA' pt 7 ps 0.6 lw 3
  # set style line 306 lt 1 lc rgb '#6666AA' pt 7 ps 0.6 lw 2

    set term term_t enhanced color dashed

    # -------------------------------------------------------------------------------------------

    set grid
    set tics    scale 2
  # set mxtics  auto
  # set mytics  auto
    set ytics   nomirror

    scale=1

    set output "./rs_".experiment.".cpu.tot.ops.".mode.".png"
    set title   "Total CPU Usage vs Application Runtime"
    set xlabel  "tasks (sorted by runtime)"
    set xrange  [0:max_tasks+1]
    set ylabel  "total operations (MFLOPs)"
    set yrange  [0:max_tot_ops/scale]
    set y2label "task runtime (s)"
    set y2tics  auto
    set y2range [0:max_runtime]

    plot "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($3/scale) with linespoints ls 401 title 'ops'   ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($4/scale) with linespoints ls 403 title 'flops' ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($2      ) with linespoints ls 100 title 'runtime' axes x1y2


    scale=100
    set output "./rs_".experiment.".cpu.tot.eff.".mode.".png"
    set title   "Total CPU Utilization vs Application Runtime"
    set xlabel  "tasks (sorted by runtime)"
    set xrange  [0:max_tasks+1]
    set ylabel  "cpu utilization / efficiency (%)"
    set yrange  [0:100]
    set y2label "task runtime (s)"
    set y2tics  auto
    set y2range [0:max_runtime]

    plot "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($5*scale) with linespoints ls 401 title 'efficiency'  ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($6*scale) with linespoints ls 403 title 'utilization' ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($2      ) with linespoints ls 100 title 'runtime' axes x1y2


    # -------------------------------------------------------------------------------------------

    scale=1024*1024

    set output "./rs_".experiment.".cpu.inc.ops.".mode.".png"
    set title   "CPU Usage over Application Runtime"
    set xlabel  "task runtime (s)"
    set xrange  [0:*]
    set ylabel  "operations (MOPS / MFLOPs)"
    set yrange  [0:*]
    set y2label ""
  unset y2tics  
  unset y2range 

    plot "/tmp/rs_".experiment.".cpu.inc.dat" using 2:($3/scale) with linespoints ls 411 title 'ops'  ,\
         "/tmp/rs_".experiment.".cpu.inc.dat" using 2:($4/scale) with linespoints ls 413 title 'flops' ,\


    # -------------------------------------------------------------------------------------------

    scale=1024*1024

    set output "./rs_".experiment.".cpu.acc.ops.".mode.".png"
    set title   "Accumulated CPU Usage over Application Runtime"
    set xlabel  "task runtime (s)"
    set xrange  [0:*]
    set ylabel  "accumulated operations (MOPS / MFLOPS)"
    set yrange  [0:*]
    set y2label ""
  unset y2tics  
  unset y2range 

    plot "/tmp/rs_".experiment.".cpu.acc.dat" using 2:($3/scale) with linespoints ls 211 title 'ops'


    # -------------------------------------------------------------------------------------------
    # I/O
    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Total I/O vs Application Runtime"
    set xlabel  "task (sorted by runtime)"
    set xrange  [0:max_tasks+1]
    set ylabel  "accumulated read / write (kByte)"
    set yrange  [0:(max_tot_io/scale)]
    set y2label "task runtime (s)"
    set y2tics  auto
    set y2range [0:max_runtime]

    set output "./rs_".experiment.".io.tot.".mode.".png"
    plot "/tmp/rs_".experiment.".io.tot.dat" using 1:($3/scale) with linespoints ls 201 title 'read'  ,\
         "/tmp/rs_".experiment.".io.tot.dat" using 1:($4/scale) with linespoints ls 202 title 'write' ,\
         "/tmp/rs_".experiment.".io.tot.dat" using 1:($2      ) with linespoints ls 100 title 'runtime' axes x1y2

    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "I/O over Application Runtime"
    set xlabel  "runtime (s)"
    set xrange  [0:max_time]
    set ylabel  "read / write (kByte)"
    set yrange  [0:(max_inc_io/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".io.inc.".mode.".png"
    plot "/tmp/rs_".experiment.".io.inc.dat" using 2:($3/scale) with linespoints ls 211 title 'read'  ,\
         "/tmp/rs_".experiment.".io.inc.dat" using 2:($4/scale) with linespoints ls 212 title 'write' 


    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Accumulated I/O over Application Runtime"
    set xlabel  "runtime (s)"
    set xrange  [0:max_time]
    set ylabel  "accumulated read / write (kByte)"
    set yrange  [0:(max_tot_io/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".io.acc.".mode.".png"
    plot "/tmp/rs_".experiment.".io.acc.dat" using 2:($3/scale) with linespoints ls 211 title 'read'  ,\
         "/tmp/rs_".experiment.".io.acc.dat" using 2:($4/scale) with linespoints ls 212 title 'write' 


    # -------------------------------------------------------------------------------------------
    # MEM
    # -------------------------------------------------------------------------------------------

    scale=1024*1024

    set term    term_t enhanced color dashed
    set output "./rs_".experiment.".mem.tot.".mode.".png"

    print max_time

    set title   "Total Memory Usage vs Application Runtime"
    set xlabel  "task (sorted by runtime)"
    set xrange  [0:max_tasks+1]
    set ylabel  "total memory (MByte)"
    set yrange  [0:max_tot_mem/scale]
    set y2label "task runtime (s)"
    set y2tics  auto
    set y2range [0:max_runtime]

    plot "/tmp/rs_".experiment.".mem.tot.dat" using 1:($3/scale) with linespoints ls 301 title 'rss'  ,\
         "/tmp/rs_".experiment.".mem.tot.dat" using 1:($4/scale) with linespoints ls 303 title 'peak' ,\
         "/tmp/rs_".experiment.".mem.tot.dat" using 1:($2      ) with linespoints ls 100 title 'runtime' axes x1y2
                                         
       # "/tmp/rs_".experiment.".mem.tot.dat" using 1:($4/scale) with linespoints ls 302 title 'size' ,\

    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Memory Usage over Application Runtime"
    set xlabel  "runtime (s)"
    set xrange  [0:max_time]
    set ylabel  "accumulated memory (kByte)"
    set yrange  [0:(max_inc_mem/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".mem.inc.".mode.".png"
    plot "/tmp/rs_".experiment.".mem.inc.dat" using 2:($3/scale) with linespoints ls 311 title 'rss'  ,\
         "/tmp/rs_".experiment.".mem.inc.dat" using 2:($4/scale) with linespoints ls 313 title 'size' 



    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Accumulated Memory Usage over Application Runtime"
    set xlabel  "runtime (s)"
    set xrange  [0:max_time]
    set ylabel  "accumulated memory (kByte)"
    set yrange  [0:(max_tot_mem/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".mem.acc.".mode.".png"
    plot "/tmp/rs_".experiment.".mem.acc.dat" using 2:($3/scale) with linespoints ls 311 title 'rss'  ,\
         "/tmp/rs_".experiment.".mem.acc.dat" using 2:($4/scale) with linespoints ls 313 title 'size' 


    # -------------------------------------------------------------------------------------------

    exit


    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------

    set xlabel  "time (s)"
    set ylabel  "memory  (kByte)"
    set ytics  5000
    set y2label ""
    set y2tics  ""
    set title   "Memory Allocation over Application Runtime"

    set output "./rs_".experiment.".mem.".mode.".png"
    plot "/tmp/rs_".experiment.".mem.dat" using 1:($2/1024) with linespoints pt 7 ps 0.3 lt 206 title 'total size',\
         "/tmp/rs_".experiment.".mem.dat" using 1:($3/1024) with linespoints pt 7 ps 0.3 lt 306 title 'resident size'


    # -------------------------------------------------------------------------------------------

    set xlabel  "task instance (sorted by runtime)"
    set ylabel  "efficiency/utilization (%)"
    set ytics   auto
    set y2label "FLOPs (s)"
    set y2tics  auto

    set xrange  [0:ntasks]
    set yrange  [0:100]
    set y2range [0:flops]
    set title   "CPU Consumption over Application Runtime"

    set output "./rs_".experiment.".cpu.".mode.".png"
    plot "/tmp/rs_".experiment.".cpu.dat" using 1:($4*100) with points pt 6 ps 0.5 lt 206 title 'FLOPs' axes x1y2 ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($4*100) with points pt 6 ps 0.5 lt 206 title 'efficiency'  ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($5*100) with points pt 1 ps 0.5 lt 307 title 'utilization'


    # -------------------------------------------------------------------------------------------

    set xlabel  "task instance (sorted by runtime)"
    set ylabel  "efficiency/utilization (%)"
    set ytics   auto
    set y2label "runtime (s)"
    set y2tics  auto

    set xrange  [0:ntasks]
    set yrange  [0:100]
    set y2range [0:rtime]
    set title   "Computation Efficiency vs. Application Runtime"

    set output "./rs_".experiment.".cpu_1.".mode.".png"
    plot "/tmp/rs_".experiment.".cpu.dat" using 1:($4*100) with points pt 6 ps 0.5 lt 206 title 'efficiency'  ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($5*100) with points pt 1 ps 0.5 lt 307 title 'utilization' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($6*1  ) with points pt 6 ps 0.5 lt 308 title 'runtime' axes x1y2


    # -------------------------------------------------------------------------------------------

    set xlabel  "task instance (sorted by runtime)"
    set ylabel  "Mega-FLOPs"
    set ytics  auto
    set y2label "runtime (s)"
    set y2tics  auto

    set xrange  [0:ntasks]
    set yrange  [0:flops]
    set y2range [0:rtime]
    set title   "CPU Cycle Consumption vs. Application Runtime"

    set output "./rs_".experiment.".cpu_2.".mode.".png"
    plot "/tmp/rs_".experiment.".cpu.dat" using 1:($3/1024/1024) with points pt 6 ps 0.5 lt 306 title 'MegaFLOPs' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($6*1        ) with points pt 6 ps 0.5 lt 308 title 'runtime' axes x1y2


    # -------------------------------------------------------------------------------------------

    set xlabel  "task instance (sorted by runtime)"
    set ylabel  "CPU (Mega-Flops) / utilization (rel) / read (kBytes)"
    set ytics  auto
    set y2label "runtime (s)"
    set y2tics  auto

    set xrange  [0:ntasks]
    set yrange  [0:flops]
    set y2range [0:rtime]
    set title   "Relation between Resource Consumption and Runtime"

    set output "./rs_".experiment.".cpu_3.".mode.".png"
    plot "/tmp/rs_".experiment.".cpu.dat" using 1:($7/1024     ) with lines              lt 301 title 'read' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($3/1024/1024) with points pt 6 ps 0.5 lt 306 title 'MegaFLOPs' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($5*2        ) with points pt 1 ps 0.5 lt 307 title 'utilization'  axes x1y2 ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($6          ) with points pt 6 ps 0.5 lt 308 title 'runtime'      axes x1y2


    # -------------------------------------------------------------------------------------------

    set autoscale
    set xrange  [0:ntasks]
    set xlabel  "task instance (sorted by runtime)"
    set ylabel  "FLOPs/time (normalized)"
    set ytics  1
    set y2label "runtime (s)"
    set y2tics  auto

    set xrange  [0:ntasks]
    set yrange  [0:6.5]
    set y2range [0:rtime]
    set title   "Relation between Resource Consumption Rate and Runtime"
    set output "./rs_".experiment.".cpu_4.".mode.".png"
    plot "/tmp/rs_".experiment.".cpu.dat" using 1:(1/($4*$5)) with lines lt 306 title '(FLOPs/time)^-1' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($6       ) with linespoints pt 6 ps 0.5 lt 308 title 'runtime' axes x1y2 ,\

    # -------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------

    set autoscale
    set xrange  [0:ntasks]
    set xlabel  "task instance (sorted by runtime)"
    set ylabel  "ops"
    set yrange  [0:]
    set y2range [0:]
    set ytics   auto
  # set y2label "runtime (s)"
  # set y2tics  auto
    set title   "Memory Consumption and Disk Read over Application Runtime"

    flops_1=13600000000.0/4/4 # BG
    flops_2=10680000000.0   # PC

    set output "./rs_".experiment.".test.".mode.".png"
    plot "/tmp/rs_".experiment.".cpu.dat" using 1:($3/$4/$5/flops_1) with      points pt 7 ps 0.3 lt 206 title 'pred bg' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($3/$4/$5/flops_2) with      points pt 7 ps 0.3 lt 207 title 'pred pc' ,\
         "/tmp/rs_".experiment.".cpu.dat" using 1:($6              ) with linespoints pt 6 ps 0.5 lt 308 title 'runtime'


