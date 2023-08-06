# Windows Install

If you encounter errors installing qary within Anaconda on Windows these notes may help.

## FAQ

### conda: command not found

If you are using Git Bash on Windows and encounter the following error:

```
bash: conda: command not found
```

You probably need to run `conda init` inside the Anaconda Prompt **as administrator**:

```bash
conda init bash
```

### `torch` version

If during `conda env update -n qaryenv -f environment.yml` you encounter the following error:

```
Pip subprocess error:
ERROR: Could not find a version that satisfies the requirement torch<2.0.0,>=1.5.0
```

You probably need to install the correct version of torch within your `qaryenv` environment:

```bash
conda activate qaryenv
pip install torch==1.5.0+cpu torchvision==0.6.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
conda env update -n qaryenv -f environment.yml
pip install --editable .
```

### Access denied (putup.exe)

If you encounter the following error:

```
Pip subprocess error:
ERROR: Could not install packages due to an EnvironmentError: [WinError 5] Access is denied: 'C:\\Users\\Username\\AppData\\Local\\Temp\\pip-uninstall-pni9ktu_\\putup.exe'
Consider using the `--user` option or check the permissions.
```

Delete the `pip-uninstall-*` folder (or folders, if there is more then one) manually from the Temp directory:

#### In **`jupyter notebook`** or **`ipython`**
```python
! rm -rf ~/AppData/Local/Temp/pip-uninstall*
```

### Install pytorch or torch

If you encounter an error while installing pytorch or torch try installing from a wheel on github:

#### In **`jupyter notebook`** or **`ipython`**
```bash
! pip install torch==1.5.0 -f https://download.pytorch.org/whl/torch_stable.html
```

You can delete the pip-uninstall folder (or folders, if there is more then one) manually from the Temp directory.
Alternatively bypass this error by running `conda env update -n qaryenv -f environment.yml` in Git-Bash or Anaconda Prompt.


### Git Bash not installed

Any bash command can be run within ipython or jupyter ntoebook using the '!' prefix.

The "`!`" prefix tells the ipython interpreter to run the command in a bash shell rather than python.

Try the following to get up to speed on the powerful open standard for shell commands called **POSIX**:

```bash
! ls -al
! more README.md
! cd qary
! ls | grep qary
! find . -name qary
```

### Switch to Linux

Any operating system that allows you to directly use the linux operating system for your everyday work would be a huge step up in your productivity.

And you'd be supporting open source and the community of developers that keep the world internet servers running like clockwork.
The world's server work as well as they do because they don't use Windows or any other proprietary OS.
Harness this power for yourself.

