
# see http://stackoverflow.com/questions/938733/total-memory-used-by-python-process

import os


# ------------------------------------------------------------------------------
#
def get_mem_usage () :
    
    ret   = dict ()

    scale = {'kb'      : 1024.0,
             'mb'      : 1     }
    info  = {'VmPeak:' : 'mem_peak', 
             'VmSize:' : 'mem_size', 
             'VmData:' : 'mem_data', 
             'VmRSS:'  : 'mem_resident', 
             'VmStk:'  : 'mem_stack'}

    with open ('/proc/%d/status'  %  os.getpid ()) as t :

        text = t.read ()

        for key in info.keys () :

            i = text.index (key)
            v = text[i:].split (None, 3)

            if  len(v) < 3 :
                ret[info[key]] = -1
            else :
                ret[info[key]] = "%f MB" % (float(v[1]) / scale[v[2].lower ()])

        return ret


# ------------------------------------------------------------------------------
#
def get_io_usage () :
    
    ret   = dict ()
    info  = {'read_bytes:'  : 'io_read' , 
             'write_bytes:' : 'io_write'}

    with open ('/proc/%d/io'  %  os.getpid ()) as t :

        text = t.read ()

        for key in info.keys () :

            i = text.index (key)
            v = text[i:].split (None, 3)

            if  len(v) < 2 :
                ret[info[key]] = -1
            else :
                ret[info[key]] = "%d" % int(v[1])

        return ret


# ------------------------------------------------------------------------------

