#!/usr/bin/perl
my $I = $ENV{'ITER'};
my $L = 10 ** 5;
my $f = 3.1415926; 
for my $i (0..$I) { for my $j (0..$L*10) { $f = 4.00 * $f; } } 
