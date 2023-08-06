## Sprint 2 Retrospective

- wikipedia titles, db setup, no titles or vectors yet, downloaded all wikipedia text
- 2 0.5.15-0.5.16 releases
- tests passing
- increased
- Raj got rouge1 and rougen working, BLEU
- Maria Slack glossary bot
- REST API endpoint
- tabot, dashboard app
- two dicts RandomForestClassifer F1 score (severe .24), precision good but recall bad LogisticRegression() & SGDClassifer()
- Olesya released a blog post on BERT and transformers and benchmarking
- Compared 5 models and tested them on QABot-like questions

## Sprint 3 Planning
- Olesya: submit post to towardsdatascience.org (medium channel)
- Hobson: finish loading titles and first 2 sentences and w2v vectors and BERT vectors, blog word vectors, take the hate out of hate speech
- Duncan: integrating MyCroft into qary using REST api at http://34.220.107.74/bot/ or api.qary.me/bot (if working)
- Mohamed: React, plus learning OpenEdX
- Rikeem and Mohammed are working on a DS Dashboard
- API for elastic search with highlights (snippets compatible with BERT context)
   - load an elastic search instance with all of wikipedia
   - index all of wikipedia with ES
   - expose ES API from separate container
   - connect api.qary.me REST API to ES.qary.me API
- Jake: fine tuning and analyzing features to identify features most correlated with anemi
   - draft final report
   - markdown text in jupyter notebooks
   - plots
   - blog post

## Sprint 4: Backlog
- Maria: qary Accuracy improvement: benchmark accuracy with our own testset and training set (https://gitlab.com/tangibleai/qary/-/issues/38)
- Fast connection to Wikipedia
