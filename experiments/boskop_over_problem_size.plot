

name = 'boskop_over_problem_size'
dat  = '../experiments/'.name.'.dat'

hosts = 'boskop'
do for [host_i=1:words(hosts)] {
    h = word(hosts, host_i)

    terms = 'png pdf'
    do for [term_i=1:words(terms)] {
        t = word(terms, term_i)
        term_t = t.'cairo'

        # --------------------------------------------------------------------------------------------------
        #
        # base parameters
        #
        set key Left left

        if (t eq 'pdf') {
            term_mult  = 6.0
            term_x     = 50
            term_y     = 50
            term_font  = 'Monospace,8'
            term_dl    = 7
            term_lw    = 3

            set key    font ",8"
            set xlabel font ",8"
            set ylabel font ",8"
            set title  font ",8"

        } else {
            term_mult  = 8.0
            term_x     = '6000'
            term_y     = '4000'
            term_font  = 'Monospace,8'
            term_dl    = 6
            term_lw    = 1

            set key    font ",8"
            set xlabel font ",8"
            set ylabel font ",8"
            set title  font ",8"
        }
        
        set style line 1 lt 2 lc rgb '#FF9944' pt 0 ps term_mult*0.5 lw term_mult*4
        set style line 2 lt 2 lc rgb '#AA6666' pt 7 ps term_mult*0.5 lw term_mult*1
        set style line 3 lt 2 lc rgb '#66AA66' pt 7 ps term_mult*0.5 lw term_mult*1
        set style line 4 lt 2 lc rgb '#6666AA' pt 7 ps term_mult*0.5 lw term_mult*1
        set style line 5 lt 1 lc rgb '#FF4400' pt 0 ps term_mult*0.5 lw term_mult*4
        set style line 6 lt 1 lc rgb '#AA6666' pt 5 ps term_mult*0.5 lw term_mult*1
        set style line 7 lt 1 lc rgb '#66AA66' pt 5 ps term_mult*0.5 lw term_mult*1
        set style line 8 lt 1 lc rgb '#6666AA' pt 5 ps term_mult*0.5 lw term_mult*1
        
        set border lw 4.0
      # set mxtics 10
      # set mytics 10
        set tics   scale 1.5

        set term   term_t enhanced color size term_x,term_y font term_font fontscale term_mult dashed dashlength term_dl linewidth term_lw
          
        # --------------------------------------------------------------------------------------------------
        # 
        # The ditect mandelbrot profiling and emulation comparison only exists for boskop_2
        #
        set output './'.name.'.'.t 
        print      './'.name.'.'.t

      # set title     'synapse profiling vs. emulation ['.h.']'
        set logscale xy

        set tmargin 0
        set bmargin 0
        set lmargin 15
        set rmargin 13
      unset format

      # set size 1.0,1.5
        set multiplot layout 9,1 title ""

        set key at screen 0.158,screen 0.14

        set xtics  out
        set ytics  out 1,10,1000
        set xlabel ''
        set ylabel "TTC\n[sec]" offset second -0.06,0
        set format x ""

        plot [5:10000][0.5:5000] \
            '<(grep -e "STAT_EXE" '.dat.')' using 3:7       title ''                      with lines       ls 6, \
            '<(grep -e "STAT_EXE" '.dat.')' using 3:7:8     title 'Execution'             with yerrorbars  ls 6, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:7       title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:7:8     title 'Profiling'             with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:7       title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:7:8     title 'Emulation'             with yerrorbars  ls 8

        set xtics  out
        set ytics  out 0.1,10,10
        set xlabel ''
        set ylabel "Load\n[%]" offset second -0.17,0
        set format x ""
     
        plot [5:10000][0.05:50] \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:21      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:21:22   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:21      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:21:22   title ''                      with yerrorbars  ls 8
     
        set xtics  out
        set ytics  out 10,100,1000000
        set xlabel ''
        set ylabel "CPU\n# MFLOPs" offset second -0.02,0
        set format x ""
     
        plot [5:10000][5:500000] \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:15      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:15:16   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:15      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:15:16   title ''                      with yerrorbars  ls 8
     
        set xtics  out
        set ytics  out 0.1,10,1
        set xlabel ''
        set ylabel "CPU Eff.\n[%]" offset second -0.16,0
        set format x ""

        plot [5:10000][0.05:5] \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:19      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:19:20   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:19      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:19:20   title ''                      with yerrorbars  ls 8


        set xtics  out
        set ytics  out 0.01,10,1
        set xlabel ''
        set ylabel "CPU Util.\n[%]" offset second -0.1,0
        set format x ""

        plot [5:10000][0.005:5] \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:17      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:17:18   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:17      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:17:18   title ''                      with yerrorbars  ls 8

        set xtics  out
        set ytics  out 100,10,10000
        set xlabel ''
        set ylabel "Memory\n# MB" offset second -0.07,0
        set format x ""
     
        plot [5:10000][50:50000] \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:23      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:23:24   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:23      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:23:24   title ''                      with yerrorbars  ls 8
     
        set xtics  out
        set ytics  out 0.01,100,10000
        set xlabel 'Problem Size' offset 27,0
        set ylabel "Storage\n# MB" offset second -0.07,0
        set format x "%.0f"
     
        plot [5:10000][0.005:50000] \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:25      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 3:25:26   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:25      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 3:25:26   title ''                      with yerrorbars  ls 8
     
        unset multiplot

      # set nologscale xy
    }
}


# ------------------------------------------------------------------------------
# vim: ft=gnuplot

