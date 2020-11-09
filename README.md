# TAC

Course material for "Traitement automatique de corpus" (STIC-B545) taught at [ULB](https://ulb.be)

## Module 1 (rewritten scripts)

### s2_sparql.py

Get information about the Belgian Monarchy through an interactive menu.
Queries available data from [Wikidata](https://www.wikidata.org).

Usage:

`python module1/s2_sparql.py`

### s3_api.py

Query two datasets in the [Open Data Brussels](https://opendata.bruxelles.be/page/home/).

Usage:

`python module1/s3_api.py (population | bourgmestres)`

### s4_scrape.py

Scraping the AVB to retrieve 2833 PDF bulletins.

If the script breaks or is closed by the user, next run will only download missing files.

Usage:

`python module1/s4_scrape.py (download | check)`

## Module 2 (original scripts)

`s1_convert.sh`: bash script to convert PDFs to TXTs, move them to dedicated folder and aggregate them in single big text file

`s2_explore.py`: playing with various categories (city, year, decade, type...)

`s3_freq.py`: basic frenquency analysis, hapaxes, long words...

## Module 3 (rewritten scripts)

### Keyword extraction

#### s1_keyword.py

Extract French keywords in text files converted from PDFs (see [Module 2](#module-2-original-scripts)).

Searches, by default, bigrams or higher for the year 1955 (because we had to pick a year for the project). Optionally, other values can be picked through arguments.

Usage:

```
python module3/s1_keywords.py -h

usage: s1_keywords.py [-h] [--year YEAR] [--ngrams NGRAMS]

Extract keywords from AVB bulletins (in txt form).

optional arguments:
  -h, --help       show this help message and exit
  --year YEAR      Year to extract from (default: 1955, because we had to
                   chose one)
  --ngrams NGRAMS  N-grams or higher to research (default: bigrams or higher)
```

#### s2_wordcloud.sh

Generate a wordcloud for a given year (calling `filter.py` in the background).

Usage:

`./module3/s2_wordcloud.sh YEAR`

### Named-entity recognition

Perform named-entity recognition (NER) with SpaCy FR model.

Requirements:

Install SpaCy from requirements then run this command to download French model: `python -m spacy download fr_core_news_sm`

Usage:

```
python module3/s3_ner.py YYYY (year)
```

### Sentiment analysis

`s4_sentiment.py`: analyse positive/negative sentences with textblob

## Module 4 (original scripts)

`classification.py`: supervised classification of 20 newsgroups

`clustering.py`: unsupervised clustering with k-means

`sentence_tokenizer.py`: split big text into sentences

`model_builder.py`: train word2vec model on corpus

`model_explorer.py`: explore similarity between vectors

## Module 5 (original scripts)

`language_detection`: language identification with langid

`anonymization.py`: de-identification of data with Faker

## Module 6 (original scripts)

`extraction.py`: extract text from various file types

`htr.sh`: script for handwritten text recognition
