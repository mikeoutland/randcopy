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


supportedExtensions = ('.mp3','.flac','.wma')

def populateFileList(srcPath, extensions):
	allFiles = []
	for root, dirnames, filename in os.walk(srcPath):
		for f in filename:
			if f.endswith(extensions):
				allFiles.append(os.path.join(root, f))
	return allFiles

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

def randomCopy(srcPathList, dstPath, fileCount):
	startTime = datetime.datetime.now()
	for x in range(0, fileCount):
		percent = float(x) / fileCount
		hashes = '#' * int(round(percent * 20))
		spaces = ' ' * (20 - len(hashes))
		randIndex = randint(0, len(srcPathList)-1)
		sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))) + " ETA: " + calcEtaStr(startTime, x, fileCount))
		sys.stdout.flush()
		copyOrConvert(srcPathList.pop(randIndex), dstPath)

	sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes + spaces, 100) + " ETA: " + calcEtaStr(startTime, x, fileCount))
	sys.stdout.flush()

def calcEtaStr(startTime, position, total):
	if position == 0:
		return "???"
	else:
		elapsedTime = datetime.datetime.now() - startTime
		estimatedRemaining = elapsedTime * total / position
		estimatedTimeToComplete = estimatedRemaining - elapsedTime
		return estimatedTimeToComplete.__str__()

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

def printHelp():
	f = open('README.md', 'r')
	print f.read()
	f.close()

def printUsage():
	print("Usage: randcopy.py [-h] srcDir dstDir numFiles")


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

if __name__ == "__main__":
    main(sys.argv)
