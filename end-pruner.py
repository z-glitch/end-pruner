#!/usr/bin/python
# end-pruner
# Prune the End dimension in Minecraft, leaving a 1000x1000 central area in-tact.
# Created by glitch@glitchy.net
# Inspired by xisumavoid's tutorial at https://xisumavoid.com/pruneendchunks/

import sys
import os
import re

def confirm(default='y'):
	input = sys.stdin.readline().strip().lower()
	if not input:
		input = default
	return input == 'y'

class EndPruner(object):
	regionFileRegex = re.compile(r'^r\.([-0-9]+)\.([-0-9]+)\.mca$')

	@staticmethod
	def shouldKeepCoords(x, z):
		return  x >= -3 and x <= 2 and z >= -3 and z <= 2

	def getFilesToRemove(self, serverDir):
		regionDir = os.path.join(serverDir, 'DIM1', 'region')
		if not os.path.exists(regionDir):
			print("Can't find region directory \"%s\"" % regionDir)
			return

		filesToRemove = []
		for item in os.listdir(regionDir):
			fullitem = os.path.join(regionDir, item)
			if not os.path.isfile(fullitem):
				continue
			m = self.regionFileRegex.search(item)
			if not m:
				continue
			x = int(m.group(1))
			z = int(m.group(2))
			if self.shouldKeepCoords(x, z):
				print('%s: keep' % item)
			else:
				print('%s: delete' % item)
				filesToRemove.append(fullitem)
		return filesToRemove

	def run(self, dir):
		filesToRemove = self.getFilesToRemove(dir)
		if not filesToRemove:
			print('No files to prune.')
			return
		numToRemove = len(filesToRemove)
		print('Delete %d file%s? [Y/n] ' % (numToRemove, '' if numToRemove == 1 else 's'))
		if confirm():
			for f in filesToRemove:
				print('Deleting %s' % f)
				os.remove(f)
		else:
			print('Aborting')
		print('Done.')

def main():
	if len(sys.argv) != 2:
		print('Usage:  %s <server directory>' % sys.argv[0])
		return
	pruner = EndPruner()
	pruner.run(sys.argv[1])

if __name__ == '__main__':
	main()
