all: reader

reader: reader.cc collector.cc iprange.cc records.cc cell.cc flow.cc util.cc map.pb.cc
	g++ -std=c++11 -g -o reader reader.cc collector.cc iprange.cc records.cc cell.cc flow.cc util.cc map.pb.cc -ldl -lprotobuf -lpthread

clean:
	rm reader
