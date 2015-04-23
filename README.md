RANDCOPY
========

Randcopy was created by Mike Outland at https://github.com/mikeoutland-nexusis/randcopy

Randcopy is a utility to randomly copy music from a large local datastore to another local datastore.
A typical use case might be to generate a random collection of music on a USB thumb drive.

REQUIREMENTS
============

1. Python 2.7.x

2. ffmpeg (compatible with .flac and .wma)

QUICK START
===========

python randcopy.py /Volumes/MUSIC/MP3s /Volumes/USBSTICK 2500

Randcopy takes 3 parameters:
	1.  Source directory:
		This is a source directory that must be visible from the command line where music to be copied is located. Randcopy will automatically traverse sub directories.
	2.  Destination directory:
		This is a directory that must be visible from the command line where muisc will be copied and converted to. All files will retain their ID3 tags but will NOT retain source directory structure.
	3.  Number of files to copy:
		This is the number of files you wish  to copy or convert from the source to the destination.