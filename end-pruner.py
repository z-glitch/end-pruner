#!/usr/bin/python3
# end-pruner
# Prune the End dimension in Minecraft, leaving a 1000x1000 central area in-tact.
# Created by glitch@glitchy.net
# Inspired by xisumavoid's tutorial at https://xisumavoid.com/pruneendchunks/

import sys
import argparse
import os
import re

def confirm(default='n'):
    input = sys.stdin.readline().strip().lower()
    if not input:
        input = default
    return input == 'y'

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('%s: error: %s\n' % (sys.argv[0], message))
        self.print_help()
        sys.exit(2)

class EndPruner(object):
    regionSuffixes = [
        ['world_the_end', 'DIM1', 'region'],
        ['DIM1', 'region'],
    ]

    regionFileRegex = re.compile(r'^r\.([-0-9]+)\.([-0-9]+)\.mca$')

    def __init__(self):
        self.dir = '.'
        self.quiet = False
        self.confirm = False
        self.dry_run = False

    def qprint(self, *args, **kwargs):
        if self.quiet:
            return
        print(*args, **kwargs)

    @staticmethod
    def shouldKeepCoords(x, z):
        return  x >= -3 and x <= 2 and z >= -3 and z <= 2

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
            x = int(m.group(1))
            z = int(m.group(2))
            if self.shouldKeepCoords(x, z):
                self.qprint('[ ] %s' % item)
                numFilesToKeep += 1
            else:
                self.qprint('[D] %s' % item)
                filesToRemove.append(fullitem)
        self.qprint('[ ] Keeping %d files' % numFilesToKeep)
        return filesToRemove

    def initFromCommandLine(self):
        parser = MyParser(description='end-pruner v0.2:  A tool to prune the end dimension in Minecraft')
        parser.add_argument('-y', action='store_true', help='Skip delete confirmation')
        parser.add_argument('-q', action='store_true', help='Quiet mode')
        parser.add_argument('--dry-run', action='store_true', help='Show files to be deleted, but do not actually delete them')
        parser.add_argument('server_dir', help='Minecraft server directory')
        args = parser.parse_args()

        self.dir = args.server_dir
        self.quiet = args.q
        self.confirm = args.y
        self.dry_run = args.dry_run

    def run(self):
        filesToRemove = self.getFilesToRemove(self.dir)
        if not filesToRemove:
            self.qprint('[ ] No files to prune.')
            return
        numToRemove = len(filesToRemove)
        self.qprint('[ ] Need to delete %d file%s' % (numToRemove, '' if numToRemove == 1 else 's'))
        if not self.confirm:
            print('[!] ARE YOU SURE YOU WANT TO DELETE THESE FILES?  (NO WAY TO UNDELETE) [y/N] ', end='')
            sys.stdout.flush()
            if not confirm():
                print('[!] Aborting')
                return
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
