# notepadplusplus_python_timestamp
Script for `Python Script` Plugin for `Notepad++` to add timestamps to files.
Adds timestamps to new files automatically.
Can add timestamps to old unsaved files retroactively.

# install
I used `Python3` so you need the alpha version of `Python Script`.
If you want to use `Python Script 2.1` which uses `Python2.7` you need to rewrite the script to `Python 2.7`.

- install `Python Script` plugin (I use v3.0.25): https://github.com/bruderstein/PythonScript
- Notepad++ -> Plugins -> Python Script -> Configuration...
- initialisation: ATSTARTUP
- Notepad++ -> Plugins -> Python Script -> New script
- add timestamp.py

# issues
`ATSTARTUP` is not always reliable
in that case copy add_now to `startup.py`
