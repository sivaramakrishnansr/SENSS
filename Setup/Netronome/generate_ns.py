def generate_ns():
	nodes=[]
	f=open("nodes","r")
	for line in f:
		if "#" in line:
			continue
		node=line.strip().split(" ")[0]
		nodes.append(node)
	f.close()

	fw=open("deter.ns","w")
	fw.write("set ns [new Simulator]\n")
	fw.write("source tb_compat.tcl\n\n")
	count=0
	for node in nodes:
		count=count+1
		node_name="node"+str(count)
		fw.write("set "+node_name+" [$ns node]\n")
		fw.write("tb-fix-node $"+node_name+" "+node+"\n")
		fw.write("tb-set-node-os $"+node_name+" Ubuntu-Agilio-2\n\n")
	fw.write("$ns rtproto Static\n")
	fw.write("$ns run")
	fw.close()
	
