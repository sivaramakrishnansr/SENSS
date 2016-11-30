#!/usr/bin/perl

use File::Find;

our %flows=();
our %hash=();
sub wanted {
    if (-f) {
	if ($File::Find::name =~ /\/ft/)
	{
	    $hash{$File::Find::name} = 1;
	}
    }
}

find(\&wanted, $ARGV[0]);
@files = keys %hash;
for ($i=0; $i<= $#files; )
{
    $file=$files[$i];
    print "$file\n";
    $file =~ /(.*)(\/ft-v05\.)(.*\.\d\d)(.*)/;
    $time = $3;
    open(PS,"ps axuw | grep python | grep mirkovic | wc |") || die "Failed: $!\n";
    while ( <PS> )
    {
	@items = split /\s+/, $_;
	$count = $items[1];
	print "Count $count\n";
    }
    if($count < 10)
    {
	#/nfs_ds/users/mirkovic/nfs_ds/radb_ddos/EQX2i/2016/2016-01/2016-01-22/ft-v05.2016-01-22.000001-0500
	$cmd = "python count_flows.py -f flow-tools $file > $1/dflows.$time";
	#print "$cmd\n";
	system("$cmd &");
	$i++;
    }
    else
    {
	sleep 1;
    }
}

