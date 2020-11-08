"""Testing keyword extraction with YAKE"""

import argparse
import os

import yake

parser = argparse.ArgumentParser(
    description='Extract keywords from AVB bulletins (in txt form).'
)
parser.add_argument(
    '--year', type=int, default=1955,
    help='Year to extract from (default: 1955, because we had to chose one)'
)
parser.add_argument(
    '--ngrams', type=int, default=2,
    help='N-grams or higher to research (default: bigrams or higher)'
)

args = parser.parse_args()

ignored = set(["conseil communal", "conseil général"])

kw_extractor = yake.KeywordExtractor(lan="fr", top=20)
data_path = "data/txt/"
files = os.listdir(data_path)
for f in sorted(files):
    if f.startswith(f"Bxl_{args.year}"):
        text = open(data_path + f).read()
        keywords = kw_extractor.extract_keywords(text)
        kept = []
        for score, kw in keywords:
            words = kw.split()
            if len(words) > (args.ngrams - 1) and kw not in ignored:  # only bigrams and more
                kept.append(kw)
        print(f"{f} mentions these keywords: {', '.join(kept)}...")
