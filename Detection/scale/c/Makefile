all: reader

reader: reader.cc iprange.cc records.cc cell.cc flow.cc util.cc
	g++ -g -o reader reader.cc iprange.cc records.cc cell.cc flow.cc util.cc -lcrypto -lssl -lpthread -ldl

clean:
	rm reader
