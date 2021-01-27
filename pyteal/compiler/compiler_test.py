import pytest

from .. import *
from .compiler import compileTeal

def test_compile_single():
    expr = Int(1)

    expected = """
#pragma version 2
int 1
""".strip()
    actual_application = compileTeal(expr, Mode.Application)
    actual_signature = compileTeal(expr, Mode.Signature)

    assert actual_application == actual_signature
    assert actual_application == expected

def test_compile_sequence():
    expr = Seq([Pop(Int(1)), Pop(Int(2)), Int(3) + Int(4)])

    expected = """
#pragma version 2
int 1
pop
int 2
pop
int 3
int 4
+
""".strip()
    actual_application = compileTeal(expr, Mode.Application)
    actual_signature = compileTeal(expr, Mode.Signature)

    assert actual_application == actual_signature
    assert actual_application == expected

def test_compile_branch():
    expr = If(Int(1), Bytes("true"), Bytes("false"))

    expected = """
#pragma version 2
int 1
bnz l2
byte "false"
b l3
l2:
byte "true"
l3:
""".strip()
    actual_application = compileTeal(expr, Mode.Application)
    actual_signature = compileTeal(expr, Mode.Signature)

    assert actual_application == actual_signature
    assert actual_application == expected

def test_compile_mode():
    expr = App.globalGet(Bytes("key"))

    expected = """
#pragma version 2
byte "key"
app_global_get
""".strip()
    actual_application = compileTeal(expr, Mode.Application)

    assert actual_application == expected

    with pytest.raises(TealInputError):
        compileTeal(expr, Mode.Signature)
