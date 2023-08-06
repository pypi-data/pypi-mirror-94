# Code Reviews

## Process

1. Developer creates a branch for their feature. 
2. Developer initiates a merge request (MR) marking it with the prefix "WIP:" in the title of the MR
3. Developer finishes developing the feature pushing often until tests are passing
4. Devloper deletes the "WIP:" prefix from the MR title, and adds a reviewer to the MR (anyone on the team)
4. Reviewer adds comments (see Mozilla Best Pratices below)
5. Reviewer approves the MR, conditionally approves it, or denies it
6. Developer makes sure tests pass (locally and on gitlab-ci) and coverage is not reduced (codecov.io)
7. Developer merges the MR to master and deletes the merged feature branch (locally and on gitlab)

## Mozilla Best Practice

Erik Rose (Mozilla)[^1] gave 3 possible goals and results for code review. I expanded it to 4.

### Goals
1. help improve code
2. spread competence/education
3. spread the love of the craft of programming
4. build yourself up, your confidence and emotional wellbeing

### Anti-goals
1. nitpicking
2. spread bad ideas, antipatterns
3. spread bad will, resentment, imposter syndrome
4. burn yourself out, draining your energy, reducing productive time

### Do
- paste code snippets
- clear language-neutral comments (consider ESL or stressed out colleagues)
- merge it!
    - if the code makes master better
- don't merge it!
    - security issues
    - correctness issues
    - significant efficiency reduction
    - test coverage reduction
    - the tiny typo fixes you're sugesting would be easier than filing a bug issue on the merged code

## Examples:

### [Bad, Why], [Good, Why]:

```yaml
- socratic:
    -
        - "There's no point returning path results when there is more than one term."
        - "Bad assumption. Assumes the otehr person didn't know something. "
    -
        - "Can you remind me of some use cases for returning path results when there is more than one term (but only one text term, of course)?"
        - "Explicit. Nonconfrontational. Asks question to spark thinking (Socratic method)"
- we:
    -
        - "If you do it this way, you'll break [Unicode queries|for use cases like x|version x|python 2|compatability with x].s [|you idiot]."
        - "Use of **you** is Confrontational. Finger-pointing."
    -
        - "If **we** do it this way we'll break [Unicode queries|for use cases like x|version x|python 2|compatability with x][|, I think]."
        - "Show that you're in this together and you've thought about it a bit, and would actually consider doing it the other person's way. More textbooky, factual."
- complement topping:
    -
        -
            - "That oughta do."
            - "flippant"
        -
            - "Really looking forward to [having|getting|incorporating][this|your code][|merged|in place]; I know [a lot|most|some|ton|many] of our users [need|want|would like] to [do x]. let me take a look."
            - "complement before you look at the code to get yourself and the reader in the right frame of mind."
- complement closer (sandwich):
        -
            - "Needs some work."
            - not complementary
        -
            - "Thank you for refactoring this [scary|difficult|challenging|complicated|spaghetti] mess [|that I created]."
            - Explain what you liked about the code that you read after you've reviewed it. complement them on their skill at dealing with something complex/difficult.
-
        -
            - "Obvious off-by-one error at the end of the list."
            - "belittling of the work and the coder"
        -
            - "I think this would be off-by-one at the end of the list."
            - "Humility. Open to feedback"
```

[^1]: https://www.youtube.com/watch?v=iNG1a--SIlk
