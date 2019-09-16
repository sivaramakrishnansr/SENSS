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
$class = 0;
$limit = 0;
while(<$fh>)
{
    if ($_ =~ /Victim/ && $_ =~ /making/)
    {
	#Victim 328107 making up traffic
	@items = split /\s/, $_;
	$victim = $items[1];
    }
    elsif ($_ =~ /fixed/)
    {
	#34781 199451: initial 0 original 4754 still polluted 2079 demoted 0 liar 34781 old path length 5.294 new 6.269
	#1497672986 class 3 tier 3 limit 7752 fixed 0.648010352636687
	@items = split /\s/, $_;
	$class = $items[2];
	$limit = $items[6];
    }
    elsif($_ =~ /polluted/)
    {
	@items = split /\s/, $_;
	if ($items[18] >= $items[16]+0)
	{
	    $val = $items[18] - $items[16];
	    push(@{$results{$limit}{$class}}, $val);
	}
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
