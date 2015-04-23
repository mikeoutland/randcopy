#!/usr/bin/python

import shutil
import sys
import os
import errno
import fnmatch
import subprocess
from random import randint

supportedExtensions = ('.mp3')

def populateFileList(srcPath, extensions):
	allFiles = []
	for root, dirnames, filename in os.walk(srcPath):
		for f in filename:
			if f.endswith(extensions):
				allFiles.append(os.path.join(root, f))
	return allFiles

def copyMp3(srcPath, dstPath):
	filePath, fileExtension = os.path.splitext(srcPath)
	fileName = os.path.basename(filePath)
	shutil.copy2(srcPath, dstPath)

def randomCopy(srcPathList, dstPath, fileCount):
	for x in range(0, fileCount):
		randIndex = randint(0, len(srcPathList)-1)
		copyMp3(srcPathList.pop(randIndex), dstPath)


def main(argv):
	if len(argv) != 4:
		print("Usage: randcopy.py srcDir dstDir numFiles")
		sys.exit(1)

	filesSourcePath = argv[1]
	filesDestinationPath = argv[2]
	howManyFilesToCopy = int(argv[3])

	print("Source: " + str(filesSourcePath))
	print("Destination: " + str(filesDestinationPath))
	print("Count: " + str(howManyFilesToCopy))

	print("Building src file list...")
	filesSourcePathList = populateFileList(filesSourcePath, supportedExtensions)
	print("Src file list complete; number of files = " + str(len(filesSourcePathList)))
	print("Start copy to dest...")
	randomCopy(filesSourcePathList, filesDestinationPath, howManyFilesToCopy)
	print("\nCopy complete")

if __name__ == "__main__":
    main(sys.argv)
