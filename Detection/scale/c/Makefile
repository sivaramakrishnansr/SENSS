all: reader

reader: reader.cc iprange.cc records.cc cell.cc flow.cc util.cc
	g++ -g -o reader reader.cc iprange.cc records.cc cell.cc flow.cc util.cc -lcrypto -lssl -ldl -lpthread

clean:
	rm reader
