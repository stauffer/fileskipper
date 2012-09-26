Fileskipper
==============

fileskipper is a quick and simple file navigator/launcher. 

It's purpose is to display the related files in a project in one spot for quick launching, testing or editing.

Fileskipper will search for all files in the current working directory (including all subfolders) of the specified file type(s) and create launch buttons for them. Select how you wish to launch the file (i.e. python, php or a text editor), add any required system arguments and click the file's launch button. Tooltips for each launch button shows the filepath, size and last modified date. You can change the working directory or reload the files at any time.

Place fileskipper.py in the folder you are working in and run it; it will find all python files in that directory as well as in any subdirectories and build a grid of buttons. You can then open the file for editing or with Python. See 'Tips and tricks' below for an even better solution.

By default fileskipper looks for python and text files and launches with Python2.

Please enjoy and we hope you find fileskipper as handy as we do.


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
