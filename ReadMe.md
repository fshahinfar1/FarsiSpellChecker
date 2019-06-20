# Farsi Spell Checker
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

