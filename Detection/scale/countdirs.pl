#!/usr/bin/perl

use File::Find;

our %flows=();
our %hash=();
sub wanted {
    if (-f) {
	if ($File::Find::name =/nfs_ds/users/mirkovic/nfs_ds /\/ft-v05/)
	{
	    $fname = $File::Find::name;
	    $fname =/nfs_ds/users/mirkovic/nfs_ds /(.*)(\/ft-v05\.)(.*\.\d\d)(.*)/;
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
    #for $file (keys %{$hash{$time}})
    #{
#	system("python reader.py -f flow-tools $file &");
	print "python reader.py -f flow-tools $file &";
	# wait here for all 29 to finish
    #}
}

sub printStats
{
    $time = shift;
    print "Stats for $time\n";
}

