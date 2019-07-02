#!/usr/bin/python3
# end-pruner
# Prune the End dimension in Minecraft, leaving specific areas in-tact.
# https://github.com/z-glitch/end-pruner

import sys
import argparse
import os
import re

def confirm(msg, default='n'):
    r = input(msg).strip().lower()
    if not r:
        r = default
    return r == 'y'

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('%s: error: %s\n' % (sys.argv[0], message))
        self.print_help()
        sys.exit(2)

class BBox(object):
    def __init__(self, x1, z1, x2, z2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.z1 = min(z1, z2)
        self.z2 = max(z1, z2)
    def contains(self, x, z):
        return x >= self.x1 and x <= self.x2 and z >= self.z1 and z <= self.z2

class BBoxList(object):
    def __init__(self):
        self.list = []
    def add(self, x1, z1, x2, z2):
        self.list.append(BBox(x1, z1, x2, z2))
    def contains(self, x, z):
        for bbox in self.list:
            if bbox.contains(x, z):
                return True
        return False

class EndPruner(object):
    regionSuffixes = [
        ['world_the_end', 'DIM1', 'region'],
        ['DIM1', 'region'],
    ]

    regionFileRegex = re.compile(r'^r\.([-0-9]+)\.([-0-9]+)\.mca$')
    coordsRegex = re.compile(r'^([-0-9]+),([-0-9]+),([-0-9]+),([-0-9]+)$')
    defaultKeepRange = '-1536,-1536,1535,1535'

    def __init__(self):
        self.dir = '.'
        self.quiet = False
        self.autoConfirm = False
        self.dry_run = False
        self.keepRanges = BBoxList()

    def qprint(self, *args, **kwargs):
        if self.quiet:
            return
        print(*args, **kwargs)

    @staticmethod
    def worldCoordsToRegionCoords(x, z):
        return x>>9, z>>9

    def getRegionDir(self, serverDir):
        for suffix in self.regionSuffixes:
            regionDir = os.path.join(*([serverDir] + suffix))
            if os.path.exists(regionDir):
                self.qprint("[ ] Found region directory at %s" % regionDir)
                return regionDir
            self.qprint('[ ] No region directory found at %s' % regionDir)
        self.qprint("[!] Can't find region directory")

    def getFilesToRemove(self, serverDir):
        regionDir = self.getRegionDir(serverDir)
        if not regionDir:
            return

        filesToRemove = []
        numFilesToKeep = 0
        for item in os.listdir(regionDir):
            fullitem = os.path.join(regionDir, item)
            if not os.path.isfile(fullitem):
                continue
            m = self.regionFileRegex.search(item)
            if not m:
                continue
            if self.keepRanges.contains(int(m.group(1)), int(m.group(2))):
                self.qprint('[ ] %s' % item)
                numFilesToKeep += 1
            else:
                self.qprint('[D] %s' % item)
                filesToRemove.append(fullitem)
        self.qprint('[ ] Keeping %d files' % numFilesToKeep)
        return filesToRemove

    @classmethod
    def convertRangeCoords(cls, s):
        m = cls.coordsRegex.search(s)
        if not m:
            raise Exception('Error: Invalid coordinate syntax: %s\nExpected x1,z1,x2,z2 (e.g. -1000,-1000,1000,1000)' % s)
        r = []
        for i in range(1,5):
            r.append(int(m.group(i)) >> 9)
        return r

    def initFromCommandLine(self):
        parser = MyParser(description='end-pruner v0.3:  A tool to prune the end dimension in Minecraft')
        parser.add_argument('--keep-range', action='append', metavar='x1,z1,x2,z2',
            help='Range of blocks to keep, specified in world coordinates.  '
                'For example, 1000,1000,-1000,-1000 will cover a 2000x2000 square centered on the origin.  '
                'Because blocks are aggregated into files by region, the actual preserved area will often be '
                'a bit larger than what is specified.  This flag may be used multiple times to keep several areas, '
                'and it\'s okay if those areas overlap.  The default range of %s is always preserved.'
                % self.defaultKeepRange)
        parser.add_argument('-y', action='store_true', help='Skip delete confirmation')
        parser.add_argument('-q', action='store_true', help='Quiet mode')
        parser.add_argument('--dry-run', action='store_true', help='Show files to be deleted, but do not actually delete them')
        parser.add_argument('server_dir', help='Minecraft server directory')
        args = parser.parse_args()

        # Set keep ranges
        if args.keep_range is None:
            args.keep_range = []
        self.qprint('Preserving %s by default' % self.defaultKeepRange)
        args.keep_range.append(self.defaultKeepRange)
        for wr in args.keep_range:
            rr = self.convertRangeCoords(wr)
            self.keepRanges.add(*rr)

        # Set other options
        self.dir = args.server_dir
        self.quiet = args.q
        self.autoConfirm = args.y
        self.dry_run = args.dry_run

    def run(self):
        # Get list of files to remove
        filesToRemove = self.getFilesToRemove(self.dir)
        if not filesToRemove:
            self.qprint('[ ] No files to prune.')
            return
        numToRemove = len(filesToRemove)
        self.qprint('[ ] Need to delete %d file%s' % (numToRemove, '' if numToRemove == 1 else 's'))
        # Get user confirmation if required
        if not self.autoConfirm:
            if not confirm('[!] ARE YOU SURE YOU WANT TO DELETE THESE FILES?  (NO WAY TO UNDELETE) [y/N] '):
                print('[!] Aborting')
                return
        # Remove the files
        for f in filesToRemove:
            if self.dry_run:
                self.qprint('[D] Dry run: would have deleted %s' % f)
            else:
                self.qprint('[D] Deleting %s' % f)
                os.remove(f)
        self.qprint('[ ] Done.')

def main():
    pruner = EndPruner()
    pruner.initFromCommandLine()
    pruner.run()

if __name__ == '__main__':
    main()
