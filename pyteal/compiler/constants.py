from typing import List, DefaultDict
from collections import defaultdict

from ..ir import Op, TealOp, TealLabel, TealComponent, TealBlock, TealSimpleBlock, TealConditionalBlock
from ..errors import TealInternalError

def createConstantBlocks(ops: List[TealComponent]) -> List[TealComponent]:
    intFreqs: DefaultDict[int, int] = defaultdict(int)
    byteFreqs: DefaultDict[str, int] = defaultdict(int)

    for op in ops:
        if not isinstance(op, TealOp):
            continue
        
        basicOp = op.getOp()

        if basicOp == Op.int:
            intValue = op.args[0]
            if type(intValue) != int:
                raise TealInternalError('Invalid integer constant')
            intFreqs[intValue] += 1
        elif basicOp == Op.byte:
            byteValue = op.args[0]
            if type(byteValue) != str:
                raise TealInternalError('Invalid byte constant')
            byteFreqs[byteValue] += 1
    
    assembled: List[TealComponent] = []
    sortedInts = sorted(intFreqs.keys(), key=lambda x: intFreqs[x], reverse=True)
    sortedBytes = sorted(byteFreqs.keys(), key=lambda x: byteFreqs[x], reverse=True)

    if len(intFreqs) != 0:
        assembled.append(TealOp(Op.intcblock, *sortedInts))
    
    if len(byteFreqs) != 0:
        assembled.append(TealOp(Op.bytecblock, *sortedBytes))
    
    for op in ops:
        if isinstance(op, TealOp):
            basicOp = op.getOp()

            if basicOp == Op.int:
                intValue = op.args[0]
                index = sortedInts.index(intValue)
                if index == 0:
                    assembled.append(TealOp(Op.intc_0))
                elif index == 1:
                    assembled.append(TealOp(Op.intc_1))
                elif index == 2:
                    assembled.append(TealOp(Op.intc_2))
                elif index == 3:
                    assembled.append(TealOp(Op.intc_3))
                else:
                    assembled.append(TealOp(Op.intc, index))
                continue
            
            if basicOp == Op.byte:
                byteValue = op.args[0]
                index = sortedBytes.index(byteValue)
                if index == 0:
                    assembled.append(TealOp(Op.bytec_0))
                elif index == 1:
                    assembled.append(TealOp(Op.bytec_1))
                elif index == 2:
                    assembled.append(TealOp(Op.bytec_2))
                elif index == 3:
                    assembled.append(TealOp(Op.bytec_3))
                else:
                    assembled.append(TealOp(Op.bytec, index))
                continue
                
        assembled.append(op)
    
    return assembled
