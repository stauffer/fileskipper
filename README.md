Fileskipper
==============

fileskipper is a quick file search/launcher.

Recently, while working on a project involving several different Python scripts, I had the need to quickly launch the different scripts either directly with Python or in an editor... and Fileskipper was born.

Place fileskipper.py in the folder you are working in and run it; it will find all python files in that directory as well as in any subdirectories and build a grid of buttons. You can then open the file for editing or with Python.

The default is to look for python scripts in the installed directory and build a table of executable buttons. By default Python2 is the executor but options for Python3, gedit, idle and sublime.

Things to remember:
* Written in and for Linux - any cross platform functionality is purely accidental (and I have no intention of building that in but am open to someone else doing that).
* Separate all file extensions with commas only.
* System arguments are basic; string will be split by spaces and passed to the program in quotes (i.e. python myscript.py 'arg1' 'arg2') 

Please feel free to give feedback.

Not all functions are complete... more to come.

Enjoy,

Jeff Stauffer





Tips and Tricks
------------

**Access fileskipper.py from anywhere in the file tree and avoid typing "python2 fileskipper.py" every time.**
Add the following to your `~/.bashrc` file (`~/.bash_profile` for Mac and Cygwin users):

<pre>
alias f='python2 /path/to/fileskipper.py'
</pre>

Run `source ~/.bashrc` to reload your changes.

Now you simply type `f` from anywhere in your file tree to open Fileskipper.