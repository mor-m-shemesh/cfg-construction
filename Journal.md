# CFG Construction!

### The API:

Input - 

@variables - List[Var]
@instructions - List[Assignment / Jump / Expression / Call]

Output - Graph constructed using "networkx" 

------

I configured my Pycharm to be how I like it, figured out how to use logging properly, built a logger util, all the while trying to think of how to start implementing this project...

## Intermission - time to LEARN!

I was getting ahead of myself trying to break my brain thinking of how to implement this CFG, even though I had a really hard time figuring it out, so I had to learn the basics first.

I started with the recommended sources given in the explanation:
**CFGs (https://en.wikipedia.org/wiki/Control-flow_graph)** - I knew what directed graphs were, so felt comfortable skipping the definition of directed graphs and facing the next step.
I was prepared to jump into **basic blocks (https://en.wikipedia.org/wiki/Basic_block)** just in case they weren't what I was assuming they were.

SO, cfg... 
After reading the Wiki article on CFGs, I felt comfortable with the concept - everything made sense to me. Basic, so it is to be expected... There were a lot of references to computational optimization algorithms and concepts that I assume are useful when building things like interpreters and compilers (and SSA), but beside having a guess as to what they're good for, I don't know much about. I just know compilers lie a whole lot and can do some wicked smart and bastardly stuff...

I studied the 1st figure on the CFG wiki article to make sure I understood it, and wasn't surprised :)

Now, let's check something that bothers me - is there a "print" functionality to networkx
There is! good.

## The algorithm!

What am I aiming for? An algorithm that will make me a graph in O(n) time.
After a quick discussion with my dad (a very experienced programmer), that we had last weekend, I figured it's quite simple - 

You iterate the list of instructions, and start defining a block.
A block is defined by the start index (the first opcode) and the end index (the last opcode of the block).
During iteration, a block will be defined with a start index, but it's end index is defined and changed when

1) there is a JUMP opcode from inside the block
2) there is a JUMP opcode into the middle of the block

I'll need to keep track of the following:

1. All the JUMP opcodes, and where they lead, sorted by destination, IF AND ONLY IF they jump forward. the sorted dict is as such:
   { dest_address : [source addresses] }
2. All of the blocks, that I create as a dict 
3. all the starts of blocks, sorted in an AVL. I looked for and found a nice implementation that gives you a bisect function, using 'sortedcontainers' - SortedSet.

After I started writing a naïve and spaghetti-prone implementation, I rethought about it and started from scratch.

My writer's block ended and I finished implementing a simple algorithm with not much fancy frameworking (graphics, tests... still a WIP). took about... 3 hours from start to finish?

### catastrophe!

going over my code briefly, I noticed something bad - When splitting an old block, I set the curr_block no matter how far above me the block being split  is...
A quick fix - check if we are on the end of the new block created in the split! Worked like a charm!
