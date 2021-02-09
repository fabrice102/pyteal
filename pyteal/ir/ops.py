from typing import NamedTuple, cast
from enum import Enum, Flag, auto

class Mode(Flag):
    """Enum of program running modes."""
    
    Signature = auto()
    Application = auto()

Mode.__module__ = "pyteal"

OpType = NamedTuple('OpType', [('value', str), ('pops', int), ('pushes', int), ('mode', Mode)])

class Op(Enum):
    """Enum of program opcodes."""

    def __str__(self) -> str:
        return self.value.value

    @property
    def pops(self) -> int:
        """Get the number of values this op pops from the stack when ran."""
        return self.value.pops
    
    @property
    def pushes(self) -> int:
        """Get the number of values this op pushes to the stack when ran."""
        return self.value.pushes
    
    @property
    def mode(self) -> Mode:
        """Get the modes that this op is available."""
        return self.value.mode

    err = OpType("err", 0, 0, Mode.Signature | Mode.Application)
    sha256 = OpType("sha256", 1, 1, Mode.Signature | Mode.Application)
    keccak256 = OpType("keccak256", 1, 1, Mode.Signature | Mode.Application)
    sha512_256 = OpType("sha512_256", 1, 1, Mode.Signature | Mode.Application)
    ed25519verify = OpType("ed25519verify", 3, 1, Mode.Signature)
    add = OpType("+", 2, 1, Mode.Signature  | Mode.Application)
    minus = OpType("-", 2, 1, Mode.Signature  | Mode.Application)
    div = OpType("/", 2, 1, Mode.Signature  | Mode.Application)
    mul = OpType("*", 2, 1, Mode.Signature  | Mode.Application)
    lt = OpType("<", 2, 1, Mode.Signature  | Mode.Application)
    gt = OpType(">", 2, 1, Mode.Signature  | Mode.Application)
    le = OpType("<=", 2, 1, Mode.Signature  | Mode.Application)
    ge = OpType(">=", 2, 1, Mode.Signature  | Mode.Application)
    logic_and = OpType("&&", 2, 1, Mode.Signature  | Mode.Application)
    logic_or = OpType("||", 2, 1, Mode.Signature  | Mode.Application)
    eq = OpType("==", 2, 1, Mode.Signature  | Mode.Application)
    neq = OpType("!=", 2, 1, Mode.Signature  | Mode.Application)
    logic_not = OpType("!", 1, 1, Mode.Signature  | Mode.Application)
    len = OpType("len", 1, 1, Mode.Signature | Mode.Application)
    itob = OpType("itob", 1, 1, Mode.Signature | Mode.Application)
    btoi = OpType("btoi", 1, 1, Mode.Signature | Mode.Application)
    mod = OpType("%", 2, 1, Mode.Signature  | Mode.Application)
    bitwise_or = OpType("|", 2, 1, Mode.Signature  | Mode.Application)
    bitwise_and = OpType("&", 2, 1, Mode.Signature  | Mode.Application)
    bitwise_xor = OpType("^", 2, 1, Mode.Signature  | Mode.Application)
    bitwise_not = OpType("~", 1, 1, Mode.Signature  | Mode.Application)
    mulw = OpType("mulw", 2, 2, Mode.Signature | Mode.Application)
    addw = OpType("addw", 2, 2, Mode.Signature | Mode.Application)
    intcblock = OpType("intcblock", 0, 0, Mode.Signature | Mode.Application)
    intc = OpType("intc", 0, 1, Mode.Signature | Mode.Application)
    intc_0 = OpType("intc_0", 0, 1, Mode.Signature | Mode.Application)
    intc_1 = OpType("intc_1", 0, 1, Mode.Signature | Mode.Application)
    intc_2 = OpType("intc_2", 0, 1, Mode.Signature | Mode.Application)
    intc_3 = OpType("intc_3", 0, 1, Mode.Signature | Mode.Application)
    int = OpType("int", 0, 1, Mode.Signature | Mode.Application)
    bytecblock = OpType("bytecblock", 0, 0, Mode.Signature | Mode.Application)
    bytec = OpType("bytec", 0, 1, Mode.Signature | Mode.Application)
    bytec_0 = OpType("bytec_0", 0, 1, Mode.Signature | Mode.Application)
    bytec_1 = OpType("bytec_1", 0, 1, Mode.Signature | Mode.Application)
    bytec_2 = OpType("bytec_2", 0, 1, Mode.Signature | Mode.Application)
    bytec_3 = OpType("bytec_3", 0, 1, Mode.Signature | Mode.Application)
    byte = OpType("byte", 0, 1, Mode.Signature | Mode.Application)
    addr = OpType("addr", 0, 1, Mode.Signature | Mode.Application)
    arg = OpType("arg", 0, 1, Mode.Signature)
    txn = OpType("txn", 0, 1, Mode.Signature | Mode.Application)
    global_ = OpType("global", 0, 1, Mode.Signature | Mode.Application)
    gtxn = OpType("gtxn", 0, 1, Mode.Signature | Mode.Application)
    load = OpType("load", 0, 1, Mode.Signature | Mode.Application)
    store = OpType("store", 1, 0, Mode.Signature | Mode.Application)
    txna = OpType("txna", 0, 1, Mode.Signature | Mode.Application)
    gtxna = OpType("gtxna", 0, 1, Mode.Signature | Mode.Application)
    bnz = OpType("bnz", 1, 0, Mode.Signature | Mode.Application)
    bz = OpType("bz", 1, 0, Mode.Signature | Mode.Application)
    b = OpType("b", 0, 0, Mode.Signature | Mode.Application)
    return_ = OpType("return", 1, 0, Mode.Signature | Mode.Application)
    pop = OpType("pop", 1, 0, Mode.Signature | Mode.Application)
    dup = OpType("dup", 1, 2, Mode.Signature | Mode.Application)
    dup2 = OpType("dup2", 2, 4, Mode.Signature | Mode.Application)
    concat = OpType("concat", 2, 1, Mode.Signature | Mode.Application)
    substring = OpType("substring", 1, 1, Mode.Signature | Mode.Application)
    substring3 = OpType("substring3", 3, 1, Mode.Signature | Mode.Application)
    balance = OpType("balance", 1, 1, Mode.Application)
    app_opted_in = OpType("app_opted_in", 2, 1, Mode.Application)
    app_local_get = OpType("app_local_get", 2, 1, Mode.Application)
    app_local_get_ex = OpType("app_local_get_ex", 3, 1, Mode.Application)
    app_global_get = OpType("app_global_get", 1, 1, Mode.Application)
    app_global_get_ex = OpType("app_global_get_ex", 2, 1, Mode.Application)
    app_local_put = OpType("app_local_put", 3, 0, Mode.Application)
    app_global_put = OpType("app_global_put", 2, 0, Mode.Application)
    app_local_del = OpType("app_local_del", 2, 0, Mode.Application)
    app_global_del = OpType("app_global_del", 1, 0, Mode.Application)
    asset_holding_get = OpType("asset_holding_get", 2, 2, Mode.Application)
    asset_params_get = OpType("asset_params_get", 1, 2, Mode.Application)

Op.__module__ = "pyteal"
