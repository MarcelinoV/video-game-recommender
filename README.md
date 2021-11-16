# Content-based Video Game Recommender
Content-based video game recommender using Metacritic game review dataset.

A couple of weeks ago, I realized that the only type of analytics I haven't done yet from the four main types of analytics (descriptive, diagnostic, predictive, and prescriptive) was prescriptive analytics. After googling examplings of prescriptive analytics projects, I found that recommender systems are one of the most popular types of prescriptive analytic algorithms. So after reading more about recommender systems, I decided to do something I always wanted to do: Build a recommender system for video games.

With the help of a tutorial from DataCamp on Python Recommender Systems, I applied the ideas from there to build out my recommender system based on cosine similarity as the metric for finding games similar to an input.

## Code and Resources Used

**Python Version**: 3.8.10

**Packages**: requests, beautifulsoup, csv, pandas, numpy, string, re, nltk, sklearn

**Beginner Tutorial: Recommender Systems in Python**

https://www.datacamp.com/community/tutorials/recommender-systems-python

**Online Source of data accessed via Web Scraping**

https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?sort=desc

## Data Collection

### Web Scraping

Before finding my final dataset on Kaggle, I had decided to use a webscraper to collect my data from Metacritic.com's video game review section, ordered by Metascore, the score given by Metacritic to a video game.

For scraping, I decided I wanted 5 features for the data of interest: 

- title
- summary
- release date
- metascore
- userscore

Even though my recommender system would be content-based, thus only the summary feature would be used, I thought it would be interesting to collect these other pieces of data just in case I wanted to analyze further to learn more about the video games in the dataset. 

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/master/Images/web-scraper-snap.jpg "Key part of web-scraping code: lines 42-47 are html that contain desired features.")

This scraper would scrape the first 100 pages of metacritic's catalogue, yielding the original dataset of about 5000 rows, with around 3700 as unique records.

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/master/Images/scraped-data-snap.jpg "snapshot of scraped data")

### Final Kaggle Dataset

After implementing the first recommender system using this scraped data, I later discovered that I missed an already available dataset on Kaggle of the same data that I scraped from Metacritic but contained ALL of the games on the Metacritic review catalogue (about 180 pages or 18000 games). This dataset can be found here:

https://www.kaggle.com/deepcontractor/top-video-games-19952021-metacritic

## Data Cleaning and Processing

In the data wrangling phase, my cleaning strategy was straightforward:

1. Drop duplicate titles in the dataset.
2. Drop rows where the summary was null.
3. Use NLP techniques to create tokenized feature of summaries

The NLP techniques used consisted of converting words to lowercase, dropping stopwords and punctuation, and performing stemming and lemmatization on the tokenized texts.



Reading more into it, I learned that recommender systems work by using some sort of distance formula, whether it be Euclidean Distance, Cosine Similarity, Manhattan Distance or other such metrics. 
