

import radical.utils as ru

import atoms as rsa

# 
# 
# # ------------------------------------------------------------------------------
# class Description (object) :
# 
#     # --------------------------------------------------------------------------
#     def __init__ (self, fname) :
#         """
#         fname: json input file
#         """
# 
#         self.fname = fname
#         self.descr = ru.read_json (fname)
# 
# 
#     # --------------------------------------------------------------------------
#     def generate_troy_workload (self) :
# 
#         try :
#             import troy
# 
#         except Exception as e :
#             radical.synapse._logger.error ("Cannot import troy")
#             return  None
# 
# 
#         workload = troy.Workload ()
# 
#         for sequence in self.descr[ in radical_students :
#             workload.add_task (create_task_description ())
# 
#         return workload
# 
# 
# 
# with open ('%s/synapse/experiments/%s.dat' % (home, host), 'a') as f :
# 
#     _     = os.popen ('sync')
# #   _     = os.popen ('rm -f /tmp/synapse_*')
# #   _     = os.popen ('sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"')
# 
#     start = time.time()
# 
# 
#     load_id        = str(os.environ.get ('SYNAPSE_ID',           'X'))
#     load_instances = int(os.environ.get ('SYNAPSE_INSTANCES',      1))
#     load_compute   = int(os.environ.get ('SYNAPSE_COMPUTE_GFLOPS', 0))
#     load_memory    = int(os.environ.get ('SYNAPSE_MEMORY_GBYTES' , 0))
#     load_storage   = int(os.environ.get ('SYNAPSE_STORAGE_GBYTES', 0))
# 
#     apps = list()
# 
#     # create containers for different system workload types
#     for i in range (0, load_instances) :
# 
#         app = dict()
#         app['c'] = rsa.Compute ()
#         app['m'] = rsa.Memory  ()
#         app['s'] = rsa.Storage ()
#       # app['n'] = rsa.Network ()
# 
#         apps.append (app)
# 
# 
#     # run load (this spawns threads as quickly as possible)
#     for app in apps :
# 
#         # the atoms below are executed concurrently (in their own threads)
#         app['c'].run (info={'n'   : load_compute})  # consume  10 GFlop CPY Cycles
#         app['m'].run (info={'n'   : load_memory})   # allocate  5 GByte memory
#         app['s'].run (info={'n'   : load_storage,   # write     2 GByte to disk
#                             'tgt' : '%(tmp)s/synapse_storage.tmp.%(pid)s'})
# 
#       # app['n'].run (info={'type'   : 'server', # communicate a 1 MByte message
#       #                     'mode'   : 'read',
#       #                     'port'   : 10000,
#       #                     'n'      : 100})
#       # time.sleep (1)
#       # app['n'].run (info={'type'   : 'client',
#       #                     'mode'   : 'write',
#       #                     'host'   : 'localhost',
#       #                     'port'   : 10000,
#       #                     'n'      : 100})
# 
# 
#     # all are started -- now wait for completion and collect times
#     times = {}
#     times['c'] = 0.0
#     times['m'] = 0.0
#     times['s'] = 0.0
#   # times['n'] = 0.0
# 
#     cid = 0
#     for app in apps :
#         cid += 1
# 
#         info_c = app['c'].wait ()
#         info_m = app['m'].wait ()
#         info_s = app['s'].wait ()
#       # info_n = app['n'].wait ()
# 
#         t_c    = float(info_c['timer'])
#         t_m    = float(info_m['timer'])
#         t_s    = float(info_s['timer'])
#       # t_n    = float(info_n['timer'])
# 
#       # import pprint
#       # pprint.pprint (info_c)
# 
#         times['c'] += t_c
#         times['m'] += t_m
#         times['s'] += t_s
#       # times['n'] += t_n
# 
#         output = '%-10s %10s ------- %7.2f %7.2f %7.2f %5d %5d %5d %5d' % \
#                 (host, "%s.%002d" % (load_id, cid), t_c, t_m, t_s,
#                  load_instances, load_compute, load_memory, load_storage)
# 
#       # print output
#         f.write ("%s\n" % output)
# 
# 
#     # also print summary
#     output = '%-10s %7s    %7.2f ------- ------- ------- %5d %5d %5d %5d' % \
#              (host, load_id, time.time() - start, 
#              load_instances, load_compute, load_memory, load_storage)
# 
# #   print output
#     f.write ("%s\n" % output)
# 
#     time.sleep (10)
#     _ = os.popen ('ps -ef | grep -i "/tmp/synapse_" | grep -v grep | cut -c 8-15 | xargs -r kill -9')
# 
# #   print su.get_mem_usage ()
# #   print su.get_io_usage  ()
# 
