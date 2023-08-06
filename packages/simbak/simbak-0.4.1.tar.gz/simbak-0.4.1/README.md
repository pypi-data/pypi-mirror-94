# Simbak

For a detailed outline of simbak, visit the 
[wiki](https://github.com/mark-bromell/simbak/wiki).

Simbak is a simple backup solution that is aimed towards individuals who
just want a quick and easy way to backup their files. Backups are stored
as `tar.gz` files, so there is no dependence on any application to
restore your backups.

# Benefits of simbak

- Simbak uses tar and gzip in order to store the backups, so that
recovering the data in backups does not depend on simbak itself.
- Simbak is also very light, portable, and very easy to use, meaning
that there's no large application to install.
- It's free and open source, meaning anyone can contribute or change
simbak to meet their own needs.

# Getting started

## Installation
To install simbak you can simply use
[pip](https://pypi.org/project/pip/).

```bash
$ pip install simbak
```

## Using simbak

### Terminal

You can use simbak in many ways, the fastest way would be to use the
`simbak` command in the terminal directly, this will perform a normal
backup, use `$ simbak --help` to see your options.

```bash
$ simbak [...]
```

You can also use the simbak module itself through the python executable.

```bash
$ python3 -m simbak [...]
```

### Python script

You can use simbak within your own python code, and you can make python
scripts to use simbak (a python script can be prettier than shell script).

```python
import simbak

# This will perform a normal backup.
simbak.backup(...)
```

### Example usages

Each of these examples will achieve the same reults. They will create a
backup of `/home/projects/my_project/` and `/home/docs/important.txt`
and it will store the backup in `/remote/backups` and `/local/backups`.
The backup will be a `tar.gz` file and it will have the name of
`important--YYYY-MM-DD--hh-mm-ss`, the time is stamped at the end of the
backup to ensure the file is unique and not conflicting with other
backups.

#### Python script example

```python
# backup.py

import simbak

simbak.backup(
    sources=[
        "/home/projects/my_project/",
        "/home/docs/important.txt",
    ],
    destinations=[
        "/local/backups/",
        "/remote/backups/",
    ],
    name="important"
)
```

You can then run this script through the terminal using
`$ python3 backup.py`.

#### Bash script example

**Note**: I am using a backslash at the end of each line in order to
have a command spread across multiple lines, this helps readability.

```bash
# backup.bash

simbak \
    --source \
        "/home/projects/my_project/" \
        "/home/docs/important.txt" \
    --destination \
        "/local/backups/" \
        "/remote/backups/" \
    --name "important"
```

#### Terminal example

Using simbak directly in the terminal isn't recommended unless you are
backing up one directory or file to one location for a one time occurrence,
as you can see the lines can get quite long.

```bash
$ simbak -s "/home/projects/my_project/" "/home/docs/important.txt" \
> -d "/local/backups/" "/remote/backups/" \
> --name "important"
```
