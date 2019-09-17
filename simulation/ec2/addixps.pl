# specify file w topology (.all) and another with ixps (.jsonl)
# enrich relationships in .all with peerings from ixps
$usage = "$0 topology.all ixps.jsonl\n";
if ($#ARGV < 1)
{
    print $usage;
    exit 0;
}
%as=();
%ixps=();
$fh = new IO::File($ARGV[0]);
while(<$fh>)
{
    @items = split /\s+/, $_;
    $as{$items[0]}{$items[1]} = $items[2];
}
close($fh);
$fh = new IO::File($ARGV[1]);
<$fh>;
while(<$fh>)
{
    @items = split(/\:/, $_);
    @elems = split(/\,/, $items[1]);
    $asn = int($elems[0]);
    $ixp = $items[$#items];
    $ixp =~ s/\}.*//;
    $ixp = int($ixp);
    $ixps{$ixp}{$asn} = 1;
}
$add = 0;
for $i (keys %ixps)
{
    @asns = keys %{$ixps{$i}};
    for $a (@asns)
    {
	for $b (@asns)
	{
	    if ($a == $b)
	    {
		next;
	    }
	    if (exists($as{$a}{$b}) || exists($as{$b}{$a}))
	    {
		next;
	    }
	    elsif($a < $b)
	    {
		$as{$a}{$b} = 0;
		$add++;
	    }
	}
    }
}
for $x (sort {$a <=> $b} keys %as)
{
    for $y (sort {$a <=> $b} keys %{$as{$x}})
    {
	print "$x $y " . $as{$x}{$y};
    }
}
open(my $oh, '>', "ixps.txt") or die "Could not open file ixps.txt $!";
for $i (keys %ixps)
{
    for $as (sort {$a <=> $b} keys %{$ixps{$i}})
    {
	print $oh "$i $as\n";
    }
}
