# Your First Qary Skill

## Prerequisites

- Anaconda installed on your machine
- A linux-like terminal (Ubuntu, Mac, WSL, gitbash)
- command line basics: `cd`, `ls`, `cp`, `mv`, `mkdir` 
- git basics: `git clone`
- a gitlab account

## Getting Started

1. Visit gitlab.com/tangibleai/qary and hit the Fork button (upper right).
2. Select your user account as the destination for the Fork.
3. Remember you gitlab username or copy it from the your gitlab.com profile
4. Open a terminal and run the following commands (making sure to put in your username where appropriate):

```console
$ GITLAB_USERNAME=your_username_here
$ cd ~/code # or whever you keep your source code
$ git clone git@gitlab.com:$GITLAB_USERNAME/qary
$ cd qary
$ ls -al
```

You should now see an environment.yml and setup.py for qary. 
So now you can install the source code for qary from your fork.
And you'll install it in `--editable` mode so that whenever you make changes they'll immediately be available within `qary`.

```console
$ conda update -y -n base -c defaults conda
$ conda create -y -n qaryenv 'python>=3.6.5,<3.9'
$ conda env update -n qaryenv -f environment.yml
$ conda activate qaryenv || source activate qaryenv
$ pip install --editable .
```

Now you can play with qary by taking a short quiz using the quiz bot, if you like:

```console
$ qary -s quiz
Welcome to ...
...
Ready?
YOU: yes
```

## Creating your own Skill

Copy an existing skill withing `src/qary/skills` so you don't have to start with a blank page:

```console
$ cp src/qary/skills/quiz.py src/qary/skills/my_new_skill.py
```

Now open that my_new_skill.py file in your favorite editor.
You're _Sublime_ and _pyCharming_ aren't you ;)? 

Feel free to add any `import`s you need at the top of the `my_new_skill.py` file. 
And delete the `__init__():` method.
You won't need it where you're going.

Finally, delete everything within the `reply():` method except the return statement.
Now change it to return your first `qary` reply text:

```python
    def reply(statement, context=None):
        return [BotReply(
            confidence=1.0,
            text="This is my first simple new skill!!!"
            )]
```

Now you can run your skill from the command line with:

```console
$ qary -s my_new_skill

qary: This is my first simple new skill!!!

YOU: Hi!!!

qary: This is my first simple new skill!!!

YOU: exit
```

You can see that it's a pretty simply skill. 
Now it's your turn. 
Try adding some more replies to the list of BotReply objects. 
Play around with the confident value and see if you can figure our why it's chosing one reply over another.
Once you get bored with random conversation, start thinking about what kinds of statements you want your skill to be able to handle.
The text that the user types will be available in the `statement` argment to the reply function.
So to be an annopying echo bot you could do something like this:

```python
    def reply(statement, context=None):
        return [BotReply(
            confidence=1.0,
            text=statement
            )]
```

When you run qary with your new skill, you'll see that it's quite skillful and consistent at playing the echo game:

```console
$ qary -s my_new_skill

qary:

YOU: Hi!!!

qary: Hi!!!

YOU: What are you saying?

qary: What are you saying?

YOU: I know you are but what am I?

qary: I know you are but what am I?
```

Your turn... play around with some of the other skills that you see in the skills/ directory.

Some fun ones you might like are `qary -s eliza` or `qary -s qa`.
And if you really want to go crazy, you can combine a few of them:

```console
$ qary -s my_new_skill,faq,glossary,eliza
```

The `qa` skill requires a lot of resources.
So don't bother with it if you aren't feeling very patient.

