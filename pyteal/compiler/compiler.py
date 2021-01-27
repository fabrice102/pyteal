from typing import List

from ..ast import Expr
from ..ir import Op, Mode, TealComponent, TealOp, TealLabel, TealBlock, TealSimpleBlock, TealConditionalBlock
from ..errors import TealInputError, TealInternalError
from ..config import NUM_SLOTS

from .sort import sortBlocks
from .flatten import flattenBlocks

def verifyOpsForMode(teal: List[TealComponent], mode: Mode):
    """Verify that all TEAL operations are allowed in mode.

    Args:
        teal: Code to check.
        mode: The mode to check against.

    Raises:
        TealInputError: if teal contains an operation not allowed in mode.
    """
    for stmt in teal:
        if isinstance(stmt, TealOp):
            op = stmt.getOp()
            if not op.mode & mode:
                raise TealInputError("Op not supported in {} mode: {}".format(mode.name, op.value))

def compileTeal(ast: Expr, mode: Mode) -> str:
    """Compile a PyTeal expression into TEAL assembly.

    Args:
        ast: The PyTeal expression to assemble.
        mode: The mode of the program to assemble. Must be Signature or Application.

    Returns:
        A TEAL assembly program compiled from the input expression.

    Raises:
        TealInputError: if an operation in ast is not supported by the supplied mode.
    """
    start, _ = ast.__teal__()
    start.addIncoming()
    start.validate()

    start = TealBlock.NormalizeBlocks(start)
    start.validate()

    order = sortBlocks(start)
    teal = flattenBlocks(order)

    verifyOpsForMode(teal, mode)

    slots = set()
    for stmt in teal:
        for slot in stmt.getSlots():
            slots.add(slot)
    
    if len(slots) > NUM_SLOTS:
        # TODO: identify which slots can be reused
        raise TealInternalError("Too many slots in use: {}, maximum is {}".format(slots, NUM_SLOTS))
    
    # TODO: convert slots to a list with a defined order so that generated code is deterministic
    location = 0
    while len(slots) > 0:
        slot = slots.pop()
        for stmt in teal:
            stmt.assignSlot(slot, location)
        location += 1

    lines = ["#pragma version 2"]
    lines += [i.assemble() for i in teal]
    return "\n".join(lines)
