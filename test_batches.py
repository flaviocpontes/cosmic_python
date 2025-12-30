from datetime import date

from model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty) -> tuple[Batch, OrderLine]:
    return (
        Batch(ref="batch-001", sku=sku, qty=batch_qty, eta=date.today()),
        OrderLine(orderId="order-123", sku=sku, qty=line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch("batch-001", "SMALL-TABLE", qty=20, eta=date.today())
    line = OrderLine("order-ref", "SMALL-TABLE", 2)

    batch.allocate(line)

    assert batch.available_quantity == 18

def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line("LARGE-TABLE", 10, 2)
    assert large_batch.can_allocate(small_line)

def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line("SMALL-TABLE", 10, 20)
    assert small_batch.can_allocate(large_line) is False

def test_can_allocate_if_available_equal_to_required():
    small_batch, small_line = make_batch_and_line("SMALL-TABLE", 10, 10)
    assert small_batch.can_allocate(small_line)

def test_cannot_allocate_if_skus_do_not_match():
    small_batch, large_line = make_batch_and_line("SMALL-TABLE", 20, 10)
    different_sku_line = OrderLine("order-123", "WRONG-TABLE", 20)
    assert small_batch.can_allocate(different_sku_line) is False

def test_an_only_deallocate_allocated_lines():
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 10)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 20