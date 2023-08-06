## 2020-12-23 End of 2020 Sprint (Tanbot)

### good

- django videos on youtube
- django learning
- a lot more attendance at the meeting

### bad

- tanbot not connected to slack
- qary not understood by interns
- qary broken on my branch
- qary error messages despite tests passing
- bad README documentation

### improve

- better first-time tickets
- more outreach at Python user group
- announce at each Saturday study group
- announce at monthly PUG meetup
- more promotion on slack
- move tanbot requirements to tanbot repo

## Jose Tickets (81 pt estimate)

1. 1 pt.: User can launch an empty do-nothing quest bot without error using `qary -s quest`
2. 8 pt.: When user launches qary quest skill they are presented with a welcome message describing the Cat Lady Puzzle.
3. 16 pt (task should be split?): When user launches a qary quest skill they get the welcome message and then can reply with a question that is stored in a list of dictionaries or other log of thier interactions (preferably in the `context` attribute of the `quest.Skill` class)
4. 16 pt (split task up?): When user gets an answer to their questions, one of either yes, no, or irrelevant. yes or no happen whenever the user's  questions are an exact match for a question in the script. irrelevant if they are not.
5. 16 pt: Smarter selection of the bot's answers of "yes", "no", or "irrelevant" are a little smarter, using spacy document vectors to find the best match for the user statement. The skills.faq skill does this to find the best match in the FAQ yaml files
6. 8 pt: Bot offers hints whenever an irrelevant question is asked.
7. 8 pt: Bot offers hints whenever more than 1 irrelevant question is asked in a row.
8. 8 pt: Bot offers a hint whenever the same question is matched in the database twice in a row (because the user asked a very similar question twice)

## John Tickets (100 pt)

0. deploy django web app to digital ocean according to the tutorial video
1. user can see messages that have been sent to them in a view
2. user can enter their reply to the latest message in a django form at the bottom of the list of previous messages (from themselves and the bot)

## Billy (100 pt)

1. create a working app based on the django tutorial on Youtube
2. help John with one of his tickets
3. help Jose with one of his tickets

## Hobson (32 pt)

1. Add a REST API to John's django app

## Raj (64 pt)

1. Web app that can display statistics from Kandarp dataset for India Family Health survey
