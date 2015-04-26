#!/usr/bin/python

import shutil
import sys
import os
import errno
import fnmatch
import subprocess
import math
import datetime
from random import randint

# File extensions tuple supported for conversion
supportedExtensions = ('.mp3','.flac','.wma')

# Function populateFileList returns a list of all files who are a part
# of the supportedExtensions.
#
# @param FilePath srcPath - Path in which to search
# @param Tuple extensions - File extensions which will be added to the returning list
# @returns Array - Array contains path and file
def populateFileList(srcPath, extensions):
	allFiles = []
	for root, dirnames, filename in os.walk(srcPath):
		for f in filename:
			if f.endswith(extensions):
				allFiles.append(os.path.join(root, f))
	return allFiles

# Function copyOrConvert copys the file from srcPath to dstPath if MP3
# or does an ffmpeg conversion for other file types to destination.
# MP3 is encoded at 320kbps for conversions.
#
# @param FilePath srcPath - Source path and file
# @param FilePath dstPath - Destination path
def copyOrConvert(srcPath, dstPath):
	filePath, fileExtension = os.path.splitext(srcPath)
	fileName = os.path.basename(filePath)
	try:
		if fileExtension == '.mp3':
			shutil.copy2(srcPath, dstPath)
		else:
			subprocess.call(["ffmpeg", "-loglevel", "panic", "-nostats", "-y", "-i", srcPath, "-ab",  "320k",  "-map_metadata",  "0",  "-id3v2_version", "3", (dstPath + "/" + fileName + ".mp3")])
	except KeyboardInterrupt:
		print("\nExiting...")
		sys.exit(1)
	except:
		print("Exception, moving along..")

# Function randomCopy loops fileCount times, 
# preforms a random lookup on srcPathList and
# calls copyOrConvert.
#
# @param Array srcPathList - Array of paths and
#   files to be copied or converted
# @param FilePath dstPath - Destination path
# @param Int fileCount - How many files to copy
#   / convert
def randomCopy(srcPathList, dstPath, fileCount):
	startTime = datetime.datetime.now()
	for x in range(0, fileCount):
		sys.stdout.write("\rProgress: " + calcProgressBarStr(20, x, fileCount) + " ETA: " + calcEtaStr(startTime, x, fileCount))
		sys.stdout.flush()
		randIndex = randint(0, len(srcPathList)-1)
		copyOrConvert(srcPathList.pop(randIndex), dstPath)

	sys.stdout.write("\rProgress: " + calcProgressBarStr(20, x, fileCount) + " ETA: " + calcEtaStr(startTime, x, fileCount))
	sys.stdout.flush()

# Function calcEtaStr takes a start time, position
# in the list and the list size to determine 
# an ETA for completion as a String.
#
# @param DateTime startTime - The time to start counting from
# @param Int position - The position in the array being 
#   consumed
# @param Int total - The total size of the array being
#   consumed
# @returns - A String of time left for consuming  the
#   array
def calcEtaStr(startTime, position, total):
	if position == 0:
		return "???"
	else:
		elapsedTime = datetime.datetime.now() - startTime
		estimatedRemaining = elapsedTime * total / position
		estimatedTimeToComplete = estimatedRemaining - elapsedTime
		return estimatedTimeToComplete.__str__()

# Function calcProgressBarStr takes a bar size, position
# in the list and the list size to determine 
# a progress bar completion and percentage as a String.
#
# @param Int barSize - The size in hashmarks for the progress bar
# @param Int position - The position in the array being 
#   consumed
# @param Int total - The total size of the array being
#   consumed
# @returns - A String as a progress bar of hash marks and percentage to 
#	completion.  eg: "[##    ] 33%"
def calcProgressBarStr(barSize, position, total):
	percent = float(position) / total
	hashes = '#' * int(round(percent * barSize))
	spaces = ' ' * (barSize - len(hashes))
	return "[{0}] {1}%".format(hashes + spaces, int(round(percent * 100)))

# Function checkFFmpeg checks for the existance of the
# ffmpeg binary by calling it with the help flag.  The
# output is surpressed from the help command.  It will 
# then print a friendly message to the terminal.
def checkFFmpeg():
	try:
		f = open(os.devnull, "w")
		subprocess.check_call(['ffmpeg', '-h'], stdout=f, stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError:
		print("Problem executing ffmpeg, please check your system")
		sys.exit(1)
	except OSError:
		print("Please install ffmepg first: https://www.ffmpeg.org/download.html")
		sys.exit(1)

# Function printHelp prints the README.md to the terminal.
def printHelp():
	f = open('README.md', 'r')
	print f.read()
	f.close()

# Function printUsage prints the command usage to the
#   terminal.
def printUsage():
	print("Usage: randcopy.py [-h] srcDir dstDir numFiles")

# Function main takes command line arguments for performing
# the random copy.
def main(argv):
	if len(argv) != 4:
		if len(argv) == 2 and argv[1] == '-h':
			printHelp()
			sys.exit(0)
		else:
			printUsage()
			sys.exit(1)
	checkFFmpeg()
	filesSourcePath = argv[1]
	filesDestinationPath = argv[2]
	howManyFilesToCopy = int(argv[3])

	print("Source: " + str(filesSourcePath))
	print("Destination: " + str(filesDestinationPath))
	print("Number of files to copy: " + str(howManyFilesToCopy))

	print("Building source file list...")
	filesSourcePathList = populateFileList(filesSourcePath, supportedExtensions)
	print("Source file list complete; number of files collected = " + str(len(filesSourcePathList)))
	randomCopy(filesSourcePathList, filesDestinationPath, howManyFilesToCopy)
	print("\nCopy complete")

# Calls function main()
if __name__ == "__main__":
    main(sys.argv)
