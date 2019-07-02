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
command line options.

# Requirements
* Python3

# Usage
Before using, **BACK UP YOUR END DIMENSION DATA FILES!**  This script was written
with care, but mistakes do happen, and a backup is cheap insurance.  The End files
can be found in the `DIM1` directory (not to be confused with `DIM-1`, which contains
the Nether).
```
usage: end-pruner.py [-h] [--keep-range x1,z1,x2,z2] [-y] [-q] [--dry-run]
                     server_dir

end-pruner v0.3: A tool to prune the end dimension in Minecraft

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
  -y                    Skip delete confirmation
  -q                    Quiet mode
  --dry-run             Show files to be deleted, but do not actually delete
                        them
```

# Example
```
$ ./end-pruner.py ~minecraft/minecraft/servers/private.test/
[ ] Found region directory at /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region
[D] r.19.0.mca
[D] r.15.0.mca
[D] r.11.0.mca
[D] r.7.0.mca
[D] r.12.0.mca
[ ] r.-1.0.mca
[ ] r.0.0.mca
[D] r.18.0.mca
[ ] r.0.-1.mca
[D] r.8.0.mca
[ ] r.2.0.mca
[D] r.17.0.mca
[D] r.5.0.mca
[D] r.13.0.mca
[D] r.3.0.mca
[D] r.14.0.mca
[D] r.9.0.mca
[D] r.20.0.mca
[D] r.-20.0.mca
[D] r.16.0.mca
[D] r.10.0.mca
[D] r.6.0.mca
[ ] r.1.0.mca
[ ] r.-1.-1.mca
[D] r.4.0.mca
[ ] Keeping 6 files
[ ] Need to delete 19 files
[!] ARE YOU SURE YOU WANT TO DELETE THESE FILES?  (NO WAY TO UNDELETE) [y/N] y
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.19.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.15.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.11.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.7.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.12.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.18.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.8.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.17.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.5.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.13.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.3.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.14.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.9.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.20.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.-20.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.16.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.10.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.6.0.mca
[D] Deleting /home/minecraft/minecraft/servers/private.test/world_the_end/DIM1/region/r.4.0.mca
[ ] Done.
$
```
