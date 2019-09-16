$fh = new IO::File($ARGV[0]);
while(<$fh>)
{
    if ($_ =~ /fixed/ || $_ =~ /polluted/)
    {
	print "$_";
    }
}
