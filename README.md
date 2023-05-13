# lustre_bulk_migrate
Ostensibly this utility will take in a zstd compress list of files that need migrated and dispatch lfs_migrate jobs to migrate them.

I spent like 2 hours writing and troubleshooting this and then realized:
```shell
lfs find --ost <ost here> ... --ost <ostn here> --print0 <path> | xargs -0 -I "{}" -P 16 lfs_migrate -y -R --non-block {}
```
would be faster and do a better job. Looks like Unix wins again.

This utility does have a nice side effect of finding corrupted filenames from client crashes and such, so there's that.
