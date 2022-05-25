"""
Wordle helper to derive information from the Green, Yellow, Grey patterns
posted by other solvers.
"""

from collections import defaultdict
from time import perf_counter
import json
from wordlists import solutions, alloptions

print (len(solutions), len(alloptions) )

#---------------------------------------------------------------------------
def pattern(solutionword, guess):
  #if not ( len(solutionword)==5 and len(guess)==5):
  #  print( solutionword, guess)
  #  raise Exception("wrong length")
  
  list_solutionword = list(solutionword)
  p = ['.']*5

  # find greens first, and remove the letter from the solution
  # so that we don't get false yellows for a repeated letter in the guess word
  for i,g in enumerate(guess):
    if solutionword[i] == g:
      p[i] = 'G'
      list_solutionword[i]='.'
  
  # find yellows, removing a matched letter from the solution
  # so that we don't get further false yellows for a repeated letter in the guess word
  for i,g in enumerate(guess):
    if g in list_solutionword:
      if p[i] != 'G':
          p[i] = 'Y'
          list_solutionword[list_solutionword.index(g)]='.'

  return ''.join(p)    
#---------------------------------------------------------------------------
    
patterndictcounts = defaultdict(lambda: defaultdict(int))
for s in solutions:
  for w in alloptions:
    patterndictcounts[s][pattern(s,w)] +=1


  
json_object = json.dumps(patterndictcounts, indent = 4) 
print(json_object)

