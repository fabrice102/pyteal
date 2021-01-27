from .. import *

from .flatten import flattenBlocks

def test_flatten_none():
    blocks = []

    expected = []
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_single_empty():
    blocks = [
        TealSimpleBlock([])
    ]

    expected = []
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_single_one():
    blocks = [
        TealSimpleBlock([TealOp(Op.int, 1)])
    ]

    expected = [TealOp(Op.int, 1)]
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_single_many():
    blocks = [
        TealSimpleBlock([
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.int, 3),
            TealOp(Op.add),
            TealOp(Op.add)
        ])
    ]

    expected = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.add),
        TealOp(Op.add)
    ]
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_sequence():
    block5 = TealSimpleBlock([TealOp(Op.int, 5)])
    block4 = TealSimpleBlock([TealOp(Op.int, 4)])
    block4.setNextBlock(block5)
    block3 = TealSimpleBlock([TealOp(Op.int, 3)])
    block3.setNextBlock(block4)
    block2 = TealSimpleBlock([TealOp(Op.int, 2)])
    block2.setNextBlock(block3)
    block1 = TealSimpleBlock([TealOp(Op.int, 1)])
    block1.setNextBlock(block2)
    block1.addIncoming()
    block1.validate()
    blocks = [block1, block2, block3, block4, block5]

    expected = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.int, 4),
        TealOp(Op.int, 5)
    ]
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_branch():
    blockTrue = TealSimpleBlock([TealOp(Op.byte, "\"true\""), TealOp(Op.return_)])
    blockFalse = TealSimpleBlock([TealOp(Op.byte, "\"false\""), TealOp(Op.return_)])
    block = TealConditionalBlock([TealOp(Op.int, 1)])
    block.setTrueBlock(blockTrue)
    block.setFalseBlock(blockFalse)
    block.addIncoming()
    block.validate()
    blocks = [block, blockFalse, blockTrue]

    expected = [
        TealOp(Op.int, 1),
        TealOp(Op.bnz, "l2"),
        TealOp(Op.byte, "\"false\""),
        TealOp(Op.return_),
        TealLabel("l2"),
        TealOp(Op.byte, "\"true\""),
        TealOp(Op.return_)
    ]
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_branch_converge():
    blockEnd = TealSimpleBlock([TealOp(Op.return_)])
    blockTrue = TealSimpleBlock([TealOp(Op.byte, "\"true\"")])
    blockTrue.setNextBlock(blockEnd)
    blockFalse = TealSimpleBlock([TealOp(Op.byte, "\"false\"")])
    blockFalse.setNextBlock(blockEnd)
    block = TealConditionalBlock([TealOp(Op.int, 1)])
    block.setTrueBlock(blockTrue)
    block.setFalseBlock(blockFalse)
    block.addIncoming()
    block.validate()
    blocks = [block, blockFalse, blockTrue, blockEnd]

    expected = [
        TealOp(Op.int, 1),
        TealOp(Op.bnz, "l2"),
        TealOp(Op.byte, "\"false\""),
        TealOp(Op.b, "l3"),
        TealLabel("l2"),
        TealOp(Op.byte, "\"true\""),
        TealLabel("l3"),
        TealOp(Op.return_)
    ]
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_multiple_branch():
    blockTrueTrue = TealSimpleBlock([TealOp(Op.byte, "\"true true\""), TealOp(Op.return_)])
    blockTrueFalse = TealSimpleBlock([TealOp(Op.byte, "\"true false\""), TealOp(Op.err)])
    blockTrueBranch = TealConditionalBlock([])
    blockTrueBranch.setTrueBlock(blockTrueTrue)
    blockTrueBranch.setFalseBlock(blockTrueFalse)
    blockTrue = TealSimpleBlock([TealOp(Op.byte, "\"true\"")])
    blockTrue.setNextBlock(blockTrueBranch)
    blockFalse = TealSimpleBlock([TealOp(Op.byte, "\"false\""), TealOp(Op.return_)])
    block = TealConditionalBlock([TealOp(Op.int, 1)])
    block.setTrueBlock(blockTrue)
    block.setFalseBlock(blockFalse)
    block.addIncoming()
    block.validate()
    blocks = [block, blockFalse, blockTrue, blockTrueBranch, blockTrueFalse, blockTrueTrue]
    
    expected = [
        TealOp(Op.int, 1),
        TealOp(Op.bnz, "l2"),
        TealOp(Op.byte, "\"false\""),
        TealOp(Op.return_),
        TealLabel("l2"),
        TealOp(Op.byte, "\"true\""),
        TealOp(Op.bnz, "l5"),
        TealOp(Op.byte, "\"true false\""),
        TealOp(Op.err),
        TealLabel("l5"),
        TealOp(Op.byte, "\"true true\""),
        TealOp(Op.return_)
    ]
    actual = flattenBlocks(blocks)

    assert actual == expected

def test_flatten_multiple_branch_converge():
    blockEnd = TealSimpleBlock([TealOp(Op.return_)])
    blockTrueTrue = TealSimpleBlock([TealOp(Op.byte, "\"true true\"")])
    blockTrueTrue.setNextBlock(blockEnd)
    blockTrueFalse = TealSimpleBlock([TealOp(Op.byte, "\"true false\""), TealOp(Op.err)])
    blockTrueBranch = TealConditionalBlock([])
    blockTrueBranch.setTrueBlock(blockTrueTrue)
    blockTrueBranch.setFalseBlock(blockTrueFalse)
    blockTrue = TealSimpleBlock([TealOp(Op.byte, "\"true\"")])
    blockTrue.setNextBlock(blockTrueBranch)
    blockFalse = TealSimpleBlock([TealOp(Op.byte, "\"false\"")])
    blockFalse.setNextBlock(blockEnd)
    block = TealConditionalBlock([TealOp(Op.int, 1)])
    block.setTrueBlock(blockTrue)
    block.setFalseBlock(blockFalse)
    block.addIncoming()
    block.validate()
    blocks = [block, blockFalse, blockTrue, blockTrueBranch, blockTrueFalse, blockTrueTrue, blockEnd]
    
    expected = [
        TealOp(Op.int, 1),
        TealOp(Op.bnz, "l2"),
        TealOp(Op.byte, "\"false\""),
        TealOp(Op.b, "l6"),
        TealLabel("l2"),
        TealOp(Op.byte, "\"true\""),
        TealOp(Op.bnz, "l5"),
        TealOp(Op.byte, "\"true false\""),
        TealOp(Op.err),
        TealLabel("l5"),
        TealOp(Op.byte, "\"true true\""),
        TealLabel("l6"),
        TealOp(Op.return_)
    ]
    actual = flattenBlocks(blocks)

    assert actual == expected
