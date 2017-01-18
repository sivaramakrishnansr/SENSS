#!/usr/bin/perl

use File::Find;

our %flows=();
our %hash=();
sub wanted {
    if (-f) {
	if ($File::Find::name =~ /\/ft-v05/)
	{
	    $fname = $File::Find::name;
	    $fname =~ /(.*)(\/ft-v05\.)(.*\.\d\d)(.*)/;
	    $time = $3;	    
	    $hash{$time}{$fname} = 1;
	}
    }
}

find(\&wanted, $ARGV[0]);
$d=scalar(keys %hash);
for $time (sort {$a<=>$b} keys %hash)
{
    $i = 0;
    $start = 0;
    %fds=();
    for $file (keys %{$hash{$time}})
    {
	open(PS,"python extract_flows.py -f flow-tools $file |") || die "Failed: $!\n";
	while (<PS> )
	{
	    #Always go with end time and save the out of order flows
	    #for future processing
	    #1453431579.95 1453431583.02 151.20.216.0:60834 -> 35.8.192.0:23 2 120 0
	    print "$_";
	    my @items = split /\s/, $_;
	    if ($start == 0) 
	    {
		$start = $items[2];
	    }
	    if ($items[2] - $last > 1)
	    {
#		push(@{$saved{$items[2]}}, $_);
		next;
	    }
	    else
	    {
		$last = $items[2];
	    }
	    if ($items[2] - $start > 1)
	    {
		printStats($items[2]);
		$start = $items[2];
		last;
	    }
	}
    }
}

sub printStats
{
    $time = shift;
    print "Stats for $time\n";
}

