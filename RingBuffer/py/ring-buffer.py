class RingBuffer:
    def __init__(self, size: int) -> None:
        if size <= 0:
            raise ValueError("Size must be positive")
        self.size: int = size
        self.buffer: list[str] = [""] * size
        self.head: int = 0
        self.tail: int = 0
        self.count: int = 0

    def _next_position(self, pos: int) -> int:
        return (pos + 1) % self.size

    def insert(self, data: str) -> None:
        if len(data) > self.size - self.count:
            raise BufferError(
                f"Not enough space: need {len(data)}, available {self.size - self.count}"
            )

        for c in data:
            self.buffer[self.head] = c
            self.head = self._next_position(self.head)
            self.count += 1

    def dequeue(self, n: int) -> str:
        if n < 0:
            raise ValueError("Cannot dequeue a negative number of items")
        if n > self.count:
            raise BufferError(
                f"Not enough data: requested {n}, available {self.count}"
            )

        buf: list[str] = []
        for _ in range(n):
            buf.append(self.buffer[self.tail])
            self.tail = self._next_position(self.tail)
            self.count -= 1
        return "".join(buf)

    def peek(self) -> str:
        if self.is_empty():
            raise IndexError("Buffer is empty")
        return self.buffer[self.tail]

    def is_empty(self) -> bool:
        return self.count == 0

    def is_full(self) -> bool:
        return self.count == self.size

    def inspect(self) -> list[str]:
        return self.buffer
    
    
if __name__ == "__main__":
    r = RingBuffer(16)
    r.insert("Hello")
    r.insert("Hello")
    print(r.dequeue(16))