# MAvis 1 feedback
From: Anton Jørgensen
To: Group 11

## General
Score: 3/4

## Exercise 1
Nice and clear overview.

## Exercise 2 + 3
You talk a lot about 'this increases', 'that gets bigger', etc., but only at the
end do you specify that the state space grows exponentially with the number
of agents. Try to quickly get to the exact answers.

Good point about DFS being better for deep goals.

Your BFSfriendly level is not that much easier for BFS than for DFS, it even
searches fewer states! Things like adding additional agents with goals, and
increasing the level size just a little, would have made a much bigger impact.

## Exercise 4
Again, you use a long(ish) explanation to tell us something that is theory: BFS
guarantees optimal solutions. Using the theorems directly makes it much easier
to understand, and quicker to explain.

Manhattan distance on its own is only admissible for single goal levels.

'The performance of BFS is still the best': According to what metric? There are
also entire levels that BFS cannot solve?

## Exercise 5
Good explanation of the push/pull actions, but generally spend less time on
implementation details, and more on the impact (e.g. what does the new actions
do to the branching factor?)

'Less optimal': Optimality is either/or, if you want to highlight especially bad
solutions say they are worse or longer.

## Exercise 6
I don't quite get the point of adding an agents 'distance to an arbitrary goal'
surely you select them in some way?

Cool to see such a big increase in performance for a relatively small change 
in heuristic!!
