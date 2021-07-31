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

