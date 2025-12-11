from __future__ import annotations
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """Стек на списке с поддержкой min() за O(1)."""

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self.data: list[T] = []
        self.mins: list[T] = []
        if items:
            for item in items:
                self.push(item)

    def push(self, x: T) -> None:
        self.data.append(x)
        if not self.mins or x <= self.mins[-1]:
            self.mins.append(x)

    def pop(self) -> T:
        if not self.data:
            raise IndexError("pop from empty stack")
        val = self.data.pop()
        if self.mins and val == self.mins[-1]:
            self.mins.pop()
        return val

    def peek(self) -> T:
        if not self.data:
            raise IndexError("peek from empty stack")
        return self.data[-1]

    def is_empty(self) -> bool:
        return not self.data

    def __len__(self) -> int:  # pragma: no cover - тривиально
        return len(self.data)

    def min(self) -> T:
        if not self.mins:
            raise IndexError("min from empty stack")
        return self.mins[-1]


class Queue(Generic[T]):
    """Очередь на двух стеках (in/out) с амортизированным O(1) dequeue."""

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self.in_stack: list[T] = []
        self.out_stack: list[T] = []
        if items:
            for item in items:
                self.enqueue(item)

    def _shift(self) -> None:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def enqueue(self, x: T) -> None:
        self.in_stack.append(x)

    def dequeue(self) -> T:
        self._shift()
        if not self.out_stack:
            raise IndexError("dequeue from empty queue")
        return self.out_stack.pop()

    def front(self) -> T:
        self._shift()
        if not self.out_stack:
            raise IndexError("front from empty queue")
        return self.out_stack[-1]

    def is_empty(self) -> bool:
        return not (self.in_stack or self.out_stack)

    def __len__(self) -> int:  # pragma: no cover - тривиально
        return len(self.in_stack) + len(self.out_stack)
