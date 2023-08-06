# Sprint 4 Retro 

## Process ideas

* Hobson: start recording wed night meetings, especially during coding sessions
* Maria: pinning the goals doc in Slack and elsewhere
* All: Link goals in this file to issues in gitlab by adding issue link to this file

## Tech progress

Looking back to progress and goals for September:

1. Log for speed an accuracy every time we push to Master
    * Elastic Cloud server accessible by web interface
    * TBD: Elastic Cloud server api accessible from python module in qary
    * TBD: should record what the CPU and RAM details
    * TBD: Stretch goal: should record what the CPU and RAM details are
2. Ability to upload a text document qary index "file path or URL", and will incorporate it into text_qa bot
3. Create the infrastructure On the conversation_planner level
    * add an action e.g. "qary play music"
    * command line option -a playmusic
4. Spelling corrector feature to the existing qa_bot pipeline
    * big.txt spelling corrector function
    * TBD: big.json loader and preprocessing functions
    * TBD: `pattern_bots.py` -> `spelling_bots.py` that echos statement with corrected spelling
    * TBD: incorporate spell corrector into a `qa_bots.py` -> `corrected_qa_bots.py`
    * TBD: wikititles.json loader and preprocessing functions
    * TBD: spell checking functions that is configurable with big.json or wikititles.json
    * TBD: spell checking functions that is configurable with big.json or wikititles.json or both

    - Stretch goal: incorporating it into the spacy model.
5. Skills refactor
    - 

# Sprint 5 Planning (October)

## Goals

* Hobson: Promote wednesday night meetings to attract contributors
- Hobson: Elastic Cloud server api accessible from python module in qary
- Hobson: should record what the CPU and RAM details
- Hobson: Stretch goal: should record what the CPU and RAM details are
* Hobson: Finish bots->skills refactor
* Hobson: Finish accuracy metric upload to elastic search
* Mohammed: Move `http://api.qary.me/bots/` to `http://api.qary.ai` using existing `qary` to answer questions
* Mohammed: Put api.qary.ai on Google cloud
* Mohammed: SSL certs for `https://api.qary.ai` so that it no longer requires browser interaction 
* Mohammed: `https://qary.ai` web form that uses `api.qary.ai` to answer questions
* Hobson: When questions aren't answer, reply gracefully to user with something like "I don't know" instead of 404
* Hobson: qary informs user in conversation where the answer was found
* Olesya/Hobson: Connect `qary/skills/qa` to ElasticCloud rather than always using `scrape_wikipedia.py`
* Hobson: Create `intake` command that takes the url to a Wikipedia page 
  *  Hobson: only searches in that article, and falls back to general wikipedia ("Can't find answer in your page, but found it here:" )
  *  Hobson: give the user to control over their personal repository of urls (file-system CDL commands `delete`, `list`)
* Hobson: A regression testset on 1 article
* Hobson: intake command accepts a wikipedia title
* John: Spelling corrector feature to the existing qa_bot pipeline
  * John: big.json loader and preprocessing functions
  * John: `pattern_bots.py` -> `spelling_bots.py` that echos statement with corrected spelling
  * John: incorporate spell corrector into a `qa_bots.py` -> `corrected_qa_bots.py`
  * Stretch: wikititles.json loader and preprocessing functions
  * Stretch: spell checking functions that is configurable with big.json or wikititles.json
  * Stretch: spell checking functions that is configurable with big.json or wikititles.json or both

## Stretch

* hobson/mohammed: Torchserver for BERT and other transformers to speed up QA
* hobson: `intake` command accepts URL to any human-readable text 
* hobson: `intake` command accepts URL to any human-readable HTML