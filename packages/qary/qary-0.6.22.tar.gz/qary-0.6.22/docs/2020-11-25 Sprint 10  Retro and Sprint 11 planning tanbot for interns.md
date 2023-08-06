# 2020-11-25 Sprint 10 (Oct) Retro and Sprint 11 (Nov) planning

## What happened

- John: loved fast pace
- Hobson: unable to fix bugs that blocked feature web api for qary
- Hobson: bad to merge browse feature with elastic-cache
- Hobson: tests pass on feature-elastic-cache (with merged browser feature) only if env vars are not set for ElasticSearch tokens

## Ideas for Improvement

- Hobson: work on sprint features/bug fixes first
- Hobson: work on small feature/bugfix branches and merge to master often
- Move all large data files to digital ocean
- gitignore dynamic data files like accuracy reports

## Plan: User (Maria) needs web API to record intern interactions with content

New Django webapp deployed on digital ocean droplet to be the brain of the Intern chatbot

- Tabot
- Tangibot
- Tangible Bot
- Tan Bot
- Tanbot
- Tan
- Tanny
- Tanh

### Maria API

0. John: Create repo "tanbot"
0. Markdown content as yml one entry (links, text) per day that Eddy was intended to send out
1. `models.py` for storing all messages/content that tabbot will say on Slack
- ContentModel: title, text, urls (many2many n ForeignKey field for urls)
- UrlModel: title (str), url (str), media_type (str)
2. Maria's Slackbot middleware can query the Tanbot API for content based on day number (1-30)
- {text: "Hi have you reviewed the qary docs", title: how to use gitlab, links: [http://tan.do.spaces/john-install-qary-tutorial.mp4, http://docs.qary.ai, ...]}
3. models.py for user log
- User: pk/id (int), slack_username, slack_id
- History: foreign key to User, datetimestamp, content foreign key
4. Webapp needs to reach out to Slackbot middleware whenever interns need reminders (based on time since last interaction)
- {user: 123, text_message: 'proactively reminding you of ...'} or "{}"



## Backlog Features

- convert json.gz > html and upload html to digital ocean
- HL: fix qary/feature-elastic-cache
- deploy qary api that can answer FAQ skill questions
- deploy qary api that cna answer glossary skill questions
- HL: deploy qary api that can answer qa skill questions (open domain)




