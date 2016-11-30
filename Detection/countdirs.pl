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
for $file (keys %hash)
{
    print "$file\n";
    system("flow-print -f 5 < $file | grep 207.75.112.0 | grep  31.222.168.0    | grep 56933");
}
