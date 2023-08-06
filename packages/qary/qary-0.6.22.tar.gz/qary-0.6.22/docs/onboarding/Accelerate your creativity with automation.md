If you want to have more brain cycles for fun, creative stuff, you can [automate the boring stuff](automatetheboringstuff.com).
Though you can't really call it a "cognitive assistant", it will definitely help you think better.
Automating the boring stuff was the secret to the rise of powerhouse startups like GitHub, GitLab, Puppet, and even Google (in the early days).
Wildly efficient companies can generate millions in profit per employee.
Companies that don't *get it* find themselves stuggling to exceed 100k of revenue per employee.

If you automate the drudgery, you will free up brain cycles for fun, creative stuff... like finding more things to automate.

At [Tangible AI](tangibleai.com), our simplest, most popular automation  has been the `workon` command. [John]([John May](https://gitlab.com/jmayjr/)), [Olesya](https://gitlab.com/ovbondarenko), and I use it every day.  And we share it with our interns as part of the onboarding process.

**Teaser**:  I've added a *mind hack* at the end of the post.  It works well with the `workon` command to rev up your creativity.

## `workon`

The [`virtualenvwrapper`](https://pypi.org/project/virtualenvwrapper/) python package includes a command called `workon`.
And others have created a package called, appropriately [`Workon`](https://pypi.org/project/Workon/)

But I use `conda` rather than `virtualenv` to organize my python environments.
So I wrote a hacky shell script to take care of this.

[John](https://gitlab.com/jmayjr) and I are working on a python version of this.
But don't hold your breath...
If it ain't broke, we probably won't fix it.

## Use case

Every time I open a new terminal, I find myself activating an environment and then switching to that directory.
Remembering the right environment name and directory path can be a problem.
I work on many different projects in a given day, and they change from day to day.

So I created a `workon` command that makes it easy for me to set up a project and come back to it later.
All `workon` does is find the paths to my conda environmnt and source code, for a particular project.
It offloads my brain from memorizing paths and names and spellings that aren't helping me be creative.
Plus it gets me started quickly.

Now, all I do is type "`workon qary`" and I'm off and running.

## Installation

Download the [bash shell script](https://gitlab.com/tangibleai/qary/-/raw/master/scripts/bash_functions.sh?inline=false).

```bash
wget https://gitlab.com/tangibleai/qary/-/raw/master/scripts/bash_functions.sh?inline=false
```

I put mine in my personal `~/bin/` directory where I keep all my automation scripts.
Then make sure that script is sourced as part of your bash login in `.bashrc` or `.bash_profile`:

```bash
mv bash_functions.sh ~/bin/
chmod +x bash_functions.sh
echo "source ~/bin/bash_functions.sh" >> ~/.bashrc
```

You may want to edit the `bash_functions.sh` script on [line 38](https://gitlab.com/tangibleai/qary/-/blob/master/scripts/bash_functions.sh#L38) to add paths where you keep your source code.
You might also want to add a `git status` command (or anything else you do a lot) below [line 55](https://gitlab.com/tangibleai/qary/-/blob/master/scripts/bash_functions.sh#L55).

That should do it!

Now, when you type `workon qary` it will get you all set up for some creative, productive coding on a chatbot to save the world.

## Mind hack

Sometimes when you `workon qary` you end up staring at a blank screen or IDE.
It's hard to know where to start.
So I do `git status` right after `workon`.
That way I can leave "easter eggs" each time you switch from one project to another.
Right before I switch to a new project I'll add a TODO comment to my code, or even start a new line of code within incomplete syntax as a *note to self*.

Professional authors (thank you [Grant Ingersol](https://www.linkedin.com/in/grantingersoll)) often use this trick to seed their brain with creative ideas and avoid writer's block.
A writer will finish the day with an unfinished sentence or the first line of a dialog.
It's like a note to your future self.
This can supercharge your creativity the next morning by reminding you where you left off.

So when I'm about to switch projects I'll add an unfinished line of code or TODO, but won't `git commit` it.
That way it shows up when I do git status.
If your past self forgot to do this, and `git status` is empty, you can just do a `git log --stat` to reorient yourself.
And if that still doesn't work, sometimes when you build your project, your linters will flag any broken lines of code from the previous session.

## Linting

You `lint` don't you?!!!
If not, I'll set you straight in a follow-up post.
Linters are a crucial bit of automation that all the strong developers I know of lean on heavily.
Thank you [Steven](https://stevenskoczen.com/) and [Aleck](https://www.linkedin.com/in/aleck-landgraf-1145799/) for indoctrinating me with this habit all those years ago.
[PEP8](https://www.python.org/dev/peps/pep-0008/) linting is mandatory for all interns and interns and employees at Tangible AI, as well as contributors to [`qary`](gitlab.com/tangibleai/qary).


