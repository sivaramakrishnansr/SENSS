#!/usr/bin/perl
$|=1;

$precision=0.01;
$ITERS=10; 
$usage="$0 type startlimit [alpha]\n";
%dsts = ();

sub customers;

if ($#ARGV < 1)
{
    print $usage;
    exit;
}
$type = $ARGV[0];
$startlimit = int($ARGV[1]);
$alpha = int($ARGV[2])/100;
our %as, %leaves, %short, %rt, %tier, %parent, %shadow, %ts;
our $NUMLEG=1000;
our $NUMATT=1000;
our $MINCUST=100;
our $LEG=1000;
our $ATT=100000;
our $ENOUGH=1000;
@tiered=();
load_topology('topology/hier0501.all');
$t1=scalar(keys %{$tier{1}});
$t2=scalar(keys %{$tier{2}});
$t3=scalar(keys %{$tier{3}});
print "T1 $t1 T2 $t2 T3 $t3 leaves " . scalar(keys %leaves) . " short " . scalar(keys %short) . "\n";
# Generate scenarios
# Just keep t=1
for $t (1)
{
    @limits=(1,2,5,10,20,50,100,200,500,1000, 2000,5000,10000);
	

    our %senss, %single, %multi, %all, %rt, %src, %att, %original, %demote, %rtcand, %popular, %polluted;
    for $l (@limits)
    {
	print "Limit $l\n";
	if ($l < $startlimit)
	{
	    next;
	}
	%results=();
	%cdresults=();
	%oldmean=();
	$oldmean{1} = $oldmean{2} = $oldmean{3} = -1;
	while(1)
	{
	    	%senss=();
                # select top points for deployment                         
                $i = 0;
		while(scalar(keys %senss) < $l)
		{
                    $senss{$tiered[$i]} = 1;
                    $i++;
                }

                for $s (sort {$a <=> $b} keys %senss)
                {
                    print "SENSS $s\n";
                }

		# select single, multi and all
		%single=();
		%multi=();
		%all=();
		select_deployment($type);
		$class = 0;
		for $victims (\%single, \%multi, \%all)
		{
		    $i = 0;
		    $class++;
		    if (scalar(@{$results{$class}}) >= $ENOUGH)
		    {
			next;
		    }
		    @vs = keys %{$victims};
		    print "Victim candidates " . scalar(@vs) . "\n";
		    %selected=();
		    while(scalar(keys %selected) < $ITERS && scalar(keys %selected) < scalar(@vs))
		    {
			$r = rand(scalar(@vs));
			$selected{$vs[$r]} = 1;
		    }
		    print "Selected " . scalar(keys %selected) . " victims\n";
		    %dsts = ();
		    for $s (keys %selected)
		    {
			$dsts{$s} = 1;
		    }
		    %rt = ();		    
		    %rtcand = ();
   		    
		    # Initialize routing
		    for $a (keys %short)
		    {
			for $b (keys %{$short{$a}})
			{
			    if (exists($selected{$b}))
			    {
				$rt{$a}{$b}{'next'} = $b;
				$rt{$a}{$b}{'hops'} = 1;
				$rt{$a}{$b}{'rel'} = $as{$a}{$b};
				$rt{$a}{$b}{'changed'} = 1;
				$rt{$a}{$b}{'path'} = " $b";
				$rtcand{$a}{$b}{$b} = 1;
			    }
			}
		    }
		    find_routes(0,0,0,'init');
		    # Load traffic
		    for $victim (keys %selected)
		    {
			$m=make_up_realistic_traffic($victim);
			# Poorly reachable victim
			if ($m == 0)
			{
			    next;
			}
			$attack = 0;
			$dropped = 0;
			if ($type eq "sig")
			{
			    for $at (sort {$a<=>$b} keys %att)
			    {
				# Go from each attacker to victim
				if (!exists($rt{$at}{$victim}))
				{
				    next;
				}
				$attack += $att{$at};
				$start = $at;
				$found = 0;
				$hops = 0;
				while($start != $victim && $hops < 20)
				{
				    if (exists($senss{$start}))
				    {
					$dropped += $att{$at};
					$found = 1;
					last;
				    }
				    $hops++;
				    $start = $rt{$start}{$victim}{'next'};
				}
			    }
			    if ($attack > 0)
			    {
				$r = $dropped/$attack;
				$ofh = 0;
				$time=time();
				if ($class == 1)
				{
				    print "$time class $class tier $t limit $l attack $attack dropped $dropped r $r\n";
				}
				elsif($class == 2)
				{
				    print "$time class $class tier $t limit $l attack $attack dropped $dropped r $r\n";
				}
				else
				{
				    print "$time class $class tier $t limit $l attack $attack dropped $dropped r $r\n";
				}
				push (@{$results{$class}}, $r);
			    }
			}
			elsif($type eq "nosig")
			{
			    %ltraffic=();
			    %atraffic=();
			    $ltraffic{'all'} = 0;
			    for $lt (sort {$a<=>$b} keys %src)
			    {
				# Go from each legitimate source to victim
				if (!exists($rt{$lt}{$victim}))
				{
				    next;
				}
				$ltraffic{'all'} += $src{$lt};
				$start = $lt;
				$hops = 0;
				$prev = 0;
				while($start != $victim && $hops < 20)
				{
				    $is = exists($senss{$start});
				    $hops++;
				    if (exists($senss{$start}))
				    {
					if ($prev > 0)
					{
					    $ltraffic{$prev . "-" . $start} += $src{$lt};
					}
					else
					{
					    $ltraffic{$start} += $src{$lt};
					}
				    }
				    $prev = $start;
				    $next = $rt{$start}{$victim}{'next'};
				    $start = $next;
				}
			    }
			    %enc = ();
			    for $at (sort {$a<=>$b} keys %att)
			    {
				# Go from each attacker to victim
				if (!exists($rt{$at}{$victim}))
				{
				    next;
				}
				$atraffic{'all'} += $att{$at};
				$start = $at;
				$hops = 0;
				$prev = 0;
				while($start != $victim && $hops < 20)
				{
				    $hops++;
				    $is = exists($senss{$start});
				    if (exists($senss{$start}))
                                    {
					if ($prev > 0)
                                        {
                                            $atraffic{$prev . "-" . $start} += $att{$at};
                                        }
					else
                                        {
                                            $atraffic{$start} += $att{$at};
                                        }
					$enc{$at} = 1;
                                    }
                                    $prev = $start;
                                    $next = $rt{$start}{$victim}{'next'};
                                    $start = $next;
				}
			    }
			    # Find where to filter
			    %candidates=();
			    %droptag = ();
			    for $k (keys %atraffic)
			    {
				if (!exists($ltraffic{$k}))
				{
				    $candidates{$k}{'att'} = $atraffic{$k};
				    $candidates{$k}{'leg'} = 0;
				}
				elsif($ltraffic{$k} < $ltraffic{'all'}*$alpha)
				{
				    $candidates{$k}{'att'} = $atraffic{$k};
				    $candidates{$k}{'leg'} = $ltraffic{$k};
				}
			    }
			    @sorted = sort {$candidates{$a}{'leg'} <=> $candidates{$b}{'leg'}} keys %candidates;
			    $cd = 0;
			    for $s (@sorted)
			    {
				$rl =  $candidates{$s}{'leg'}/$ltraffic{'all'};
				$ra =  $candidates{$s}{'att'}/$atraffic{'all'};
				$cdr = $cd/$ltraffic{'all'};

				if ($cd + $candidates{$s}{'leg'} <= $ltraffic{'all'}*$alpha)
				{
				    $droptag{$s} = 1;
				    $cd += $candidates{$s}{'leg'}; 
				}
			    }
			    $rcd = 0;
			    $dropped = 0;
			    for $lt (sort {$a<=>$b} keys %src)
			    {
				# Go from each legitimate source to victim
				if (!exists($rt{$lt}{$victim}))
				{
				    next;
				}
				$start = $lt;
				$hops = 0;
				$prev = 0;
				while($start != $victim && $hops < 20)
				{
				    $hops++;
				    $next = $rt{$start}{$victim}{'next'};
				    if ($prev > 0)
				    {
					$tag = "$prev-$start";
				    }
				    else
				    {
					$tag = "$start";
				    }
				    if (exists($droptag{$tag}) && exists($ltraffic{$tag}))
				    {
					$rcd += $src{$lt};
					last;
				    }
				    $prev = $start;
				    $start = $next;
				}
			    }
			    for $at (sort {$a<=>$b} keys %att)
			    {
				# Go from each attacker to victim
				if (!exists($rt{$at}{$victim}))
				{
				    next;
				}
				$start = $at;
				$hops = 0;
				$prev = 0;

				while($start != $victim && $hops < 20)
				{
				    $hops++;
				    $next = $rt{$start}{$victim}{'next'};
				    if ($prev > 0)
				    {
					$tag = "$prev-$start";
				    }
				    else
				    {
					$tag = "$start";
				    }
				    if (exists($droptag{$tag}) && exists($atraffic{$tag}))
				    {
					$dropped += $att{$at};
					last;
				    }
				    $prev = $start;
				    $start = $next;
				}
			    }
			    $attack = $atraffic{'all'};
			    if ($attack == 0)
			    {
				next;
			    }
			    $r = $dropped/$atraffic{'all'};
			    $lr = $rcd/$ltraffic{'all'};
			    
			    $time=time();
			    if ($class == 1)
			    {
				print "$time class $class tier $t limit $l attack $attack dropped $dropped r $r cd $lr\n";
			    }
			    elsif($class == 2)
			    {
				print "$time class $class tier $t limit $l attack $attack dropped $dropped r $r cd $lr\n";
			    }
			    else
			    {
				print "$time class $class tier $t limit $l attack $attack dropped $dropped r $r cd $lr\n";
			    }
			    push (@{$results{$class}}, $r);
			    push (@{$cdresults{$class}}, $lr);
			}
			elsif($type eq "cross")
			{
			    %popular=();
			    # Find all ASes crossed to reach a victim
			    $tlt = 0;
			    for $lt (sort {$a<=>$b} keys %src)
			    {
				# Go from each source to victim
				if (!exists($rt{$lt}{$victim}))
				{
				    next;
				}
				$hidden = $src{$lt}/$LEG;
				$popular{$lt} += $hidden;
				$tlt += $hidden;
				$start = $lt;
				$hops = 0;
				while($start != $victim && $hops < 20)
				{
				    $hops++;
				    $next = $rt{$start}{$victim}{'next'};
				    $popular{$next} += $hidden;
				    $start = $next;
				}
			    }
			    # Bottleneck candidates are those where at least
			    # 10% of sources cross that AS and not 100%
			    @populars = keys %popular;
			    for $p (@populars)
			    {
				if ($popular{$p}/$tlt < 0.1 || $popular{$p}/$tlt == 1)
				{
				    delete($popular{$p});
				}
			    }
			    @sorted = sort{$popular{$b}<=>$popular{$a}} keys %popular;
			    if (scalar(@sorted) == 0)
			    {
				next;
			    }
			    $bneck = $sorted[0];
			    print "Bottleneck at $bneck victim $victim\n";
			    fix_control_paths($victim, $bneck);
			    print "$bneck $victim: Original " . scalar(keys %original) . " still polluted " . scalar(keys %polluted) . " demoted " . scalar(keys %demote) . " bneck $bneck \n";
			    
			    if (scalar(keys %original) == 0)
			    {
				next;
			    }
			    
			    $r = 1-(scalar(keys %polluted)/scalar(keys %original));
			    $time=time();
			    if ($class == 1)
			    {
				print "$time class $class tier $t limit $l fixed $r\n";
			    }
			    elsif($class == 2)
			    {
				print "$time class $class tier $t limit $l fixed $r\n";
			    }
			    else
			    {
				print "$time class $class tier $t limit $l fixed $r\n";
			    }
			    push (@{$results{$class}}, $r);
			}
		    }
		}
		$stop=0;
		$enough=0;
		# Check if we ran long enough or if we still have too much variance
		for $class (1,2,3)
		{
		    @sorted = sort {$a <=> $b} @{$results{$class}};
		    $mean =  $sorted[int(scalar(@sorted)*0.5)];
		    $om = $oldmean{$class};
		    $abs = abs($mean-$om);
		    $s = scalar(@{$results{$class}});
		
		    if (abs($mean-$om) < $precision)
		    {
			$stop++;
		    }
		    if (scalar(@{$results{$class}}) >= $ENOUGH)
		    {
			$enough++;
		    }
		    $oldmean{$class}=$mean;
		    print "$class $t $l Mean $mean oldmean $om $abs samples $s\n enough $enough\n";
		}
		if ($enough > 2 && $stop > 1)
		{
		    last;
		}
	}
    }
}


sub fix_control_paths
{
    ($victim,$bneck) = @_;
    print "Fix control paths victim $victim bneck $bneck\n";
    
    collect_data_paths($victim, 0);
    # Remember original paths
    collect_original_paths($victim,$bneck);
    print "Original " . scalar(keys %original) . "\n";
    # Find control paths
    %demote = ();
    $voted = 0;
    for $s (keys %senss)
    {
	if (!exists($rt{$s}{$victim}))
	{
	    next;
	}
	if (!exists($ltraffic{$s}))
	{
	    next;
	}
	if ($rt{$s}{$victim}{'path'} !~ / $bneck /)
	{
	    next;
	}
	$prev = -1;
	# If there is a bottleneck and two SENSS
	# nodes around it or one SENSS one victim, then we should demote
	@path = split /\s+/, $rt{$s}{$victim}{'path'};
	shift(@path);
	%popular=();
	for $p (@path)
	{
	    if ((exists($senss{$p}) || $p == $victim))
	    {
		if ($rt{$s}{$victim}{'path'} =~ /($bneck)(.*)($p)/)
		{
		    for $q (@path)
		    {
			if ($q == $victim)
			{
			    last;
			}
			$demote{$q}++;
		    }
		    $voted++;
		    last;
		}
	    }
	}
    }
    for $d (keys %demote)
    {
	if ($demote{$d} < $voted)
	{
	    delete($demote{$d});
	}
    }
    fix_paths($victim,$bneck);
}

sub fix_paths
{
    ($victim,$bneck) = @_;
    if(scalar(keys %demote)==0)
    {
	%polluted = %original;
	return;
    }
    print "Fix paths demote " . scalar(keys %demote) . "\n";
    for $d (keys %demote)
    {
	print "Demote $d\n";
    }
    # zero down demoted routes
    for $a (keys %senss)
    {
	if (exists($original{$a}))
	{
	    $td=1;
	    for $d (keys %demote)
	    {
		if ($rt{$a}{$victim}{'path'} !~ / $d /)
		{
		    $td=0;
		}
	    }
	    # Withdraw routes that were deleted
	    if ($td)
	    {
		delete($rt{$a}{$victim});
		for $b (keys %short)
		{
		    if (exists($rt{$b}{$victim}) && $rt{$b}{$victim}{'path'} =~ /\s$a\s/)
		    {
			delete($rt{$b}{$victim});
		    }
		}
	    }
	}
    }
    for $a (keys %short)
    {
	if(!exists($rt{$a}{$victim}))
	{
	    # see if we can adopt any other route
	    # by forcing neighbors of nodes that have 
	    # no route
	    # readvertise
	    for $b (keys %{$short{$a}})
	    {
		if (exists($rt{$b}{$victim}) && $rt{$b}{$victim}{'next'} != $a && $b != $bneck)
		{
		    $rt{$b}{$victim}{'changed'} = 1;
		}
	    }
	}		
    }	
    find_routes(0,0,0,'newr');
    %polluted = ();
    for $a (keys %short)
    {
	if (exists($rt{$a}{$victim}))
	{
	    if ($rt{$a}{$victim}{'path'} =~ /\s$bneck\s/)
	    {
		$polluted{$a} = 1;
	    }
	}
    }
}

sub collect_data_paths
{
    ($victim, $sh) = @_;
    %ltraffic=();
    $ltraffic{'all'} = 0;
    %paths = ();
    for $lt (sort {$a<=>$b} keys %src)
    {
	# Go from each source to victim
	if (!exists($rt{$lt}{$victim}))
	{
	    next;
	}
	$ltraffic{'all'} += $src{$lt};
	$start = $lt;
	$prev = -1;
	$factor = 1;
	$hops = 0;
	while($start != $victim && $hops < 20)
	{	    
	    if ($sh && exists($shadow{$start}))
	    {
		$next = $shadow{$start}{$victim}{'next'};
	    }
	    else
	    {
		$next = $rt{$start}{$victim}{'next'};
	    }
	    if ($next == $victim)
	    {
		$paths{$start . " " . $next} = 1;
	    }
	    $hops ++;
	    if (exists($senss{$start}))
	    {
		if ($prev != -1)
		{
		    $paths{"$prev $start $next"} = 1;
		}
		else
		{
		    $paths{"$start $next"} = 1;
		}
		$ltraffic{$start}{'in'} += $src{$lt}*$factor;
	    }
	    if ($start == $bneck)
	    {
		$factor = 0.5;
	    }
	    if (exists($senss{$start}))
	    {
		$ltraffic{$start}{'out'} += $src{$lt}*$factor;
	    }
	    $prev = $start;
	    $start = $next;
	}
    }
    return (keys %paths);
}
sub collect_control_paths
{
    @paths=();
    for $s (keys %senss)
    {
	if (exists($rt{$s}{$victim}))
	{
	    push(@paths, $s . " " . $rt{$s}{$victim}{'path'});
	}
    }
    return @paths;
}

sub collect_original_paths
{
    ($victim,$bneck) = @_;
    %original=();
    %polluted=();

    for $a (keys %short)
    {
	if (exists($rt{$a}{$victim}))
	{
	    $path = $rt{$a}{$victim}{'path'};
	    if ($path =~ /\s$bneck\s/)
	    {
		$original{$a} = 1;
	    }
	}
    }
}

sub make_up_realistic_traffic
{
    $victim = shift;
    %src=();
    %att=();
    print "Victim $victim making up traffic\n";
    @endpoints = keys %leaves;
    # Select 1000 legitimate sources and 1000 attackers
    %possrc = ();
    for $a (keys %leaves)
    {
	if (exists($rt{$parent{$a}}{$victim}))
	{
	    $possrc{$parent{$a}} = 1;
	}
    }
    print "Possible sources " . scalar(keys %possrc)  . "\n";
    if (scalar(keys %possrc) < $NUMLEG+$NUMATT)
    {
	return 0;
    }
    # Load mirai
    $fh = new IO::File("mirai.txt");
    $tot = 0;
    while(<$fh>)
    {
	@items = split (/\,/, $_);
	$cand = $items[0];
	if ($cand == $victim)
	{
	    next;
	}
	if (exists($leaves{$cand}))
	{
	    $att{$parent{$cand}} += $items[1]*$ATT;
	    $tot += $items[1];
	}
	elsif(exists($short{$cand}))
	{
	    $att{$cand} += $items[1]*$ATT;
	    $tot += $items[1];
	}
    }
    print "Total $tot\n";
    $numlegitimate = 0;
    # Load legitimate
    $fh = new IO::File("clients.txt");
    while(<$fh>)
    {
	@items = split /\s+/, $_;
	$cand = $items[1];
	$cand =~ s/AS//;
	print "Candidate for clients $cand\n";
	if (exists($leaves{$cand}))
	{
	    $cand = $parent{$cand};
	}
	if (exists($src{$cand}))
	{
	    next;
	}
	if ($cand == $victim)
	{
	    next;
	}
	if (!exists($rt{$cand}{$victim}))
	{
	    next;
	}
	$src{$cand} += $items[2]*$LEG;
	$numlegitimate++;
	print "Allocated " . $numlegitimate . " source " . $cand . "\n";
    }
    print "Done with legitimate\n";
    return 1;
}

sub make_up_traffic
{
    $victim = shift;
    %src=();
    %att=();
    print "Victim $victim making up traffic\n";
    @endpoints = keys %leaves;
    # Select 1000 legitimate sources and 1000 attackers
    %possrc = ();
    for $a (keys %leaves)
    {
	if (exists($rt{$parent{$a}}{$victim}))
	{
	    $possrc{$parent{$a}} = 1;
	}
    }
    print "Possible sources " . scalar(keys %possrc)  . "\n";
    if (scalar(keys %possrc) < $NUMLEG+$NUMATT)
    {
	return 0;
    }
    $numlegitimate = 0;
    $numattackers = 0;
    while ($numlegitimate < $NUMLEG)
    {
	$r = rand(scalar(@endpoints));
	$cand = $endpoints[$r];
	if (!exists($src{$parent{$cand}}) && $cand != $victim &&  exists($rt{$parent{$cand}}{$victim}))
	{
	    $src{$parent{$cand}} += $LEG;
	    $numlegitimate++;
	}
    }
    print "Done with legitimate\n";
    while ($numattackers < $NUMATT)
    {
	$r = rand(scalar(@endpoints));
	$cand = $endpoints[$r];
	$par = $parent{$cand};
	if (!exists($att{$parent{$cand}}) && !exists($src{$parent{$cand}}) && $cand != $victim && exists($rt{$parent{$cand}}{$victim}))
	{
	    $att{$parent{$cand}} += $ATT;
	    $numattackers++;
	}
    }
    print "Done with attack\n";
    return 1;
}

sub select_deployment
{
    $type = shift;
    if ($type =~ /sig/)
    {
	for $a (keys %senss)
	{
	    for $b (keys %{$short{$a}})
	    {
		if ($short{$a}{$b} == 1)
		{
		    $issingle = 1;
		    for $c (keys %{$short{$b}})
		    {
			if ($short{$b}{$c} == 3 && $c != $a)
			{
			    $issingle = 0;
			}
		    }
		    if ($issingle)
		    {
			$single{$b} = 1;
		    }
		    else
		    {
			$multi{$b} = 1;
		    }
		}
	    }	   
	}
    }
    for $a (keys %short)
    {
	if (!exists($senss{$a}) && !exists($single{$a})  && !exists($multi{$a}))
	{
	    $all{$a} = 1;
	}
    }
    print "Selected single," . scalar(keys %single) . " multi, " . scalar(keys %multi) . " and all " . scalar(keys %all) . "\n";    
}

sub load_topology
{
    $file = shift;
    my $fh = new IO::File($file);
    while(<$fh>)
    {
	my @items = split /\s+/, $_;
	if ($items[2] == 1)
	{
	    $as{$items[0]}{$items[1]} = 1;
	    $as{$items[1]}{$items[0]} = 3;
	}
	elsif ($items[2] == 2)
	{
	    $as{$items[0]}{$items[1]} = 3;
	    $as{$items[1]}{$items[0]} = 1;
	}
	else
	{
	    $as{$items[0]}{$items[1]} = 2;
	    $as{$items[1]}{$items[0]} = 2;
	}
    }
    # Figure out leaves first
    for $a (keys %as)
    {
	@neighbors = keys %{$as{$a}};
	if (scalar(@neighbors) == 1)
	{
	    $leaves{$a} = 1;
	    $parent{$a} = $neighbors[0];
	}
	else
	{
	    $isleaf = 1;
	    for $b (keys%{$as{$a}})
	    {
		if ($as{$a}{$b} < 3)
		{
		    $isleaf = 0;
		}
	    }
	    if ($isleaf)
	    {
		$leaves{$a} = 1;
		$parent{$a} = $neighbors[0];
	    }
	}
    }
    # Deal just with non leaves
    for $a (keys %as)
    {
	if (!exists($leaves{$a}))
	{
	    for $b (keys %{$as{$a}})
	    {
		if (!exists($leaves{$b}))
		{
		    $short{$a}{$b} = $as{$a}{$b};
		    $short{$b}{$a} = $as{$b}{$a};
		}
	    }
	}
    }
    $all = scalar(keys %short);
    %temp=();
    for $s (sort {$a <=> $b} keys %short)
    {
	$temp{$s} = customers($s);
    }
    for $s (sort {$temp{$a} <=> $temp{$b}} keys %temp)
    {
	for $p (keys %{$short{$s}})
	{
	    # $p is provider of $s
	    if ($short{$s}{$p} == 3)
	    {
		$temp{$p} += $temp{$a};
	    }
	}
    }
	
    #Order nodes by size of customer cone
    @tiered = sort {$temp{$b} <=> $temp{$a}} (keys %short);
}

sub find_routes
{
    my ($liar, $neighbor, $print, $label) = @_;
    $round = 0;
    do
    {
	$updated = 0;
	$round++;
	for $an (sort {$a <=> $b} keys %short)
	{
	    $i++;
	    for $p (keys %dsts)
	    {
		if (exists($rt{$an}{$p}) && $rt{$an}{$p}{'changed'} == 1)
		{
		    for $bn (sort {$a <=> $b} keys %{$short{$an}})
		    {
			# OK to announce
			$circle = circle($rt{$an}{$p}{'path'}, $bn);
			$notliaran = ($short{$an}{$bn} == 3 && $an == $liar);
			if ($liar == $an && exists($shadow{$an}{$p}))
			{
			    # Don't announce if you want to preserve your old path
			    # to the victim
			    if ($bn == $neighbor)
			    {
				next;
			    }
			    # Don't announce to providers or it creates circles
			    if ($notliaran)
			    {
				next;
			    }
			}
			if ($p != $bn && !circle($rt{$an}{$p}{'path'}, $bn) && $rt{$an}{$p}{'next'} != $bn && ($short{$an}{$bn} == 1 || $rt{$an}{$p}{'rel'} == 1))
			{
			    # store a candidate route and select best one to reannounce
			    $rtcand{$bn}{$p}{$an} = $rt{$an}{$p}{'hops'} + 1;
			    $updated += find_best($bn, $p, $print, $label);
			}
		    }
		    $rt{$an}{$p}{'changed'} = 0;
		}
	    }
	}
	print "Updated $updated\n";
    }while($updated > 0);
}

sub find_best
{
    ($bn, $p, $print, $label) = @_;
    $best = 0;
    $besthops = 0;

    for $c (keys %{$rtcand{$bn}{$p}})
    {
	#Check if things changed due to deletion
	if (!exists($rt{$c}{$p}) && $c != $p)
	{
	    next;
	}
	#Update estimate
	if ($c != p)
	{
	    $rtcand{$bn}{$p}{$c} = $rt{$c}{$p}{'hops'} + 1;
	}
	else
	{
	    $rtcand{$bn}{$p}{$c} = 1;
	}
	# Check if candidate has you in his path
	if (circle($rt{$c}{$p}{'path'}, $bn))
	{
	    next;
	}
	# accept the new route
	if ($best == 0 || 
	    ($best > 0 && (
		 $short{$bn}{$c} < $short{$bn}{$best} || 
		 ($short{$bn}{$c} == $short{$bn}{$best} && $besthops > $rtcand{$bn}{$p}{$c}) || 
		 ($short{$bn}{$c} == $short{$bn}{$best} && $besthops == $$rtcand{$bn}{$p}{$c} && $best > $c) ||
		 ($best == $c))))
	{
	    $skip = 0;
	    if (scalar(keys %demote) > 0)
	    {
		# Also check that candidate path does not have a demoted node
		# if you are a SENSS node
		if ($c != $p)
		{
		    $path =  " " . $c . $rt{$c}{$p}{'path'};
		}
		else
		{
		    $path = " " . $c;
		}
		
		$skip = 1;

		for $d (keys %demote)
		{
		    if($path !~ /\s$d\s/ || !exists($senss{$bn}))
		    {
			$issenss = exists($senss{$bn});
			$skip = 0;
		    }
		}
	    }
	    if (!$skip)
	    {
		if ($best != 0)
		{
		    if ($c != $p)
		    {
			$nb = $rt{$c}{$p}{'hops'} + 1;
		    }
		    else
		    {
			$nb = 1;
		    }

		}
		$best = $c;
		if ($c != $p)
		{
		    $besthops = $rt{$c}{$p}{'hops'} + 1;
		}
		else
		{
		    $besthops = 1;
		}
	    }
	}
    }
    if ($best != 0 && ($best != $rt{$bn}{$p}{'next'} || $besthops !=  $rt{$bn}{$p}{'hops'} ||  (" " . $best . $rt{$best}{$p}{'path'} ne $rt{$bn}{$p}{'path'})))
    {
	$rt{$bn}{$p}{'next'} = $best;
	$rt{$bn}{$p}{'hops'} = $rt{$best}{$p}{'hops'}+1;
	$rt{$bn}{$p}{'rel'} = $short{$bn}{$best};
	$rt{$bn}{$p}{'changed'} = 1;
	$rt{$bn}{$p}{'path'} = " " . $best . $rt{$best}{$p}{'path'};
	return 1;
    }
    return 0;
}

sub circle
{
    ($path, $bn) = @_;
    @ases = split /\s+/, $path;
    for $a (@ases)
    {
	if ($a == $bn)
	{
	    return 1;
	}
    }
    return 0;
}

sub customers
{
    my $aa = shift;
    my $count = 0;
    for my $bb (sort {$a <=> $b} keys %{$as{$aa}})
    {
	if ($as{$aa}{$bb} == 1)
	{
	    $count++;
	}
    }
    return $count;
}


