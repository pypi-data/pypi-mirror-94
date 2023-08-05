#most_common_words.py
import sys
from collections import Counter

#pass in a number of words as first arg
try :
    num_words = int(sys.argv[1])
except :
    print("usage : most_common_words.py num_words")
    sys.exit(1) #nonzero exit code denotes error

counter = Counter(word.lower() #ower case words
                  for line in sys.stdin
                  for word in line.strip().split() #split on spaces
                  if word  #skip empty words
                  )

for word, count in counter.most_common(num_words) :
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")
