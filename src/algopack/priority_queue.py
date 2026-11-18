import math
from dataclasses import dataclass, field

from algopack.errors import EmptyStructureError, InvalidInputError


@dataclass(order=True)
class _Entry[T]:
    priority: float
    order: int
    item: T = field(compare=False)


@dataclass
class PriorityQueue[T]:
    """Min priority queue on heap, equal priorities go FIFO"""

    _heap: list[_Entry[T]] = field(default_factory=list, init=False, repr=False)
    _counter: int = field(default=0, init=False, repr=False)

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def push(self, item: T, priority: float) -> None:
        """Add item with priority"""
        if (
            isinstance(priority, bool)
            or not isinstance(priority, int | float)
            or math.isnan(priority)
        ):
            raise InvalidInputError(message=f"priority must be a number: {priority!r}")
        self._heap.append(_Entry(priority=priority, order=self._counter, item=item))
        self._counter += 1
        self._sift_up(index=len(self._heap) - 1)

    def pop(self) -> T:
        """Remove and return item with smallest priority"""
        if not self._heap:
            raise EmptyStructureError(operation="pop")
        top = self._heap[0]
        last = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._sift_down(index=0)
        return top.item

    def peek(self) -> T:
        """Return next item without removing it"""
        if not self._heap:
            raise EmptyStructureError(operation="peek")
        return self._heap[0].item

    def is_valid_heap(self) -> bool:
        """Check heap invariant, parent is not bigger than children"""
        return all(
            not self._heap[i] < self._heap[(i - 1) // 2]
            for i in range(1, len(self._heap))
        )

    def _sift_up(self, index: int) -> None:
        heap = self._heap
        while index > 0:
            parent = (index - 1) // 2
            if not heap[index] < heap[parent]:
                break
            heap[index], heap[parent] = heap[parent], heap[index]
            index = parent

    def _sift_down(self, index: int) -> None:
        heap = self._heap
        size = len(heap)
        while True:
            smallest = index
            for child in (2 * index + 1, 2 * index + 2):
                if child < size and heap[child] < heap[smallest]:
                    smallest = child
            if smallest == index:
                break
            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest
