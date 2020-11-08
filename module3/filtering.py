"""Filter out stopwords for word cloud"""

import sys
import nltk
try:
    from nltk.corpus import stopwords
except LookupError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords

sw = stopwords.words("french")
# Stop words added by the teacher
sw += [
    "les", "plus", "cette", "fait", "faire", "être", "deux", "comme", "dont",
    "tout", "ils", "bien", "sans", "peut", "tous", "après", "ainsi", "donc",
    "cet", "sous", "celle", "entre", "encore", "toutes", "pendant", "moins",
    "dire", "cela", "non", "faut", "trois", "aussi", "dit", "avoir", "doit",
    "contre", "depuis", "autres", "van", "het", "autre", "jusqu"
]
# My stop words
sw += [
    # Avoid over-representation of dates in the word cloud
    "janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
    "septembre", "octobre", "novembre", "décembre", "ans", "années"
    # Avoid over-representation of non-interesting or obvious words
    "ville", "bruxelles", "conseil", "communal", "mesdames", "messieurs",
    "bourgmestre",
    # Other french stop words which were over-represented
    "idem", "car", "etc", "quelque", "tant", "telle", "ceux", "elles", "peu",
    "devant", "voir", "leurs", "lorsque"
]
sw = set(sw)


def filtering(dpath, year):
    path = f"{dpath}/{year}.txt"
    output = open(f"{dpath}/{year}_keywords.txt", "w", encoding='utf-8')

    with open(path, encoding='utf-8') as f:
        text = f.read()
        words = nltk.wordpunct_tokenize(text)
        kept = [
            w.lower()
            for w in words
            if len(w) > 2 and w.isalpha() and w.lower() not in sw
        ]
        kept_string = " ".join(kept)
        output.write(kept_string)


if __name__ == '__main__':
    data_path = sys.argv[1]
    chosen_year = sys.argv[2]
    filtering(data_path, chosen_year)
