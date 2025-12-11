import pytest

from src.data_structures import Queue, Stack


def test_stack_push_pop_min():
    st = Stack[int]([3, 1])
    st.push(2)
    assert st.min() == 1
    assert st.peek() == 2
    assert st.pop() == 2
    assert st.min() == 1
    assert len(st) == 2
    assert not st.is_empty()
    st.pop()
    st.pop()
    assert st.is_empty()
    with pytest.raises(IndexError):
        st.pop()
    with pytest.raises(IndexError):
        st.min()
    with pytest.raises(IndexError):
        st.peek()


def test_queue_basic():
    q = Queue[int]([1])
    q.enqueue(1)
    q.enqueue(2)
    assert q.front() == 1
    assert q.dequeue() == 1
    q.enqueue(3)
    assert len(q) == 3
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.front()
