#!/usr/bin/perl
# One argument, path to the folder with attack like /nfs_ds/users/mirkovic/nfs_ds/radb_ddos

use File::Find;

$|=1;
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
$d=scalar(keys %hash);
for $file (sort keys %hash)
{
    my @items = split /\//, $file;
    $dir = "";
    for $item (@items)
    {
	if ($item =~ /WSU/ || $item =~ /EQX/ || $item =~ /CHI/  )
	{
	    $dir = $item;
	    last;
	}
    }
    #$cmd = "python extract_flows.py $file -f flow-tools >> $dir.out";
    print "$file\n";
}
