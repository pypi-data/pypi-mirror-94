from __future__ import annotations

from typing import Optional, Generic, Callable, TypeVar, List

T = TypeVar('T')


class Pagination(Generic[T]):

    def __init__(self, data: List[T], current_page: int, pages: int,
                 switch_page_fn: Optional[Callable[[int], Pagination[T]]] = None):
        self.data = data
        self.pages = pages
        self.current_page = current_page
        if self.pages < 1:
            raise ValueError('Number of pages cannot be less than one.')
        if self.current_page < 1 or self.current_page > self.pages:
            raise ValueError('Invalid current page number.')
        self.switch_page_fn = switch_page_fn

    def count(self):
        return len(self.data)

    def has_previous_page(self):
        return self.current_page > 1

    def has_next_page(self):
        return self.current_page < self.pages

    def previous_page(self):
        if not self.has_previous_page():
            raise IndexError('No previous page available.')
        if not self.switch_page_fn:
            raise NotImplementedError('No switch page function defined.')
        return self.switch_page_fn(self.current_page - 1)

    def next_page(self):
        if not self.has_next_page():
            raise IndexError('No next page available.')
        if not self.switch_page_fn:
            raise NotImplementedError('No switch page function defined.')
        return self.switch_page_fn(self.current_page + 1)
