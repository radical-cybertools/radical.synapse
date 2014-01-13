
hosts = 'boskop india sierra'
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
            term_x     = '50cm'
            term_y     = '35cm'
            term_font  = 'Arial,10'
            term_dl    = 7
            term_lw    = 3

            set key    font ",10"
            set xlabel font ",14"
            set ylabel font ",14"
            set title  font ",14"

        } else {
            term_mult  = 8.0
            term_x     = '6000'
            term_y     = '4000'
            term_font  = 'Arial,10'
            term_dl    = 6
            term_lw    = 1

            set key    font ",10"
            set xlabel font ",14"
            set ylabel font ",14"
            set title  font ",14"
        }
        
        smd = '../experiments/mandelbrot_'.h.'.dat'
        dat = '../experiments/'.h.'.dat'
        mod = '../experiments/'.h.'.mod'
        
        set style line 1 lt 2 lc rgb '#FF9944' pt 0 ps term_mult*0.5 lw term_mult*4
        set style line 2 lt 2 lc rgb '#AA6666' pt 7 ps term_mult*0.5 lw term_mult*1
        set style line 3 lt 2 lc rgb '#66AA66' pt 7 ps term_mult*0.5 lw term_mult*1
        set style line 4 lt 2 lc rgb '#6666AA' pt 7 ps term_mult*0.5 lw term_mult*1
        set style line 5 lt 1 lc rgb '#FF4400' pt 0 ps term_mult*0.5 lw term_mult*4
        set style line 6 lt 1 lc rgb '#AA6666' pt 5 ps term_mult*0.5 lw term_mult*1
        set style line 7 lt 1 lc rgb '#66AA66' pt 5 ps term_mult*0.5 lw term_mult*1
        set style line 8 lt 1 lc rgb '#6666AA' pt 5 ps term_mult*0.5 lw term_mult*1
        
        set border lw 4.0
        set ytics  out 
        set xtics  out 0,10
        set mxtics 10
        set mytics 10
        set tics   scale 1.5

        set term   term_t enhanced color size term_x,term_y font term_font fontscale term_mult dashed dashlength term_dl linewidth term_lw
          
        if (h eq 'boskop') {
            # --------------------------------------------------------------------------------------------------
            # 
            # The mandelbrot/synapse scaling figure only exists for boskop
            #
            set output  h.'/synapse_mandelbrot_'.h.'.'.t

          # set title     'synapse vs. mandelbrot ['.h.']'
            set xlabel    'problem size'
            set ylabel    'time to completion (s)'
            set logscale xy

            print smd
            plot [10:10000][0.01:1000] \
                '<(grep -e "SMB" '.smd.')' using ($11+0.1):3               title 'Synapse total'      with lines       ls 5, \
                '<(grep -e "SMB" '.smd.')' using ($11+0.1):4 smooth unique title 'Synapse compute'    with linespoints ls 6, \
                '<(grep -e "SMB" '.smd.')' using ($11+0.1):5 smooth unique title 'Synapse memory'     with linespoints ls 7, \
                '<(grep -e "SMB" '.smd.')' using ($11+0.1):6 smooth unique title 'Synapse storage'    with linespoints ls 8, \
                '<(grep -e "RMB" '.smd.')' using ($11+0.1):3               title 'Mandelbrot total'   with lines       ls 1
            print 'S-M '.h.' '.t
            set nologscale xy
        }


        # --------------------------------------------------------------------------------------------------
        #
        # Weak Scaling: Compute, Memory, Storage
        #
        set output  h.'/weak_scaling_compute_'.h.'.'.t
 
      # set title     'weak scaling compute ['.h.']'
        set xlabel    'number of applications' font term_font
        set ylabel    'time to completion (s)' font term_font
        plot [0:65][] \
            '<(grep -e "WS.C\...  " '.dat.')' using ($7-0.2):3               title 'Exp.  total'   with lines       ls 5, \
            '<(grep -e "WS.C\...\." '.dat.')' using ($7-0.2):4 smooth unique title 'Exp.  compute' with linespoints ls 6, \
            '<(grep -e "WS.C\...\." '.dat.')' using ($7-0.2):5 smooth unique title 'Exp.  memory'  with linespoints ls 7, \
            '<(grep -e "WS.C\...\." '.dat.')' using ($7-0.2):6 smooth unique title 'Exp.  storage' with linespoints ls 8, \
            '<(grep -e "WS.C\...\." '.dat.')' using ($7-0.2):4               title ''              with      points ls 6, \
            '<(grep -e "WS.C\...\." '.dat.')' using ($7-0.2):5               title ''              with      points ls 7, \
            '<(grep -e "WS.C\...\." '.dat.')' using ($7-0.2):6               title ''              with      points ls 8, \
            '<(grep -e "WS.C\...  " '.mod.')' using ($7+0.2):3               title 'Model total'   with lines       ls 1, \
            '<(grep -e "WS.C\...\." '.mod.')' using ($7+0.2):4 smooth unique title 'Model compute' with linespoints ls 2, \
            '<(grep -e "WS.C\...\." '.mod.')' using ($7+0.2):5 smooth unique title 'Model memory'  with linespoints ls 3, \
            '<(grep -e "WS.C\...\." '.mod.')' using ($7+0.2):6 smooth unique title 'Model storage' with linespoints ls 4, \
            '<(grep -e "WS.C\...\." '.mod.')' using ($7+0.2):4               title ''              with      points ls 2, \
            '<(grep -e "WS.C\...\." '.mod.')' using ($7+0.2):5               title ''              with      points ls 3, \
            '<(grep -e "WS.C\...\." '.mod.')' using ($7+0.2):6               title ''              with      points ls 4
        print 'WS.C '.h.' '.t
        
        
        set output  h.'/weak_scaling_memory_'.h.'.'.t
      # set title      'weak scaling memory ['.h.']'
        set xlabel     'number of applications' font term_font
        set ylabel     'time to completion (s)' font term_font
        plot [0:65][] \
            '<(grep -e "WS.M\...  " '.dat.')' using ($7-0.2):3               title 'Exp.  total'   with lines       ls 5, \
            '<(grep -e "WS.M\...\." '.dat.')' using ($7-0.2):4 smooth unique title 'Exp.  compute' with linespoints ls 6, \
            '<(grep -e "WS.M\...\." '.dat.')' using ($7-0.2):5 smooth unique title 'Exp.  memory'  with linespoints ls 7, \
            '<(grep -e "WS.M\...\." '.dat.')' using ($7-0.2):6 smooth unique title 'Exp.  storage' with linespoints ls 8, \
            '<(grep -e "WS.M\...\." '.dat.')' using ($7-0.2):4               title ''              with      points ls 6, \
            '<(grep -e "WS.M\...\." '.dat.')' using ($7-0.2):5               title ''              with      points ls 7, \
            '<(grep -e "WS.M\...\." '.dat.')' using ($7-0.2):6               title ''              with      points ls 8, \
            '<(grep -e "WS.M\...  " '.mod.')' using ($7+0.2):3               title 'Model total'   with lines       ls 1, \
            '<(grep -e "WS.M\...\." '.mod.')' using ($7+0.2):4 smooth unique title 'Model compute' with linespoints ls 2, \
            '<(grep -e "WS.M\...\." '.mod.')' using ($7+0.2):5 smooth unique title 'Model memory'  with linespoints ls 3, \
            '<(grep -e "WS.M\...\." '.mod.')' using ($7+0.2):6 smooth unique title 'Model storage' with linespoints ls 4, \
            '<(grep -e "WS.M\...\." '.mod.')' using ($7+0.2):4               title ''              with      points ls 2, \
            '<(grep -e "WS.M\...\." '.mod.')' using ($7+0.2):5               title ''              with      points ls 3, \
            '<(grep -e "WS.M\...\." '.mod.')' using ($7+0.2):6               title ''              with      points ls 4
        print 'WS.M '.h.' '.t
 
 
        set output  h.'/weak_scaling_storage_'.h.'.'.t
      # set title      'weak scaling storage ['.h.']'
        set xlabel     'number of applications' font term_font
        set ylabel     'time to completion (s)' font term_font
        plot [0:65][] \
            '<(grep -e "WS.S\...  " '.dat.')' using ($7-0.2):3               title 'Exp.  total'   with lines       ls 5, \
            '<(grep -e "WS.S\...\." '.dat.')' using ($7-0.2):4 smooth unique title 'Exp.  compute' with linespoints ls 6, \
            '<(grep -e "WS.S\...\." '.dat.')' using ($7-0.2):5 smooth unique title 'Exp.  memory'  with linespoints ls 7, \
            '<(grep -e "WS.S\...\." '.dat.')' using ($7-0.2):6 smooth unique title 'Exp.  storage' with linespoints ls 8, \
            '<(grep -e "WS.S\...\." '.dat.')' using ($7-0.2):4               title ''              with      points ls 6, \
            '<(grep -e "WS.S\...\." '.dat.')' using ($7-0.2):5               title ''              with      points ls 7, \
            '<(grep -e "WS.S\...\." '.dat.')' using ($7-0.2):6               title ''              with      points ls 8, \
            '<(grep -e "WS.S\...  " '.mod.')' using ($7+0.2):3               title 'Model total'   with lines       ls 1, \
            '<(grep -e "WS.S\...\." '.mod.')' using ($7+0.2):4 smooth unique title 'Model compute' with linespoints ls 2, \
            '<(grep -e "WS.S\...\." '.mod.')' using ($7+0.2):5 smooth unique title 'Model memory'  with linespoints ls 3, \
            '<(grep -e "WS.S\...\." '.mod.')' using ($7+0.2):6 smooth unique title 'Model storage' with linespoints ls 4, \
            '<(grep -e "WS.S\...\." '.mod.')' using ($7+0.2):4               title ''              with      points ls 2, \
            '<(grep -e "WS.S\...\." '.mod.')' using ($7+0.2):5               title ''              with      points ls 3, \
            '<(grep -e "WS.S\...\." '.mod.')' using ($7+0.2):6               title ''              with      points ls 4
        print 'WS.S '.h.' '.t
        
        
        # --------------------------------------------------------------------------------------------------
        #
        set pointsize  1.0
        set ytics  out 
        set xtics  out 0,4
        set mxtics 4
        #
        # --------------------------------------------------------------------------------------------------
        
        # --------------------------------------------------------------------------------------------------
        #
        # Scaling Compute load + background
        #
        do for [i=1:8] {
            set output  h.'/scaling_compute_'.i.'_'.h.'.'.t
          # set title      'scaling compute '.i.' ['.h.']'
            set xlabel     'number of applications' font term_font
            set ylabel     'time to completion (s)' font term_font
            plot [0:17][] \
                '<(grep -e " C'.i.'\...  " '.dat.')' using ($7-0.2):3               title 'Exp.  total'   with lines       ls 5, \
                '<(grep -e " C'.i.'\...\." '.dat.')' using ($7-0.2):4 smooth unique title 'Exp.  compute' with linespoints ls 6, \
                '<(grep -e " C'.i.'\...\." '.dat.')' using ($7-0.2):5 smooth unique title 'Exp.  memory'  with linespoints ls 7, \
                '<(grep -e " C'.i.'\...\." '.dat.')' using ($7-0.2):6 smooth unique title 'Exp.  storage' with linespoints ls 8, \
                '<(grep -e " C'.i.'\...\." '.dat.')' using ($7-0.2):4               title ''              with      points ls 6, \
                '<(grep -e " C'.i.'\...\." '.dat.')' using ($7-0.2):5               title ''              with      points ls 7, \
                '<(grep -e " C'.i.'\...\." '.dat.')' using ($7-0.2):6               title ''              with      points ls 8, \
                '<(grep -e " C'.i.'\...  " '.mod.')' using ($7+0.2):3               title 'Model total'   with lines       ls 1, \
                '<(grep -e " C'.i.'\...\." '.mod.')' using ($7+0.2):4 smooth unique title 'Model compute' with linespoints ls 2, \
                '<(grep -e " C'.i.'\...\." '.mod.')' using ($7+0.2):5 smooth unique title 'Model memory'  with linespoints ls 3, \
                '<(grep -e " C'.i.'\...\." '.mod.')' using ($7+0.2):6 smooth unique title 'Model storage' with linespoints ls 4, \
                '<(grep -e " C'.i.'\...\." '.mod.')' using ($7+0.2):4               title ''              with      points ls 2, \
                '<(grep -e " C'.i.'\...\." '.mod.')' using ($7+0.2):5               title ''              with      points ls 3, \
                '<(grep -e " C'.i.'\...\." '.mod.')' using ($7+0.2):6               title ''              with      points ls 4
            print '   C '.h.' '.t.' '.i
        }
        
        
        # --------------------------------------------------------------------------------------------------
        #
        # Scaling Memory load + background
        #
        do for [i=1:8] {
            set output  h.'/scaling_memory_'.i.'_'.h.'.'.t
          # set title      'scaling memory '.i.' ['.h.']'
            set xlabel     'number of applications' font term_font
            set ylabel     'time to completion (s)' font term_font
            plot [0:17][] \
                '<(grep -e " M'.i.'\...  " '.dat.')' using ($7-0.2):3               title 'Exp.  total'   with lines       ls 5, \
                '<(grep -e " M'.i.'\...\." '.dat.')' using ($7-0.2):4 smooth unique title 'Exp.  compute' with linespoints ls 6, \
                '<(grep -e " M'.i.'\...\." '.dat.')' using ($7-0.2):5 smooth unique title 'Exp.  memory'  with linespoints ls 7, \
                '<(grep -e " M'.i.'\...\." '.dat.')' using ($7-0.2):6 smooth unique title 'Exp.  storage' with linespoints ls 8, \
                '<(grep -e " M'.i.'\...\." '.dat.')' using ($7-0.2):4               title ''              with      points ls 6, \
                '<(grep -e " M'.i.'\...\." '.dat.')' using ($7-0.2):5               title ''              with      points ls 7, \
                '<(grep -e " M'.i.'\...\." '.dat.')' using ($7-0.2):6               title ''              with      points ls 8, \
                '<(grep -e " M'.i.'\...  " '.mod.')' using ($7+0.2):3               title 'Model total'   with lines       ls 1, \
                '<(grep -e " M'.i.'\...\." '.mod.')' using ($7+0.2):4 smooth unique title 'Model compute' with linespoints ls 2, \
                '<(grep -e " M'.i.'\...\." '.mod.')' using ($7+0.2):5 smooth unique title 'Model memory'  with linespoints ls 3, \
                '<(grep -e " M'.i.'\...\." '.mod.')' using ($7+0.2):6 smooth unique title 'Model storage' with linespoints ls 4, \
                '<(grep -e " M'.i.'\...\." '.mod.')' using ($7+0.2):4               title ''              with      points ls 2, \
                '<(grep -e " M'.i.'\...\." '.mod.')' using ($7+0.2):5               title ''              with      points ls 3, \
                '<(grep -e " M'.i.'\...\." '.mod.')' using ($7+0.2):6               title ''              with      points ls 4
            print '   M '.h.' '.t.' '.i
        }
        
        
        # --------------------------------------------------------------------------------------------------
        #
        # Scaling Storage load + background
        #
        do for [i=1:8] {
            set output  h.'/scaling_storage_'.i.'_'.h.'.'.t
          # set title      'scaling storage '.i.' ['.h.']'
            set xlabel     'number of applications' font term_font
            set ylabel     'time to completion (s)' font term_font
            plot [0:17][] \
                '<(grep -e " S'.i.'\...  " '.dat.')' using ($7-0.2):3               title 'Exp.  total'   with lines       ls 5, \
                '<(grep -e " S'.i.'\...\." '.dat.')' using ($7-0.2):4 smooth unique title 'Exp.  compute' with linespoints ls 6, \
                '<(grep -e " S'.i.'\...\." '.dat.')' using ($7-0.2):5 smooth unique title 'Exp.  memory'  with linespoints ls 7, \
                '<(grep -e " S'.i.'\...\." '.dat.')' using ($7-0.2):6 smooth unique title 'Exp.  storage' with linespoints ls 8, \
                '<(grep -e " S'.i.'\...\." '.dat.')' using ($7-0.2):4               title ''              with      points ls 6, \
                '<(grep -e " S'.i.'\...\." '.dat.')' using ($7-0.2):5               title ''              with      points ls 7, \
                '<(grep -e " S'.i.'\...\." '.dat.')' using ($7-0.2):6               title ''              with      points ls 8, \
                '<(grep -e " S'.i.'\...  " '.mod.')' using ($7+0.2):3               title 'Model total'   with lines       ls 1, \
                '<(grep -e " S'.i.'\...\." '.mod.')' using ($7+0.2):4 smooth unique title 'Model compute' with linespoints ls 2, \
                '<(grep -e " S'.i.'\...\." '.mod.')' using ($7+0.2):5 smooth unique title 'Model memory'  with linespoints ls 3, \
                '<(grep -e " S'.i.'\...\." '.mod.')' using ($7+0.2):6 smooth unique title 'Model storage' with linespoints ls 4, \
                '<(grep -e " S'.i.'\...\." '.mod.')' using ($7+0.2):4               title ''              with      points ls 2, \
                '<(grep -e " S'.i.'\...\." '.mod.')' using ($7+0.2):5               title ''              with      points ls 3, \
                '<(grep -e " S'.i.'\...\." '.mod.')' using ($7+0.2):6               title ''              with      points ls 4
            print '   S '.h.' '.t.' '.i
        }
    }
}


# ------------------------------------------------------------------------------
# vim: ft=gnuplot

