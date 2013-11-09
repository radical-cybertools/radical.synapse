
# --------------------------------------------------------------------------------------------------
#
# base parameters
#
set key       Left left
set pointsize  0.8
#set ytic      0,5

# exp = "boskop"
# exp = "india"
  exp = "sierra"

dat = "../experiments/".exp.".dat"
mod = "../experiments/".exp.".mod"

# --------------------------------------------------------------------------------------------------
#
# Weak Scaling: Compute, Memory, Storage
#

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/weak_scaling_compute_'.exp.'.pdf'
set title     'weak scaling compute '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e 'WS.C\... '  ".mod.")" using ($7+0.2):3 title 'Model total'   with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e 'WS.C\...\.' ".mod.")" using ($7-0.2):4 title 'Model compute' with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e 'WS.C\...\.' ".mod.")" using ($7-0.2):5 title 'Model memory'  with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e 'WS.C\...\.' ".mod.")" using ($7-0.2):6 title 'Model storage' with points      lc rgb '#777733' pt 7, \
    "<(grep -e 'WS.C\... '  ".dat.")" using ($7-0.2):3 title 'Exp.  total'   with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e 'WS.C\...\.' ".dat.")" using ($7-0.2):4 title 'Exp.  compute' with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e 'WS.C\...\.' ".dat.")" using ($7-0.2):5 title 'Exp.  memory'  with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e 'WS.C\...\.' ".dat.")" using ($7-0.2):6 title 'Exp.  storage' with points      lc rgb '#994499' pt 7 
set output exp.'/weak_scaling_compute_'.exp.'.png'
set term   pngcairo size 800,600 enhanced color font "Arial,12"
replot
print "WS.C"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/weak_scaling_memory_'.exp.'.pdf'
set title     'weak scaling memory '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e 'WS.M\... '  ".mod.")" using ($7+0.2):3 title 'Model total'   with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e 'WS.M\...\.' ".mod.")" using ($7-0.2):4 title 'Model compute' with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e 'WS.M\...\.' ".mod.")" using ($7-0.2):5 title 'Model memory'  with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e 'WS.M\...\.' ".mod.")" using ($7-0.2):6 title 'Model storage' with points      lc rgb '#777733' pt 7, \
    "<(grep -e 'WS.M\... '  ".dat.")" using ($7-0.2):3 title 'Exp.  total'   with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e 'WS.M\...\.' ".dat.")" using ($7-0.2):4 title 'Exp.  compute' with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e 'WS.M\...\.' ".dat.")" using ($7-0.2):5 title 'Exp.  memory'  with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e 'WS.M\...\.' ".dat.")" using ($7-0.2):6 title 'Exp.  storage' with points      lc rgb '#994499' pt 7 
set output exp.'/weak_scaling_memory_'.exp.'.png'
set term   pngcairo size 800,600 enhanced color font "Arial,12"
replot
print "WS.M"


set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/weak_scaling_storage_'.exp.'.pdf'
set title     'weak scaling storage '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot  \
    "<(grep -e 'WS.S\... '  ".mod.")" using ($7+0.2):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e 'WS.S\...\.' ".mod.")" using ($7-0.2):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e 'WS.S\...\.' ".mod.")" using ($7-0.2):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e 'WS.S\...\.' ".mod.")" using ($7-0.2):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e 'WS.S\... '  ".dat.")" using ($7-0.2):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e 'WS.S\...\.' ".dat.")" using ($7-0.2):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e 'WS.S\...\.' ".dat.")" using ($7-0.2):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e 'WS.S\...\.' ".dat.")" using ($7-0.2):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set output exp.'/weak_scaling_storage_'.exp.'.png'
set term   pngcairo size 800,600 enhanced color font "Arial,12"
replot
print "WS.S"


# --------------------------------------------------------------------------------------------------
#
# Scaling Compute load + background
#
set pointsize  1.0
set xtic       1,1

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_1_'.exp.'.pdf'
set title     'scaling compute 1 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C1\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 2, \
    "<(grep -e ' C1\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C1\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C1\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C1\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 2, \
    "<(grep -e ' C1\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C1\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C1\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_1_'.exp.'.png'
replot
print "C1"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_2_'.exp.'.pdf'
set title     'scaling compute 2 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C2\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C2\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C2\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C2\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C2\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C2\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C2\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C2\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_2_'.exp.'.png'
replot
print "C2"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_3_'.exp.'.pdf'
set title     'scaling compute 3 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C3\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C3\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C3\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C3\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C3\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C3\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C3\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C3\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_3_'.exp.'.png'
replot
print "C3"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_4_'.exp.'.pdf'
set title     'scaling compute 4 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C4\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C4\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C4\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C4\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C4\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C4\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C4\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C4\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_4_'.exp.'.png'
replot
print "C4"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_5_'.exp.'.pdf'
set title     'scaling compute 5 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C5\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C5\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C5\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C5\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C5\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C5\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C5\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C5\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_5_'.exp.'.png'
replot
print "C5"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_6_'.exp.'.pdf'
set title     'scaling compute 6 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C6\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C6\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C6\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C6\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C6\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C6\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C6\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C6\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_6_'.exp.'.png'
replot
print "C6"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_7_'.exp.'.pdf'
set title     'scaling compute 7 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C7\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C7\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C7\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C7\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C7\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C7\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C7\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C7\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_7_'.exp.'.png'
replot
print "C7"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_compute_8_'.exp.'.pdf'
set title     'scaling compute 8 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' C8\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' C8\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' C8\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' C8\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' C8\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' C8\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' C8\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' C8\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_compute_8_'.exp.'.png'
replot
print "C8"


