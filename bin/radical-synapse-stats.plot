#!/usr/bin/env gnuplot

print "experiment  : " . experiment
print "max ttc     : " . max_ttc
print "max time    : " . max_time
print "samples     : " . max_tasks
print "modes       : " . modes


term   = 'png'
term_t = term.'cairo'


    set key box Right right

    # ttc
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

    set output "./rs_".experiment.".cpu.tot.ops.".modes.".png"
    set title   "Total CPU Usage vs Task TTC"
    set xlabel  "tasks (sorted by ttc)"
    set xrange  [0:max_tasks+1]
    set ylabel  "total operations (MFLOPs)"
    set yrange  [0:max_tot_ops/scale]
    set y2label "task ttc (s)"
    set y2tics  auto
    set y2range [0:max_ttc]

    plot "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($3/scale) with linespoints ls 401 title 'ops'   ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($4/scale) with linespoints ls 403 title 'flops' ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($2      ) with linespoints ls 100 title 'ttc' axes x1y2


    scale=100
    set output "./rs_".experiment.".cpu.tot.eff.".modes.".png"
    set title   "Total CPU Utilization vs Task TTC"
    set xlabel  "tasks (sorted by ttc)"
    set xrange  [0:max_tasks+1]
    set ylabel  "cpu utilization / efficiency (%)"
    set yrange  [0:100]
    set y2label "task ttc (s)"
    set y2tics  auto
    set y2range [0:max_ttc]

    plot "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($5*scale) with linespoints ls 401 title 'efficiency'  ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($6*scale) with linespoints ls 403 title 'utilization' ,\
         "/tmp/rs_".experiment.".cpu.tot.dat" using 1:($2      ) with linespoints ls 100 title 'ttc' axes x1y2


    # -------------------------------------------------------------------------------------------

    scale=1024*1024

    set output "./rs_".experiment.".cpu.inc.ops.".modes.".png"
    set title   "CPU Usage over Task TTC"
    set xlabel  "task ttc (s)"
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

    set output "./rs_".experiment.".cpu.acc.ops.".modes.".png"
    set title   "Accumulated CPU Usage over Task TTC"
    set xlabel  "task ttc (s)"
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

    set title   "Total I/O vs Task TTC"
    set xlabel  "task (sorted by ttc)"
    set xrange  [0:max_tasks+1]
    set ylabel  "accumulated read / write (kByte)"
    set yrange  [0:(max_tot_io/scale)]
    set y2label "task ttc (s)"
    set y2tics  auto
    set y2range [0:max_ttc]

    set output "./rs_".experiment.".io.tot.".modes.".png"
    plot "/tmp/rs_".experiment.".io.tot.dat" using 1:($3/scale) with linespoints ls 201 title 'read'  ,\
         "/tmp/rs_".experiment.".io.tot.dat" using 1:($4/scale) with linespoints ls 202 title 'write' ,\
         "/tmp/rs_".experiment.".io.tot.dat" using 1:($2      ) with linespoints ls 100 title 'ttc' axes x1y2

    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "I/O over Task TTC"
    set xlabel  "task ttc (s)"
    set xrange  [0:max_time]
    set ylabel  "read / write (kByte)"
    set yrange  [0:(max_inc_io/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".io.inc.".modes.".png"
    plot "/tmp/rs_".experiment.".io.inc.dat" using 2:($3/scale) with linespoints ls 211 title 'read'  ,\
         "/tmp/rs_".experiment.".io.inc.dat" using 2:($4/scale) with linespoints ls 212 title 'write' 


    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Accumulated I/O over Task TTC"
    set xlabel  "task ttc (s)"
    set xrange  [0:max_time]
    set ylabel  "accumulated read / write (kByte)"
    set yrange  [0:(max_tot_io/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".io.acc.".modes.".png"
    plot "/tmp/rs_".experiment.".io.acc.dat" using 2:($3/scale) with linespoints ls 211 title 'read'  ,\
         "/tmp/rs_".experiment.".io.acc.dat" using 2:($4/scale) with linespoints ls 212 title 'write' 


    # -------------------------------------------------------------------------------------------
    # MEM
    # -------------------------------------------------------------------------------------------

    scale=1024*1024

    set term    term_t enhanced color dashed
    set output "./rs_".experiment.".mem.tot.".modes.".png"

    print max_time

    set title   "Total Memory Usage vs Task TTC"
    set xlabel  "task (sorted by ttc)"
    set xrange  [0:max_tasks+1]
    set ylabel  "total memory (MByte)"
    set yrange  [0:max_tot_mem/scale]
    set y2label "task ttc (s)"
    set y2tics  auto
    set y2range [0:max_ttc]

    plot "/tmp/rs_".experiment.".mem.tot.dat" using 1:($3/scale) with linespoints ls 301 title 'rss'  ,\
         "/tmp/rs_".experiment.".mem.tot.dat" using 1:($2      ) with linespoints ls 100 title 'ttc' axes x1y2
                                         
       # "/tmp/rs_".experiment.".mem.tot.dat" using 1:($4/scale) with linespoints ls 303 title 'peak' ,\
       # "/tmp/rs_".experiment.".mem.tot.dat" using 1:($4/scale) with linespoints ls 302 title 'size' ,\

    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Memory Usage over Task TTC"
    set xlabel  "task ttc (s)"
    set xrange  [0:max_time]
    set ylabel  "accumulated memory (kByte)"
    set yrange  [0:(max_inc_mem/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".mem.inc.".modes.".png"
  # plot "/tmp/rs_".experiment.".mem.inc.dat" using 2:($4/scale) with linespoints ls 313 title 'size' ,\

    plot "/tmp/rs_".experiment.".mem.inc.dat" using 2:($3/scale) with linespoints ls 311 title 'rss'



    # -------------------------------------------------------------------------------------------

    scale=1024

    set title   "Accumulated Memory Usage over Task TTC"
    set xlabel  "task ttc (s)"
    set xrange  [0:max_time]
    set ylabel  "accumulated memory (kByte)"
    set yrange  [0:(max_tot_mem/scale)]

  unset y2label 
  unset y2tics  
  unset y2range 

    set output "./rs_".experiment.".mem.acc.".modes.".png"
  # plot "/tmp/rs_".experiment.".mem.acc.dat" using 2:($4/scale) with linespoints ls 313 title 'size' ,\ 

    plot "/tmp/rs_".experiment.".mem.acc.dat" using 2:($3/scale) with linespoints ls 311 title 'rss'


    # -------------------------------------------------------------------------------------------

    exit

