
set term pdfcairo enhanced color font "Arial,12"

set output 'weak_scaling_compute.pdf'
set pointsize 0.2
set key       Left left
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
set xtic      0,6
set ytic      0,20
set mxtics    1
set mytics    4
set style function dots
set parametric
plot[1:1024][0:70] \
    "<(grep -e WS.C total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    './WS.C.partial.dat'        using 7:4 title 'Compute'  with points      pt 6, \
    './WS.C.partial.dat'        using 7:5 title 'Memory'   with points      pt 6, \
    './WS.C.partial.dat'        using 7:6 title 'Storage'  with points      pt 6 

set output 'weak_scaling_memory.pdf'
set pointsize 0.2
set key       Left left
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
set xtic      0,6
set ytic      0,20
set mxtics    1
set mytics    4
set style function dots
set parametric
plot[1:1024][0:70] \
    "<(grep -e WS.M total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    './WS.M.partial.dat'        using 7:4 title 'Compute'  with points      pt 6, \
    './WS.M.partial.dat'        using 7:5 title 'Memory'   with points      pt 6, \
    './WS.M.partial.dat'        using 7:6 title 'Storage'  with points      pt 6 


set term pdfcairo enhanced color font "Arial,12"
set output 'weak_scaling_storage.pdf'
set pointsize 0.2
set key       Left left
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
set xtic      0,6
set ytic      0,20
set mxtics    1
set mytics    4
set style function dots
set parametric
plot[1:1024][0:70] \
    "<(grep -e WS.S total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    './WS.S.partial.dat'        using 7:4 title 'Compute'  with points      pt 6, \
    './WS.S.partial.dat'        using 7:5 title 'Memory'   with points      pt 6, \
    './WS.S.partial.dat'        using 7:6 title 'Storage'  with points      pt 6 

