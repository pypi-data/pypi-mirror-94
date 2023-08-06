# Software Development Workflow

## Settuing up `git`

1. Install git (or Anaconda, which includes it)
2. `git config --global user.name "<Your Name>"`
3. `git config --global user.email "<you@example.com>"`
4. `ssh-keygen`  # hit enter at all prompts
5. `cat ~/.ssh/id_rsa.pub`  # copy the text from this file that appears
6. Visit your gitlab profile page
7. Click on Settings
8. Find the SSH & GPG Keys keys on the left panel and click on it
9. Paste the ssh key in the **large** text box
10. click the submit button  # this will allow you to clone & push without a password

## Contributing

When you contribute to a new project your goal is to not interfere with the project's workflow.

1. visit the gitlab page with the repository you'd like to contribute to
2. click the [fork] button next to the star button
3. choose your own account to copy the repository into your account
4. `git clone git@gitlab.com:<your_gitlab_account_name>/<repository_name>`  # example: git@gitlab.com:hobs/qary
2. `git checkout -b feature-<your-branch-name>`
2. `git push -u origin

3. # create a docstring first, before you add or modify any code
4. `git commit -am "<"


## Starting

To start a new project from scratch you can use `pyscaffold` to give you:

1. A best-practice directory tree
2. A working `setup.py` file
3. Example tests that will pass
4. Example docstrings
5. Example command-line app skeleton

## `git`

At least once a day I do the following.
The more often I do it, the more productive I am, because it forces me to be intentional about each new thing I do.

1. `git status` # check for files that need to be added
2. `git add <new file path>`  # only if necessary
3. `git commit -am "<message about what changed>"`
4. `git push`  # push to the default remote
5. `git push` <remote-name> master  # <remote-name> is usually `upstream` for me when I'm working with someone else's code
6. `git status`  # check if everything is up to date or if I need to add anything to .gitignore
