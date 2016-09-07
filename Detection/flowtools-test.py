import flowtools

set = flowtools.FlowSet("/Users/zorro/PycharmProjects/SENSS/ft-v05.2015-07-22.000000-0400")

for flow in set:
    print "%s" % (flow.prot)