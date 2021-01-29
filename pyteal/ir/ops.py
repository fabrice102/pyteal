from enum import Enum, Flag, auto

class Mode(Flag):
    """Enum of program running modes."""
    
    Signature = auto()
    Application = auto()

Mode.__module__ = "pyteal"

class Op(Enum):
    """Enum of program opcodes."""

    err = "err", 0, 0, Mode.Signature | Mode.Application
    sha256 = "sha256", 1, 1, Mode.Signature | Mode.Application
    keccak256 = "keccak256", 1, 1, Mode.Signature | Mode.Application
    sha512_256 = "sha512_256", 1, 1, Mode.Signature | Mode.Application
    ed25519verify = "ed25519verify", 3, 1, Mode.Signature
    add = "+", 2, 1, Mode.Signature | Mode.Application
    minus = "-", 2, 1, Mode.Signature | Mode.Application
    div = "/", 2, 1, Mode.Signature | Mode.Application
    mul = "*", 2, 1, Mode.Signature | Mode.Application
    lt = "<", 2, 1, Mode.Signature | Mode.Application
    gt = ">", 2, 1, Mode.Signature | Mode.Application
    le = "<=", 2, 1, Mode.Signature | Mode.Application
    ge = ">=", 2, 1, Mode.Signature | Mode.Application
    logic_and = "&&", 2, 1, Mode.Signature | Mode.Application
    logic_or = "||", 2, 1, Mode.Signature | Mode.Application
    eq = "==", 2, 1, Mode.Signature | Mode.Application
    neq = "!=", 2, 1, Mode.Signature | Mode.Application
    logic_not = "!", 1, 1, Mode.Signature | Mode.Application
    len = "len", 1, 1, Mode.Signature | Mode.Application
    itob = "itob", 1, 1, Mode.Signature | Mode.Application
    btoi = "btoi", 1, 1, Mode.Signature | Mode.Application
    mod = "%", 2, 1, Mode.Signature | Mode.Application
    bitwise_or = "|", 2, 1, Mode.Signature | Mode.Application
    bitwise_and = "&", 2, 1, Mode.Signature | Mode.Application
    bitwise_xor = "^", 2, 1, Mode.Signature | Mode.Application
    bitwise_not = "~", 1, 1, Mode.Signature | Mode.Application
    mulw = "mulw", 2, 2, Mode.Signature | Mode.Application
    addw = "addw", 2, 2, Mode.Signature | Mode.Application
    int = "int", 0, 1, Mode.Signature | Mode.Application
    byte = "byte", 0, 1, Mode.Signature | Mode.Application
    addr = "addr", 0, 1, Mode.Signature | Mode.Application
    arg = "arg", 0, 1, Mode.Signature
    txn = "txn", 0, 1, Mode.Signature | Mode.Application
    global_ = "global", 0, 1, Mode.Signature | Mode.Application
    gtxn = "gtxn", 0, 1, Mode.Signature | Mode.Application
    load = "load", 0, 1, Mode.Signature | Mode.Application
    store = "store", 1, 0, Mode.Signature | Mode.Application
    txna = "txna", 0, 1, Mode.Signature | Mode.Application
    gtxna = "gtxna", 0, 1, Mode.Signature | Mode.Application
    bnz = "bnz", 1, 0, Mode.Signature | Mode.Application
    bz = "bz", 1, 0, Mode.Signature | Mode.Application
    b = "b", 0, 0, Mode.Signature | Mode.Application
    return_ = "return", 1, 0, Mode.Signature | Mode.Application
    pop = "pop", 1, 0, Mode.Signature | Mode.Application
    dup = "dup", 1, 2, Mode.Signature | Mode.Application
    dup2 = "dup2", 2, 4, Mode.Signature | Mode.Application
    concat = "concat", 2, 1, Mode.Signature | Mode.Application
    substring = "substring", 1, 1, Mode.Signature | Mode.Application
    substring3 = "substring3", 3, 1, Mode.Signature | Mode.Application
    balance = "balance", 1, 1, Mode.Application
    app_opted_in = "app_opted_in", 2, 1, Mode.Application
    app_local_get = "app_local_get", 2, 1, Mode.Application
    app_local_get_ex = "app_local_get_ex", 3, 1, Mode.Application
    app_global_get = "app_global_get", 1, 1, Mode.Application
    app_global_get_ex = "app_global_get_ex", 2, 1, Mode.Application
    app_local_put = "app_local_put", 3, 0, Mode.Application
    app_global_put = "app_global_put", 2, 0, Mode.Application
    app_local_del = "app_local_del", 2, 0, Mode.Application
    app_global_del = "app_global_del", 1, 0, Mode.Application
    asset_holding_get = "asset_holding_get", 2, 2, Mode.Application
    asset_params_get = "asset_params_get", 1, 2, Mode.Application

    def __new__(cls, value: str, pops: int, pushes: int, mode: Mode):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, value: str, pops: int, pushes: int, mode: Mode):
        self.pops = pops
        self.pushes = pushes
        self.mode = mode

Op.__module__ = "pyteal"
