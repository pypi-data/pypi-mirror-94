from dataclasses import dataclass, field
from typing import List

from .class_ import ClassSummary


@dataclass
class GradeSummary:
    id: str
    classesCount: int = field(repr=False, compare=False)
    studentsCount: int = field(repr=False, compare=False)


@dataclass
class Grade(GradeSummary):
    classes: List[ClassSummary] = field(repr=False, compare=False)
