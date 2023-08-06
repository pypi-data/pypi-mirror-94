wildgram tokenizes english text into "wild"-grams (tokens of varying word count)
that match closely to the the natural pauses of conversation. I originally built
it as the first step in an abstraction pipeline for medical language: since
medical concepts tend to be phrases of varying lengths, bag-of-words or bigrams
doesn't really cut it.

Wildgrams works by measuring the size of the noise (stopwords, punctuation, and
whitespace) and breaks up the text against noise of a certain size
(it varies slightly depending on the noise).
Some examples:
"rats, bats, and vats" -> ["rats","bats", "vats"]
"I dreamed a dream in time gone by" -> ["i dreamed","dream", "time gone"]

Because this is originally for a medical abstraction, some of the stop words include
words like "denies" which tend to signify a change
in topic in medical notes. Some of these words are separated into their own topics
(since they have clinical meaning), while others are removed entirely.
Numbers (0.1, 1.0, 3), "denies", etc. are an example of the former.

Words with digits that have other punctuation or characters
(e.g. potentially ids like CS123123 or time like 12:30)
are left alone as potentially part of a larger phrase.

The full list of words that get removed entirely is in the global constant STOPWORDS in wildgram.py
The full list of words/regex patterns that are separated into their own chunk can be found in TOPICWORDS in wildgram.py

Two examples:
"patient denies consuming alcohol" -> ["patient", "denies", "consuming alcohol"]
"patient describes consuming alcohol" -> ["patient", "consuming alcohol"]

Also note that it doesn't strictly tokenize each token like so:
"I dreamed a dream in time gone by" -> [("I","dreamed"),("dream"), ("time","gone")]

Final note: I do not include "of" in the stop word list, because there are quite a few
medical concepts that have of in the middle (e.g. "shortness of breath").

Updates for 0.0.6 Version:
There are now 3 new parameters to the wildgram function, all with defaults:
topicwords, stopwords, and include1gram.
topicwords: default is the list in TOPICWORDS. Can be replaced with a custom list.
stopwords: default is the list in STOPWORDS. Can be replaced with a custom list.
include1gram: boolean, default is True. True will include both the full
wildgram phrase as well as all individual tokens in the phrase, e.g.:
"I dreamed a dream in time gone by" -> ["I dreamed", "I", "dream","time gone", "time", "gone"]
Any 1-gram tokens immediately follow the wildgram token so it's still a semi-ordered list.


Update for 0.0.7 Version:
There is a new parameter called "joinerwords", which currently defaults to:
```python
JOINERWORDS = [
"of",
"in",
"to",
"on",
"than",
"at"
]
```
Demarcations that include those words will do this (assuming of is a stopword):
"shortness of breath"-> "shortness", "shortness of breath", "breath".
joiner words MUST be included in the stopwords list to be effective.


Update for version 0.0.93:
a new parameter "returnNoise" (default false) will if true also return all the
non-overlapping noise ranges (not the values, just the indexes).

Example code:

```python
from wildgram import wildgram
tokens, ranges = wildgram("and was beautiful")
#tokens -- the wildgram tokens
#ranges -- a list of tuples, the ith tuple has the start and end indexes for the ith wildgram
print(tokens, ranges) #["beautiful"], [(8, 17)]
tokens, ranges = wildgram("was a beautiful day", include1gram=True)
#tokens -- the wildgram tokens
#ranges -- a list of tuples, the ith tuple has the start and end indexes for the ith wildgram
print(tokens, ranges) #["beautiful day", "beautiful", "day"]

tokens, ranges, noise = wildgram("was a beautiful day", returnNoise=True)

print(noise) # [(0,6)]

```
That's all folks!
