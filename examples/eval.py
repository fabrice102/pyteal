from pyteal import *


def Test(a: Expr, b: Expr, c: Expr):
    return (a - b) / c


print(Test(Int(42), Int(2), Int(10)).__eval__(None))
