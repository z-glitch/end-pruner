# end-pruner
A tool to prune the End dimension in Minecraft.

# Background
The End dimension in Minecraft contains non-renewable resources like chests,
Elytra, and Shulker mobs (which drop Shulker Shells).  Once these are looted,
they're gone forever, and subsequent adventurers must travel further and further
away to find more.  This makes for a bad experience, especially for players
who are new to a shared server.

One way to address this scarcity is to delete the End dimension and allow the
game to regenerate it with fresh mobs and loot.  But, doing so will also
destroy any user-created structures in the End, which may be undesireable.

Inspired by the useful tutorial created by Xisuma (and available at
https://xisumavoid.com/pruneendchunks/ ), this script will preserve the region
files containing the central ~3000x3000 blocks of the End and delete everything
else.  You can also, if desired, specify other block ranges to preserve via
command line options or a config file.  As a courtesy, any players who logged
out while in the End will be relocated to their respective spawn points.

# Requirements
* Python3
* [The NBT Python library](https://pypi.org/project/NBT/) -- which you can get
by running `pip3 install nbt`


# Compatibility
* Known to work with Paper MC 1.14.3.

# Warning
Before using, **SHUT DOWN YOUR SERVER AND BACK UP YOUR FILES!**
This script deletes or modifies files in the following directories:
* `DIM1`, or `world_the_end/DIM1` for Bukkit servers.  (Not to be confused with
`DIM-1`, which contains the Nether.)
* `world/playerdata`

This script was written with care, but mistakes do happen, and a backup is
cheap insurance.

# Usage
```
usage: end-pruner.py [-h] [--keep-range x1,z1,x2,z2]
                     [--config-file CONFIG_FILE] [--dont-move-players] [-y]
                     [-q] [--dry-run]
                     server_dir

end-pruner v0.5: A tool to prune the End dimension in Minecraft

positional arguments:
  server_dir            Minecraft server directory

optional arguments:
  -h, --help            show this help message and exit
  --keep-range x1,z1,x2,z2
                        Range of blocks to keep, specified in world
                        coordinates. For example, 1000,1000,-1000,-1000 will
                        cover a 2000x2000 square centered on the origin.
                        Because blocks are aggregated into files by region,
                        the actual preserved area will often be a bit larger
                        than what is specified. This flag may be used multiple
                        times to keep several areas, and it's okay if those
                        areas overlap. The default range of
                        -1536,-1536,1535,1535 is always preserved.
  --config-file CONFIG_FILE
                        Load additional config from FILE. This file should
                        contain a list of block ranges to keep (in x1,z1,x2,z2
                        format), one per line. You may add comments if you
                        prefix them with the '#' character.
  --dont-move-players   Don't move players out of the End. (By default, any
                        players still in the End are sent back to their spawn
                        points.)
  -y                    Skip delete confirmation
  -q                    Quiet mode
  --dry-run             Show files to be deleted, but do not actually delete
                        them
```

# Examples
```
# Just testing -- no files modified.
$ ./end-pruner.py --dry-run YourServerDirectory

# Interactive use:
$ ./end-pruner.py YourServerDirectory

# Non-interactive use:
$ ./end-pruner.py -y YourServerDirectory

# Non-interactive use, with less output:
$ ./end-pruner.py -y -q YourServerDirectory
```
