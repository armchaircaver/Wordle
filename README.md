A program to suggest the next word to enter into worde, based on the results of guesses so far.

The program can also analyse the patterns of green, yellow and grey letters that have been posted on facebook or other social media sites for the day's wordle puzzle, reducing the initial set of solution words based on the patterns reported.

The search algorithm examines each possible guess word from the approx 13,000 allowed guesses, using a recursive algorithm to search the possible trees of guesses to find the one that minimises the average number of guesses needed to solve the puzzle.

There are several python scripts:

- precalculate_patterns.py calculates all the patterns that can occur for each solution word, to build up a map of the patterns that can be associated with each solution word.

- precalculated_patterns.py is the result of this pre-calculation, and is used by wordle_solver.py to eliminate solutions that aren't consistent with the set of patterns reported by other players.

- wordle_recursive.py is the recursive algorithm that searches word trees to find the best guess given the results of words entered so far

- wordle_solver.py a program to enter patterns and guesses made so far into the recursive algorithm, to obtain the best guess for the next word

- wordle optimal tree generator.py  is a program that generates the optimal tree of guesses for a given starting word

The program "wordle optimal tree generator.py" generates a tree with the same average number of guesses, 3.4201, as the optimal search program created by Alex Selby, described in http://sonorouschocolate.com/notes/index.php?title=The_best_strategies_for_Wordle

The file "wordle optimal tree.log" lists this optimal tree.


