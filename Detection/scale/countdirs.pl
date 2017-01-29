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
for $time (sort {$a cmp $b} keys %hash)
{
    $i = 0;
    $start = 0;
    %fds=();
    my @pids = ();
    for $file (keys %{$hash{$time}})
    {
        die "could not fork" unless defined(my $pid = fork);
        unless ($pid) { #child execs
            exec "python reader.py -f flow-tools $file";
            #print $file, "\n";
            #exec "python tempsleep.py";
            die "exec failed";
        }
        push @pids, $pid; #parent stores children's pids
        # system("python reader.py -f flow-tools $file &");
        print +(split '/', $file )[6], "\n";
    }
    #wait for all children to finish
    for my $pid (@pids) {
    	waitpid $pid, 0;
    }
    #print "$i";
    print "\n-------\n";
    #exit;
}

sub printStats
{
    $time = shift;
    print "Stats for $time\n";
}