# ----------------------------------------------------------------------   ----------------------------
#
# Scaling Memory load + background
#
set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_1_'.exp.'.pdf'
set title     'scaling memory 1 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M1\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M1\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M1\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M1\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M1\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M1\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M1\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M1\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_1_'.exp.'.png'
replot
print "M1"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_2_'.exp.'.pdf'
set title     'scaling memory 2 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M2\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M2\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M2\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M2\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M2\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M2\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M2\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M2\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_2_'.exp.'.png'
replot
print "M2"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_3_'.exp.'.pdf'
set title     'scaling memory 3 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M3\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M3\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M3\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M3\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M3\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M3\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M3\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M3\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_3_'.exp.'.png'
replot
print "M3"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_4_'.exp.'.pdf'
set title     'scaling memory 4 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M4\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M4\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M4\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M4\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M4\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M4\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M4\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M4\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_4_'.exp.'.png'
replot
print "M4"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_5_'.exp.'.pdf'
set title     'scaling memory 5 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M5\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M5\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M5\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M5\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M5\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M5\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M5\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M5\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_5_'.exp.'.png'
replot
print "M5"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_6_'.exp.'.pdf'
set title     'scaling memory 6 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M6\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M6\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M6\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M6\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M6\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M6\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M6\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M6\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_6_'.exp.'.png'
replot
print "M6"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_7_'.exp.'.pdf'
set title     'scaling memory 7 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M7\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M7\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M7\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M7\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M7\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M7\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M7\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M7\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_7_'.exp.'.png'
replot
print "M7"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_memory_8_'.exp.'.pdf'
set title     'scaling memory 8 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' M8\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' M8\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' M8\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' M8\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' M8\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' M8\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' M8\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' M8\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_memory_8_'.exp.'.png'
replot
print "M8"


# ----------------------------------------------------------------------   ----------------------------
#
# Scaling Compute load + background
#
set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_1_'.exp.'.pdf'
set title     'scaling storage 1 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S1\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S1\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S1\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S1\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S1\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S1\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S1\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S1\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_1_'.exp.'.png'
replot
print "S1"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_2_'.exp.'.pdf'
set title     'scaling storage 2 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S2\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S2\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S2\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S2\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S2\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S2\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S2\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S2\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_2_'.exp.'.png'
replot
print "S2"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_3_'.exp.'.pdf'
set title     'scaling storage 3 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S3\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S3\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S3\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S3\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S3\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S3\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S3\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S3\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_3_'.exp.'.png'
replot
print "S3"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_4_'.exp.'.pdf'
set title     'scaling storage 4 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S4\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S4\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S4\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S4\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S4\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S4\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S4\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S4\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_4_'.exp.'.png'
replot
print "S4"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_5_'.exp.'.pdf'
set title     'scaling storage 5 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S5\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S5\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S5\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S5\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S5\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S5\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S5\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S5\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_5_'.exp.'.png'
replot
print "S5"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_6_'.exp.'.pdf'
set title     'scaling storage 6 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S6\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S6\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S6\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S6\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S6\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S6\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S6\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S6\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_6_'.exp.'.png'
replot
print "S6"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_7_'.exp.'.pdf'
set title     'scaling storage 7 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S7\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S7\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S7\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S7\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S7\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S7\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S7\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S7\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_7_'.exp.'.png'
replot
print "S7"

set term pdfcairo enhanced color font "Arial,12"
set output    exp.'/scaling_storage_8_'.exp.'.pdf'
set title     'scaling storage 8 '.exp
set xlabel    'number of applications' font "Times-Italic, 20"
set ylabel    'time to completion (s)' font "Times-Italic, 20"
plot \
    "<(grep -e ' S8\... '  ".mod.")" using ($7+0.1):3 title 'Model total'    with linespoints lc rgb '#33DD55' pt 7 lw 3, \
    "<(grep -e ' S8\...\.' ".mod.")" using ($7+0.1):4 title 'Model compute'  with points      lc rgb '#00BB77' pt 7, \
    "<(grep -e ' S8\...\.' ".mod.")" using ($7+0.1):5 title 'Model memory'   with points      lc rgb '#0077BB' pt 7, \
    "<(grep -e ' S8\...\.' ".mod.")" using ($7+0.1):6 title 'Model storage'  with points      lc rgb '#777733' pt 7, \
    "<(grep -e ' S8\... '  ".dat.")" using ($7-0.1):3 title 'Exp.  total'    with linespoints lc rgb '#FF9944' pt 7 lw 3, \
    "<(grep -e ' S8\...\.' ".dat.")" using ($7-0.1):4 title 'Exp.  compute'  with points      lc rgb '#DD5500' pt 7, \
    "<(grep -e ' S8\...\.' ".dat.")" using ($7-0.1):5 title 'Exp.  memory'   with points      lc rgb '#BB0055' pt 7, \
    "<(grep -e ' S8\...\.' ".dat.")" using ($7-0.1):6 title 'Exp.  storage'  with points      lc rgb '#994499' pt 7 
set term pngcairo size 800,600 enhanced color font "Arial,12"
set output    exp.'/scaling_storage_8_'.exp.'.png'
replot
print "S8"

# ----------------------------------------------------------------------   --------
# vim: ft=gnuplot

