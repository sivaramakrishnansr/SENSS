all: reader

reader: reader.cc iprange.cc records.cc cell.cc flow.cc util.cc
	g++ -std=c++11 -g -o reader reader.cc iprange.cc records.cc cell.cc flow.cc util.cc -ldl

clean:
	rm reader
