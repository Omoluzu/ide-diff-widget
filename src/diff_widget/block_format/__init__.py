from .plus import PlusTextBlockFormat as Plus
from .diff import DiffTextBlockFormat as Diff
from .minus import MinusTextBlockFormat as Minus
from .simple import SimpleTextBlockFormat as Simple
from .open_block import OpenBlockTextBlockFormat as OpenBlock


keywords = {
    "+ ": Plus,
    "+": Plus,
    "- ": Minus,
    "-": Minus,
    " @": Diff,
    "@@": Diff,
}
