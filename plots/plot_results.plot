
# --------------------------------------------------------------------------------------------------
#
# base parameters
#
set key       Left left
set pointsize 0.2
#set ytic      0,5

# --------------------------------------------------------------------------------------------------
#
# Weak Scaling: Compute, Memory, Storage
#
#set xtic      1,5

set term pdfcairo enhanced color font "Arial,12"
set output    'weak_scaling_compute.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:64][0:200] \
    "<(grep -e WS.C total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    './WS.C.partial.dat'        using 7:4 title 'Compute'  with points      pt 6, \
    './WS.C.partial.dat'        using 7:5 title 'Memory'   with points      pt 6, \
    './WS.C.partial.dat'        using 7:6 title 'Storage'  with points      pt 6 
set output 'weak_scaling_compute.png'
set term   pngcairo enhanced color font "Arial,12"
replot
print "WS.C"

set term pdfcairo enhanced color font "Arial,12"
set output    'weak_scaling_memory.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:64][0:20] \
    "<(grep -e WS.M total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    './WS.M.partial.dat'        using 7:4 title 'Compute'  with points      pt 6, \
    './WS.M.partial.dat'        using 7:5 title 'Memory'   with points      pt 6, \
    './WS.M.partial.dat'        using 7:6 title 'Storage'  with points      pt 6 
set output 'weak_scaling_memory.png'
set term   pngcairo enhanced color font "Arial,12"
replot
print "WS.M"


set term pdfcairo enhanced color font "Arial,12"
set output    'weak_scaling_storage.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot [1:64][0:500] \
    "<(grep -e WS.S total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    './WS.S.partial.dat'        using 7:4 title 'Compute'  with points      pt 6, \
    './WS.S.partial.dat'        using 7:5 title 'Memory'   with points      pt 6, \
    './WS.S.partial.dat'        using 7:6 title 'Storage'  with points      pt 6 
set output 'weak_scaling_storage.png'
set term   pngcairo enhanced color font "Arial,12"
replot
print "WS.S"


# --------------------------------------------------------------------------------------------------
#
# Scaling Compute load + background
#
set xtic      1,1

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_1.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C1\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C1\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C1\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C1\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_1.pdf'
replot
print "C1"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_2.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C2\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C2\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C2\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C2\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_2.pdf'
replot
print "C2"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_3.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C3\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C3\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C3\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C3\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_3.pdf'
replot
print "C3"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_4.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C4\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C4\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C4\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C4\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_4.pdf'
replot
print "C4"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_5.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C5\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C5\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C5\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C5\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_5.pdf'
replot
print "C5"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_6.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C6\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C6\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C6\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C6\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_6.pdf'
replot
print "C6"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_7.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C7\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C7\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C7\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C7\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_7.pdf'
replot
print "C7"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_compute_8.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:40] \
    "<(grep -e ' C8\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' C8\...' C.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' C8\...' C.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' C8\...' C.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_compute_8.pdf'
replot
print "C8"


# --------------------------------------------------------------------------------------------------
#
# Scaling Memory load + background
#
set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_1.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M1\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M1\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M1\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M1\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_1.pdf'
replot
print "M1"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_2.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M2\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M2\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M2\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M2\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_2.pdf'
replot
print "M2"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_3.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M3\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M3\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M3\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M3\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_3.pdf'
replot
print "M3"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_4.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M4\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M4\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M4\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M4\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_4.pdf'
replot
print "M4"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_5.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M5\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M5\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M5\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M5\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_5.pdf'
replot
print "M5"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_6.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M6\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M6\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M6\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M6\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_6.pdf'
replot
print "M6"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_7.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M7\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M7\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M7\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M7\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_7.pdf'
replot
print "M7"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_memory_8.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:25] \
    "<(grep -e ' M8\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' M8\...' M.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' M8\...' M.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' M8\...' M.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_memory_8.pdf'
replot
print "M8"


# --------------------------------------------------------------------------------------------------
#
# Scaling Compute load + background
#
set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_1.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S1\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S1\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S1\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S1\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_1.pdf'
replot
print "S1"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_2.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S2\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S2\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S2\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S2\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_2.pdf'
replot
print "S2"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_3.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S3\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S3\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S3\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S3\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_3.pdf'
replot
print "S3"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_4.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S4\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S4\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S4\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S4\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_4.pdf'
replot
print "S4"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_5.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S5\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S5\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S5\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S5\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_5.pdf'
replot
print "S5"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_6.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S6\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S6\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S6\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S6\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_6.pdf'
replot
print "S6"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_7.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S7\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S7\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S7\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S7\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_7.pdf'
replot
print "S7"

set term pdfcairo enhanced color font "Arial,12"
set output    'scaling_storage_8.pdf'
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot[1:8][0:500] \
    "<(grep -e ' S8\...'     total.dat)" using 7:3 title 'Total'    with linespoints pt 6 lw 3, \
    "<(grep -e ' S8\...' S.partial.dat)" using 7:4 title 'Compute'  with points      pt 6, \
    "<(grep -e ' S8\...' S.partial.dat)" using 7:5 title 'Memory'   with points      pt 6, \
    "<(grep -e ' S8\...' S.partial.dat)" using 7:6 title 'Storage'  with points      pt 6 
set term pngcairo enhanced color font "Arial,12"
set output    'scaling_storage_8.pdf'
replot
print "S8"

# ------------------------------------------------------------------------------
# vim: ft=gnuplot

