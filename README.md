# lustre_bulk_migrate
I spent like 2 hours writing and troubleshooting this and then realized:
```shell
lfs find --ost <ost here> ... --ost <ostn here> --print0 <path> | xargs -0 -I "{}" -P 16 lfs_migrate -y -R --non-block {}
```
would be faster and do a better job. Looks like Unix wins again.
