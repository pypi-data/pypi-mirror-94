from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class StudentSummary:
    id: str
    name: str = field(compare=False)
    gender: str = field(compare=False)


@dataclass
class Student(StudentSummary):
    gradeId: str = field(repr=False, compare=False)
    classId: str = field(repr=False, compare=False)
    birthday: Optional[str] = field(default=None, repr=False, compare=False)
    eduid: Optional[str] = field(default=None, repr=False, compare=False)
    photos: Optional[List[str]] = field(default=None, repr=False)
