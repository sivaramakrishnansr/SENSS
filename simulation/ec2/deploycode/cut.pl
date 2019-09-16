$fh = new IO::File("out");
$start = 0;
while(<$fh>)
{
    if ($_ =~ /Victim 52893/)
    {
	last;
    }
    if ($_ =~ /Victim 49785/)
    {
	$start = 1;
    }
    if ($start == 0)
    {
	next;
    }
    print $_;
}
