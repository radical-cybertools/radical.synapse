
import time
import radical.synapse as rs

start = time.time ()
rsa_c = rs.atoms.Compute ()
rsa_m = rs.atoms.Memory  ()
rsa_s = rs.atoms.Storage ()

rsa_c.emulate(vals=[1100])   # consume  1.1 GFlop Cycles
rsa_m.emulate(vals=[322])    # allocate 0.3 GByte memory
rsa_s.emulate(vals=[0, 10])  # read 0, write 10 bytes

# atoms are now working in separate threads - wait for them.

info_c = rsa_c.wait ()
info_m = rsa_m.wait ()
info_s = rsa_s.wait ()
stop   = time.time ()

# info now contains self-profiled information for the atoms
print "t_c: %.2f" % info_c['timer']
print "t_m: %.2f" % info_m['timer']
print "t_s: %.2f" % info_s['timer']
print "ttc: %.2f" % (stop - start)

