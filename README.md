# Content-based Video Game Recommender

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/national-video-games-day.jpg "Source: gamerant.com")

A couple of weeks ago, I realized that the only type of analytics I haven't done yet from the four main types of analytics (descriptive, diagnostic, predictive, and prescriptive) was prescriptive analytics. After googling examples of prescriptive analytics projects, I found that recommender systems are one of the most popular types of prescriptive analytic algorithms. So after reading more about recommender systems, I decided to do something I always wanted to do: Build a recommender system for video games.

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

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/web-scraper-snap.JPG "Key part of web-scraping code: lines 42-47 are html that contain desired features.")

This scraper would scrape the first 100 pages of metacritic's catalogue, yielding the original dataset of about 5000 rows, with around 3700 as unique records.

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/scraped-data-snap.JPG "snapshot of scraped data")

### Final Kaggle Dataset

After implementing the first recommender system using this scraped data, I later discovered that I missed an already available dataset on Kaggle of the same data that I scraped from Metacritic but contained ALL of the games on the Metacritic review catalogue (about 180 pages or 18000 games). This dataset can be found here:

https://www.kaggle.com/deepcontractor/top-video-games-19952021-metacritic

## Data Cleaning and Processing

In the data wrangling phase, my cleaning strategy was straightforward:

1. Drop duplicate titles in the dataset
2. Drop rows where the summary was null
3. Use NLP techniques to create tokenized feature of summaries

The NLP techniques used consisted of converting words to lowercase, dropping stopwords and punctuation, and performing stemming and lemmatization on the tokenized texts.

From reading more into recommender systems, I learned that they work by using some sort of distance formula, whether it be Euclidean Distance, Cosine Similarity, Manhattan Distance or other such metrics. Sticking with the DataCamp resource, I compute the pairwise cosine similarity scores for all unique video games based on their summaries, recommending games based on that similarity score threshold.

To do this, more NLP knowledge is needed to convert the raw text data into numerical form. Bag of Words is an option, but we use TF-IDF, or Term Frequency-Inverse Document Frequency vectorization to generate vector representations of the summaries.

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/tfidf-formula.JPG "TFIDF formula- Source: Wikipedia")

For a recap, the TF-IDF score of a video game summary is the frequency of a word occuring in that summary, down-weighted by the number of documents, or summaries, in which a word occurs. This reduces the importance of words common in video game summaries and thus minimizes their effect in computing a similarity score.

Using the `TfIdfVectorizer` from scikit-learn, we fit and tranform the tokenized summary data to get a TF-IDF matrix to compute the cosine similarity scores using `linear_kernel`, also from scikit-learn.

## Building the Recommender

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/cosine-formula.JPG "Cosine Similarity formula- Source: DataCamp")

The formula is calculated as so, where we get the dot product between each vector within the TF-IDF matrix to get the cosine similarity score. This outputs our cosine similarity matrix where each row is a video game with *n* columns, n being the number of unique rows in our original dataset. Using the kaggle dataset, this outputted a **12153x12153** matrix.

To create the recommender system, we define a function that takes a video game title as input and outputs the 10 most similar video games. This requires several steps:

- Create a reverse mapping of video game titles to their dataframe indices
- Define function to get index of video game given its title
- Use that index to get a list of cosine similarity scores for the inputted video game with all video games
- Convert list to tuple where first element is position and second is similarity score
- Sort by similarity score
- Return 10 most similar video games using index position via reverse mapping

The result is a content/summary-based video game recommender that returns expected results:

### GTA 5

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/example-1.JPG "First example")

### Super Mario Galaxy

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/example-2.JPG "Second example")

### Halo 2

![alt text](https://github.com/MarcelinoV/video-game-recommender/blob/main/Images/example-3.JPG "Third example")

## Future Works & Production Ideas

### Improvements

The recommender can be improved to output games more similar to inputs than our current recommender by **acquiring more or better data**, better data meaning records that include a video game's producer, main character, genre, and other key details that go into recommending a video game based on an input.

Since these features are absent in our current data, another worthwhile avenue of improvement would be unsupervised machine learning, most likely via clustering. By doing this we could find underlying patterns in the data and generate features out of patterns. This will most likely be my plan for improving this recommender.

### Future Projects

In terms of accessibility and utility, I plan on implementing a web application for the recommender so that it can be a usable data science project rather than another repo on github. Such a project would further my learning how how to productionize models as well.

After this experience, I hope to apply and improve upon the same methods used here to try my hand at building a **Pokemon Recommender**. Such an engine would ideally be able to recommend not just similar Pokemon to an input, but also Pokemon that are best suited to defeat the inputted Pokemon. I have some ideas on implementing this, and look forward to experimenting.
