# notepadplusplus_python_timestamp
Script for `Python Script` Plugin for `Notepad++` to add timestamps to files.
Adds creation timestamps to new notes automatically.
Can add creation timestamps to old unsaved notes retroactively.

# Install
I used `Python3` so you need the alpha version of `Python Script`.

If you want to use `Python Script 2.1` which uses `Python2.7` you need to rewrite the script to `Python 2.7`.

- install `Python Script` plugin (I use v3.0.25): https://github.com/bruderstein/PythonScript
- Notepad++ -> Plugins -> Python Script -> Configuration...
- Initialisation: `ATSTARTUP`*
- Notepad++ -> Plugins -> Python Script -> New script
- add timestamp.py ('`C:\Program Files\Notepad++\plugins\PythonScript\scripts\')

*`ATSTARTUP` is not reliable
so add the following line at the bottom of `C:\Program Files\Notepad++\plugins\PythonScript\scripts\startup.py`:
```
import timestamp
```

# Use
- `timestamp.add_now_to_new()` will automatically be called upon opening or creating a new note and will add a timestamp. If you remove it it will keep adding current timestamp upon reopening the tab unless the note is not empty or is saved
- `timestamp.add_creation()` will add a creation timestamp at the top of a currently opened, but never saved non empty note, unless the date is already added
- `timestamp.add_creation_to_all()` calls `timestamp.add_creation()` on all open tabs
- `timestamp.add_now()` inserts current timestamp at cursor location
