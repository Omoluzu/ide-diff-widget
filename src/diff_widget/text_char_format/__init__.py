from .blue import BlueTextCharFormat as Blue
from .orange import OrangeTextCharFormat as Orange
from .violet import VioletTextCharFormat as Violet
from .green import GreenTextCharFormat as Green
from .gray import GrayTextCharFormat as Gray
from .plum import PlumTextCharFormat as Plum


keywords = {
    'py': {
        r"\breturn\b": Orange,
        r"\bclass\b": Orange,
        r"\bfrom\b": Orange,
        r"\bimport\b": Orange,
        r"\bself\b": Violet,
        r"\bin\b": Orange,
        r"\bif\b": Orange,
        r"\bsuper\b": Blue,
        r"\belse\b": Blue,
        r"\bwhile\b": Orange,
        r"\bfor\b": Orange,
        r"\bdef [^(]*\b": Blue,
        r"\bdef\b": Orange,
        r"([^\(\[]?)\"(.*?)\"": Green,
        r"([^\(\[]?)\'(.*?)\'": Green,
        r"__(.*?)__": Plum,
        r"@@(.*?)@@": Gray,
        r"(-|\+){3} .*\b": Gray,
    }
}
