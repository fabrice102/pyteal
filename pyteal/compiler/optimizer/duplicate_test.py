from ... import *

from .duplicate import getDependenciesForOp, detectDuplicatesInBlock

def test_dependencies_1():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
    ]
    
    complete, actual = getDependenciesForOp(ops, 1)
    expected = [
        TealOp(Op.int, 2),
    ]

    assert complete
    assert actual == expected

def test_dependencies_2():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.logic_not),
        TealOp(Op.int, 3),
    ]
    
    complete, actual = getDependenciesForOp(ops, 2)
    expected = [
        TealOp(Op.int, 2),
        TealOp(Op.logic_not),
    ]

    assert complete
    assert actual == expected

def test_dependencies_3():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.add),
        TealOp(Op.int, 4),
    ]
    
    complete, actual = getDependenciesForOp(ops, 3)
    expected = [
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.add),
    ]

    assert complete
    assert actual == expected

def test_dependencies_4():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.bitwise_not),
        TealOp(Op.int, 3),
        TealOp(Op.add),
        TealOp(Op.int, 4),
    ]
    
    complete, actual = getDependenciesForOp(ops, 4)
    expected = [
        TealOp(Op.int, 2),
        TealOp(Op.bitwise_not),
        TealOp(Op.int, 3),
        TealOp(Op.add),
    ]

    assert complete
    assert actual == expected

def test_dependencies_5():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.byte, "0x00"),
        TealOp(Op.int, 3),
        TealOp(Op.logic_not),
        TealOp(Op.app_local_put),
        TealOp(Op.int, 4),
    ]
    
    complete, actual = getDependenciesForOp(ops, 5)
    expected = [
        TealOp(Op.int, 2),
        TealOp(Op.byte, "0x00"),
        TealOp(Op.int, 3),
        TealOp(Op.logic_not),
        TealOp(Op.app_local_put),
    ]

    assert complete
    assert actual == expected

def test_dependencies_6():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.byte, "0x00"),
        TealOp(Op.byte, "0xFF"),
        TealOp(Op.concat),
        TealOp(Op.int, 3),
        TealOp(Op.app_local_put),
        TealOp(Op.int, 4),
    ]
    
    complete, actual = getDependenciesForOp(ops, 6)
    expected = [
        TealOp(Op.int, 2),
        TealOp(Op.byte, "0x00"),
        TealOp(Op.byte, "0xFF"),
        TealOp(Op.concat),
        TealOp(Op.int, 3),
        TealOp(Op.app_local_put),
    ]

    assert complete
    assert actual == expected

def test_dependencies_with_op_that_pushes_2():
    ops = [
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.addw),
        TealOp(Op.int, 4),
    ]
    
    complete, actual = getDependenciesForOp(ops, 3)
    expected = [
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.addw),
    ]

    assert complete
    assert actual == expected

def test_detect_duplicates_none():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.int, 3),
        ])
    )

    expected = TealSimpleBlock([
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
    ])

    assert actual == expected


def test_detect_duplicates_single_depth_1():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.int, 2),
            TealOp(Op.int, 3),
        ])
    )

    expected = TealSimpleBlock([
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.dup),
        TealOp(Op.int, 3),
    ])

    assert actual == expected

def test_detect_duplicates_single_depth_2():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.logic_not),
            TealOp(Op.int, 2),
            TealOp(Op.logic_not),
            TealOp(Op.int, 3),
        ])
    )

    expected = TealSimpleBlock([
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.logic_not),
        TealOp(Op.dup),
        TealOp(Op.int, 3),
    ])

    assert actual == expected

def test_detect_duplicates_single_depth_3():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.int, 3),
            TealOp(Op.add),
            TealOp(Op.int, 2),
            TealOp(Op.int, 3),
            TealOp(Op.add),
            TealOp(Op.int, 4),
        ])
    )

    expected = TealSimpleBlock([
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.int, 3),
        TealOp(Op.add),
        TealOp(Op.dup),
        TealOp(Op.int, 4),
    ])

    assert actual == expected

def test_detect_duplicates_single_depth_4():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 1),
            TealOp(Op.byte, "\"o\""),
            TealOp(Op.gtxn, 2, "XferAsset"),
            TealOp(Op.itob),
            TealOp(Op.concat),
            TealOp(Op.byte, "\"o\""),
            TealOp(Op.gtxn, 2, "XferAsset"),
            TealOp(Op.itob),
            TealOp(Op.concat),
            TealOp(Op.app_global_get),
            TealOp(Op.gtxn, 2, "AssetAmount"),
            TealOp(Op.add),
            TealOp(Op.int, 100),
            TealOp(Op.minus),
            TealOp(Op.app_global_put),
            TealOp(Op.return_),
        ])
    )

    expected = TealSimpleBlock([
        TealOp(Op.int, 1),
        TealOp(Op.byte, "\"o\""),
        TealOp(Op.gtxn, 2, "XferAsset"),
        TealOp(Op.itob),
        TealOp(Op.concat),
        TealOp(Op.dup),
        TealOp(Op.app_global_get),
        TealOp(Op.gtxn, 2, "AssetAmount"),
        TealOp(Op.add),
        TealOp(Op.int, 100),
        TealOp(Op.minus),
        TealOp(Op.app_global_put),
        TealOp(Op.return_),
    ])

    assert actual == expected

def test_detect_duplicates_double_simple():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 0),
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.int, 1),
            TealOp(Op.int, 2),
            TealOp(Op.int, 3),
        ])
    )

    expected = TealSimpleBlock([
        TealOp(Op.int, 0),
        TealOp(Op.int, 1),
        TealOp(Op.int, 2),
        TealOp(Op.dup2),
        TealOp(Op.int, 3),
    ])

    assert actual == expected

def test_detect_duplicates_double_complex():
    actual = detectDuplicatesInBlock(
        TealSimpleBlock([
            TealOp(Op.int, 0),
            TealOp(Op.int, 1),
            TealOp(Op.byte, "\"e\""),
            TealOp(Op.gtxn, 3, "XferAsset"),
            TealOp(Op.itob),
            TealOp(Op.concat),
            TealOp(Op.int, 1),
            TealOp(Op.byte, "\"e\""),
            TealOp(Op.gtxn, 3, "XferAsset"),
            TealOp(Op.itob),
            TealOp(Op.concat),
            TealOp(Op.app_local_get),
            TealOp(Op.int, 100),
            TealOp(Op.add),
            TealOp(Op.gtxn, 3, "AssetAmount"),
            TealOp(Op.minus),
            TealOp(Op.app_local_put),
            TealOp(Op.int, 6),
        ])
    )
    detectDuplicatesInBlock(actual)

    expected = TealSimpleBlock([
        TealOp(Op.int, 0),
        TealOp(Op.int, 1),
        TealOp(Op.byte, "\"e\""),
        TealOp(Op.gtxn, 3, "XferAsset"),
        TealOp(Op.itob),
        TealOp(Op.concat),
        TealOp(Op.dup2),
        TealOp(Op.app_local_get),
        TealOp(Op.int, 100),
        TealOp(Op.add),
        TealOp(Op.gtxn, 3, "AssetAmount"),
        TealOp(Op.minus),
        TealOp(Op.app_local_put),
        TealOp(Op.int, 6),
    ])

    assert actual == expected
