
basename = 'over_problem_size'

name  = 'hosts_'.basename

boskop_dat   = '../experiments/'.'boskop_'.basename.'.dat'
cameo_dat    = '../experiments/'.'cameo_'.basename.'.dat'
india_dat    = '../experiments/'.'india_'.basename.'.dat'
sierra_dat   = '../experiments/'.'sierra_'.basename.'.dat'
stampede_dat = '../experiments/'.'stampede_'.basename.'.dat'

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
    
    set style line 1 lt 2 lc rgb '#FF9944' pt 0 ps term_mult*0.3 lw term_mult*4
    set style line 2 lt 2 lc rgb '#AA6666' pt 7 ps term_mult*0.3 lw term_mult*1
    set style line 3 lt 2 lc rgb '#66AA66' pt 7 ps term_mult*0.3 lw term_mult*1
    set style line 4 lt 2 lc rgb '#6666AA' pt 7 ps term_mult*0.3 lw term_mult*1
    set style line 5 lt 1 lc rgb '#FF4400' pt 0 ps term_mult*0.3 lw term_mult*4
    set style line 6 lt 1 lc rgb '#AA6666' pt 7 ps term_mult*0.3 lw term_mult*1
    set style line 7 lt 1 lc rgb '#66AA66' pt 7 ps term_mult*0.3 lw term_mult*1
    set style line 8 lt 1 lc rgb '#6666AA' pt 7 ps term_mult*0.3 lw term_mult*1
    
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

  # set title     'synapse execution vs. emulation vs. simulation'
    set logscale xy

    set tmargin 0
    set bmargin 0
    set lmargin 15
    set rmargin 13
  unset format

  # set size 1.0,1.5
    set multiplot layout 6,1 title ""

    set key at screen 0.158,screen 0.11

    set xtics  in
    set ytics  in 0.1,10,1000
    set xlabel ''
    set format x ""

    set ylabel "TTC [sec]\nboskop" offset second -0.06,0
    plot [5:10000][0.05:5000] \
        '<(grep -e "boskop.*STAT_RUN" '.boskop_dat.')' using 3:7       title ''                      with lines       ls 6, \
        '<(grep -e "boskop.*STAT_RUN" '.boskop_dat.')' using 3:7:8     title 'Execution'             with yerrorbars  ls 6, \
        '<(grep -e "boskop.*STAT_EMU" '.boskop_dat.')' using 3:7       title ''                      with lines       ls 8, \
        '<(grep -e "boskop.*STAT_EMU" '.boskop_dat.')' using 3:7:8     title 'Emulation'             with yerrorbars  ls 8

    set ylabel "TTC [sec]\ncameo" offset second -0.06,0
    plot [5:10000][0.05:5000] \
        '<(grep -e "cameo.*STAT_RUN" '.cameo_dat.')'   using 3:7       title ''                      with lines       ls 6, \
        '<(grep -e "cameo.*STAT_RUN" '.cameo_dat.')'   using 3:7:8     title ''                      with yerrorbars  ls 6, \
        '<(grep -e "cameo.*STAT_EMU" '.cameo_dat.')'   using 3:7       title ''                      with lines       ls 8, \
        '<(grep -e "cameo.*STAT_EMU" '.cameo_dat.')'   using 3:7:8     title ''                      with yerrorbars  ls 8

    set ylabel "TTC [sec]\nindia" offset second -0.06,0
    plot [5:10000][0.05:5000] \
        '<(grep -e "india.*STAT_RUN" '.india_dat.')'   using 3:7       title ''                      with lines       ls 6, \
        '<(grep -e "india.*STAT_RUN" '.india_dat.')'   using 3:7:8     title ''                      with yerrorbars  ls 6, \
        '<(grep -e "india.*STAT_EMU" '.india_dat.')'   using 3:7       title ''                      with lines       ls 8, \
        '<(grep -e "india.*STAT_EMU" '.india_dat.')'   using 3:7:8     title ''                      with yerrorbars  ls 8
 
    set ylabel "TTC [sec]\nsierra" offset second -0.06,0
    plot [5:10000][0.05:5000] \
        '<(grep -e "sierra.*STAT_RUN" '.sierra_dat.')' using 3:7       title ''                      with lines       ls 6, \
        '<(grep -e "sierra.*STAT_RUN" '.sierra_dat.')' using 3:7:8     title ''                      with yerrorbars  ls 6, \
        '<(grep -e "sierra.*STAT_EMU" '.sierra_dat.')' using 3:7       title ''                      with lines       ls 8, \
        '<(grep -e "sierra.*STAT_EMU" '.sierra_dat.')' using 3:7:8     title ''                      with yerrorbars  ls 8
 
    set xtics  in
    set xlabel 'Problem Size' offset 27,0
    set format x "%.0f"
    set ylabel "TTC [sec]\nstampede" offset second -0.06,0

    plot [5:10000][0.05:5000] \
        '<(grep -e "c401.*STAT_RUN" '.stampede_dat.')' using 3:7       title ''                      with lines       ls 6, \
        '<(grep -e "c401.*STAT_RUN" '.stampede_dat.')' using 3:7:8     title ''                      with yerrorbars  ls 6, \
        '<(grep -e "c401.*STAT_EMU" '.stampede_dat.')' using 3:7       title ''                      with lines       ls 8, \
        '<(grep -e "c401.*STAT_EMU" '.stampede_dat.')' using 3:7:8     title ''                      with yerrorbars  ls 8
 
    unset multiplot

  # set nologscale xy
}



# ------------------------------------------------------------------------------
# vim: ft=gnuplot

