$|=1;
$usage = "$0 file";
if ($#ARGV < 0)
{
    print "$usage";
    exit 1;
}
%results=();
$fh = new IO::File($ARGV[0]);
%results=();
while(<$fh>)
{
    if ($_ =~ /Victim/ && $_ =~ /making/)
    {
	#Victim 328107 making up traffic
	@items = split /\s/, $_;
	$victim = $items[1];
    }
    elsif ($_ =~ /dropped/ || $_ =~ /fixed/)
    {
	#1498161459 class 3 tier 1 limit 8 attack 100000000 dropped 7500000 r 0.075
	#1497672986 class 3 tier 3 limit 7752 fixed 0.648010352636687
	@items = split /\s/, $_;
	$class = $items[2];
	$limit = $items[6];
	if ($_ =~ /dropped/)
	{
	    $val = $items[12];
	}
	else
	{
	    $val = $items[8];
	}
	push(@{$results{$limit}{$class}}, $val);
    }
}
for $limit (sort {$a <=> $b} keys %results)
{
    for $class (sort {$a <=> $b} keys %{$results{$limit}})
    {
	@sorted = sort {$a <=> $b} @{$results{$limit}{$class}};
	$sum = 0;
	for $s (@sorted)
	{
	    $sum += $s;
	}
	$l = $#sorted+1;
	$a = $sum/$l;
	print "$class $limit $sorted[int($l/4)] $sorted[int($l/2)] $sorted[int(3*$l/4)] $a $l\n";
    }
}
