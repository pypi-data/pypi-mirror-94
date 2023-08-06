from dataclasses import dataclass, field
from typing import List

from .student import StudentSummary


@dataclass
class ClassSummary:
    id: str
    studentsCount: int = field(repr=False, compare=False)


@dataclass
class Class(ClassSummary):
    gradeId: str = field(repr=False, compare=False)
    students: List[StudentSummary] = field(repr=False, compare=False)
