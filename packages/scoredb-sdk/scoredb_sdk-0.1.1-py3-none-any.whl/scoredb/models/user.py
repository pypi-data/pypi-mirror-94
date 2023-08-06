from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class User:
    id: int
    name: str = field(compare=False)
    email: str = field(compare=False)
    created_at: str = field(repr=False, compare=False)
    avatar: Optional[str] = field(default=None, repr=False, compare=False)
    roles: List[str] = field(default_factory=list, repr=False, compare=False)

    def check_access(self, roles: List[str]):
        if 'admin' in self.roles:
            return True
        for role in roles:
            if role not in self.roles:
                return False
        return True
