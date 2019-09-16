#!/usr/bin/perl

$fh=new IO::File($ARGV[0]);
while(<$fh>)
{
    if ($_ =~ /^#/)
    {
	next;
    }
    #41095|394749|0|bgp
    my @items = split /\|/, $_;
    if ($items[2] == -1)
    {
	$items[2] = 1;
    }
    print "$items[0] $items[1] $items[2]\n";
}
