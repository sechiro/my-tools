#!/usr/bin/perl -w

use strict;
use warnings;
use Getopt::Long;
use File::Basename;

my $outputdir='/video-archive/';
my $tsname = '';
my $tslist = '';

GetOptions(
	'outputdir=s'	=> \$outputdir,
	'tsname=s'	=> \$tsname,
	'tslist=s'	=> \$tslist,
);

my @tslist;
unless ($tslist eq ''){
	open TSLIST, "<$tslist";
	while(<TSLIST>){
		chomp;
		push (@tslist, $_);
	}
}
push (@tslist, $tsname) unless($tsname eq '');

die "No file!" unless(@tslist);

# const.
my $CPU_CORES = 2;#`/usr/bin/getconf _NPROCESSORS_ONLN`;	
chomp $CPU_CORES;
my $X264_HIGH_HDTV=" -f mp4 -vcodec libx264 " 
    ."-fpre /home/sechiro/ts_encode/libx264-hq-ts.ffpreset "
    ."-r 30000/1001 -aspect 16:9 -s 1280x720 -bufsize 20000k -maxrate 25000k "
    ."-acodec libfaac -ac 2 -ar 48000 -ab 128k -threads $CPU_CORES";

foreach(@tslist){
	my $basename = basename($_, '.ts');

	system "/usr/bin/ffmpeg -y -i $_ $X264_HIGH_HDTV $outputdir$basename.mp4";
	#print "ffmpeg"."-y"."-i"."$_"."$X264_HIGH_HDTV"." $outputdir$basename.mp4";
}

exit;
