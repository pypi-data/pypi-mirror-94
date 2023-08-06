#egrep.py
import sys, re

#sys.argv is the list of command-line arguments
#sys.argv[0] is the name of the program itself
#sys.argv[1] will be the regex specified at command line

regex = sys.argv[1]
print("regex : ", regex)

#for ever line passed into the script
for line in sys.stdin :
    #if it matches the regex, write to stdout
    if re.search(regex, line) :
        sys.stdout.write(line)
