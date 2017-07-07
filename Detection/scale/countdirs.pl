#!/usr/bin/perl

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
    $cmd = "python extract_flows.py $file -f flow-tools >> $dir.out";
    print "$cmd\n";
    system("$cmd");
}
