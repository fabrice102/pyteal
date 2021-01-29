from typing import Callable, List

from ..ir import TealBlock

Optimization = Callable[[TealBlock], TealBlock]

def applyOptimizationToList(blocks: List[TealBlock], optimization: Optimization) -> List[TealBlock]:
    return [optimization(block) for block in blocks]

def applyOptimizationRecursively(startBlock: TealBlock, optimization: Optimization) -> TealBlock:
    for block in TealBlock.Iterate(startBlock):
        startBlock = optimization(block)
    return startBlock
