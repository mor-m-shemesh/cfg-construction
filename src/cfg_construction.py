"""
In this exercise, we will convert a simple assembly language into a CFG (control flow graph), and later apply SSA rules
on it.
CFGs (https://en.wikipedia.org/wiki/Control-flow_graph) are directed graphs (https://en.wikipedia.org/wiki/Directed_graph),
where the nodes are usually instructions or basic blocks (https://en.wikipedia.org/wiki/Basic_block) and the edges represent
possible flows between the nodes.
Usually, there are two kinds of edges - plain ones (meaning unconditional flow from one node to another) or conditional
flows (meaning the flow will be decided from two options depending on some condition).
CFGs are useful for many kinds of analyses (liveness/dead code, stack recovery, pointer analysis,
folding, slicing, etc.)
Enough talk, let's get down to business!
Here's the definition for our assembly language:
"""
import enum
from dataclasses import dataclass
from typing import Optional, Union, List
from venv import logger


class Operation(enum.Enum):
    ADD = enum.auto()
    SUB = enum.auto()
    MUL = enum.auto()
    DIV = enum.auto()


@dataclass
class Var:
    name: str


Value = Union[Var, int]  # Variable (e.g. "foo", "x") or int for a const


@dataclass
class Expression:
    lhs: Value
    rhs: Value
    operation: Operation


@dataclass
class Assignment:
    dst: Var
    src: Union[Value, Expression]


@dataclass
class Jump:
    target: int
    condition: Optional[Var]  # If a condition is provided, the branch is taken if the var is not zero


@dataclass
class Call:
    function_name: str
    args: List[Value]


"""
Now let's write some code - e.g. exponentiation
"""

base = Var("base")
counter = Var("counter")
output = Var("output")

code = [
    Assignment(base, 2),  # 0
    Assignment(counter, 5),  # 1
    Assignment(output, 1),  # 2
    # Loop start
    Assignment(output, Expression(output, base, Operation.MUL)),  # 3
    Assignment(counter, Expression(counter, 1, Operation.SUB)),  # 4
    Jump(3, counter),  # 5
    Call("print", [output])  # 6
]

"""
Now, we want to build a control flow graph from this function.
Our nodes will be instructions, and our edges will contain conditions. For example, the code:
    a = 1
    jump(AFTER, a)
    b = 2
    jump(END)
    AFTER:
    b = 3
    END:
    print(b)

Would be represented as:
  a = 1
 ||    \\
 || !a  \\  a
 ||      \\
 b = 2    b = 3
 ||       //
 ||      //
 print(b)
You can use any library for basic graph functions - e.g. networkx. Don't forget to write tests!
"""

import networkx as nx
from utils.log_util import make_logger
from collections import defaultdict, OrderedDict
from sortedcontainers import SortedSet

Opcode = Union[Expression, Assignment, Jump, Call]


@dataclass
class Block:
    start: Optional[int]
    end: Optional[int]
    jump_targets: Optional[list]


def build_cfg(variables: List[Var], instructions: List[Opcode]):
    pass
    log = make_logger(stdout=True, filepath="cfg_construction.log")
    log.info('New run!')

    jumps = defaultdict(list)
    blocks = dict({0: Block(start=0, end=-1, jump_targets=list())})  # Just a sorted dict of the start:end
    block_starts = SortedSet([0])

    curr_block = blocks[0]
    last_jump_skipped = False
    for i, ins in enumerate(instructions):
        # Create new block if I am jumped to,
        # or someone jumped ahead of me
        if i in jumps or last_jump_skipped:
            last_jump_skipped = False
            curr_block = Block(start=i, end=-1, jump_targets=list())
            blocks[i] = curr_block
            block_starts.add(i)

        # We reached a Jump opcode that means something (jumps anywhere that's not one opcode ahead)
        if isinstance(ins, Jump) and ins.target != i + 1:
            # Finish the current block
            curr_block.end = i

            # If jump ahead -
            jumps[ins.target].append(i)
            curr_block.jump_targets.append(ins.target)

            if ins.target < i:  # we need to split a previous block (or the current one)
                log.debug(f"Splitting block {block_starts.bisect_left(ins.target) - 1}")
                block_to_split = blocks[block_starts.bisect_left(ins.target) - 1]
                new_block = Block(start=ins.target, end=block_to_split.end, jump_targets=block_to_split.jump_targets)
                block_starts.add(ins.target)
                block_to_split.end = ins.target - 1
                block_to_split.jump_targets = [ins.target]
                blocks[ins.target] = new_block
                log.debug(f"Split block: {block_to_split}")
                log.debug(f"New block: {new_block}")
                curr_block = new_block

            # if conditional jump - add the default continue ahead jump.
            if ins.condition:
                curr_block.jump_targets.append(i + 1)
                jumps[i + 1].append(i)
            else: # if we have a jump ahead with no default continue - we start a new block
                last_jump_skipped = True
        # Print the structures
        log.debug(blocks)
        log.debug(jumps)
        log.debug(block_starts)


def main():
    build_cfg(None, code)


if __name__ == "__main__":
    main()