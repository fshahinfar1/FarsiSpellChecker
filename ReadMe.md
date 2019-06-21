# Farsi Spell Checker
## Disclaimer
1) This is a work-in-progress project. (WIP)
2) The data sets and trained models are not included in this
repository. (Mostly because their size were about 800MB.)
3) The procedure described below may change.

## Chosen algorithm
LM: 3-gram with backoff and turing-good normalization.
CM: Noisy channel with naive bayes.

## How it is going to be trained
1) Gather data of normal farsi writtings. (Normal data set)
2) Gather data with possible mistakes. (Noisy data set)
3) Create a dictionary from normal data set.
4) Create a language model from normal data set. (3-gram)
5) Mark words of noisy data set which are not in created dictionary. 
(finding out of dictionary spelling errors)
6) Mark words of noisy data which are not probble base on LM.
(finding mistype words which are in dictionary)
7) Find the correct spelling of marked words by hand. (This might be tidious)
8) Split mistake datas to train, dev and test sets.
9) Create a confusion matrix (edit distant) for modeling noisy channel.

Training is done after these steps and model can be tested.

## Data sets
I have gathered data from HamshahriOnline and Virgool.
I assume HamshahriOnline as the normal data set and
Virgool posts as noisy data.

I will manage spelling errors in a csv file with two columns.
One of the columns will be for correct word and the other represents
the misspelled word.

After creating the csv file its data should be splitted into three
test set of training, development and testing.

## Progress
1) Some data from HamshahriOnline has been gathered. (it is confiremed that this data has noise.)
2) Some data from Virgool has been gathered.
3) 3 language models (1, 2, 3 -grams with laplace smoothing) have been trained.
4) Find spelling errors by checking 1-gram and suggest words with edit distant of 1.

