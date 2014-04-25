
name = 'boskop_over_stress'
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
        # The ditect mandelbrot profiling and emulation comparison only exists for boskop_3
        #
        set output './'.name.'.'.t 
        print      './'.name.'.'.t

      # set title     'synapse profiling vs. emulation ['.h.']'
      # set logscale y

        set tmargin 0
        set bmargin 0
        set lmargin 15
        set rmargin 13
      unset format

      # set size 1.0,1.5
        set multiplot layout 9,1 title ""

        set key at screen 0.158,screen 0.14

        set xtics  out 0,1,12
        set ytics  out 100,200,500
        set xlabel ''
        set ylabel "TTC\n[sec]" offset second -0.4,0
        set format x ""

        plot [-1:13][20:630] \
            '<(grep -e "STAT_RUN" '.dat.')' using 6:7       title ''                      with lines       ls 6, \
            '<(grep -e "STAT_RUN" '.dat.')' using 6:7:8     title 'Execution'             with yerrorbars  ls 6, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:7       title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:7:8     title 'Profiling'             with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:7       title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:7:8     title 'Emulation'             with yerrorbars  ls 8

        set xtics  out 0,1,12
        set ytics  out 0,5,15
        set xlabel ''
        set ylabel "Load\n[%]" offset second -0.95,0
        set format x ""
     
        plot [-1:13][-2:17] \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:21      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:21:22   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:21      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:21:22   title ''                      with yerrorbars  ls 8
     
        set xtics  out 0,1,12
        set ytics  out 90000,5000,100000
        set xlabel ''
        set ylabel "CPU\n# MFLOPs" offset second -0.1,0
        set format x ""
     
        plot [-1:13][85000:105000] \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:15      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:15:16   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:15      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:15:16   title ''                      with yerrorbars  ls 8
     
        set xtics  out 0,1,12
        set ytics  out 0,0.5,1
        set xlabel ''
        set ylabel "CPU Eff.\n[%]" offset second -0.75,0
        set format x ""

        plot [-1:13][-0.2:1.2] \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:19      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:19:20   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:19      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:19:20   title ''                      with yerrorbars  ls 8


        set xtics  out 0,1,12
        set ytics  out 0,0.5,1
        set xlabel ''
        set ylabel "CPU Util.\n[%]" offset second -0.75,0
        set format x ""

        plot [-1:13][-0.2:1.2] \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:17      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:17:18   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:17      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:17:18   title ''                      with yerrorbars  ls 8

        set xtics  out 0,1,12
        set ytics  out 1500,500,2500
        set xlabel ''
        set ylabel "Memory\n# MB" offset second -0.5,0
        set format x ""
     
        plot [-1:13][1200:2800] \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:23      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:23:24   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:23      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:23:24   title ''                      with yerrorbars  ls 8
     
        set xtics  out 0,1,12
        set ytics  out 1000,500,2000
        set xlabel 'System Stress' offset 27,0
        set ylabel "Storage\n# MB" offset second -0.5,0
        set format x "%.0f"
     
        plot [-1:13][700:2300] \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:25      title ''                      with lines       ls 7, \
            '<(grep -e "STAT_PRO" '.dat.')' using 6:25:26   title ''                      with yerrorbars  ls 7, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:25      title ''                      with lines       ls 8, \
            '<(grep -e "STAT_EMU" '.dat.')' using 6:25:26   title ''                      with yerrorbars  ls 8
     
        unset multiplot

      # set nologscale xy
    }
}


# ------------------------------------------------------------------------------
# vim: ft=gnuplot

