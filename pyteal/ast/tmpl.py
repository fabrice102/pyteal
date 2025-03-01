from ..types import TealType, valid_tmpl
from ..ir import TealOp, Op, TealBlock
from ..errors import TealInternalError
from .leafexpr import LeafExpr

class Tmpl(LeafExpr):
    """Template expression for creating placeholder values."""

    def __init__(self, op: Op, type: TealType, name: str) -> None:
        valid_tmpl(name)
        self.op = op
        self.type = type
        self.name = name

    def __str__(self):
        return "(Tmpl {} {})".format(self.op, self.name)

    def __teal__(self):
        op = TealOp(self.op, self.name)
        return TealBlock.FromOp(op)

    def type_of(self):
        return self.type

    @classmethod
    def Int(cls, placeholder: str):
        """Create a new Int template.

        Args:
            placeholder: The name to use for this template variable. Must start with `TMPL_` and
                only consist of uppercase alphanumeric characters and underscores.
        """
        return cls(Op.int, TealType.uint64, placeholder)

    @classmethod
    def Bytes(cls, placeholder: str):
        """Create a new Bytes template.

        Args:
            placeholder: The name to use for this template variable. Must start with `TMPL_` and
                only consist of uppercase alphanumeric characters and underscores.
        """
        return cls(Op.byte, TealType.bytes, placeholder)

    @classmethod
    def Addr(cls, placeholder: str):
        """Create a new Addr template.
        
        Args:
            placeholder: The name to use for this template variable. Must start with `TMPL_` and
                only consist of uppercase alphanumeric characters and underscores.
        """
        return cls(Op.addr, TealType.bytes, placeholder)

Tmpl.__module__ = "pyteal"
