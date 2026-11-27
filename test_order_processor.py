# Characterization tests for order_processor.py
# These tests capture the CURRENT behavior of the code before refactoring
# Purpose: ensure refactoring does not change observable behavior

from order_processor import proc


def test_standard_order_no_discount():
    order = {
        "id": 1,
        "items": [{"p": 10.00, "q": 2}, {"p": 5.00, "q": 1}],
        "c": "REGULAR"
    }
    # subtotal = 10*2 + 5*1 = 25.00, no discount
    # tax = 25.00 * 0.08 = 2.00
    # total = 27.00
    result = proc(order)

    assert result["order_id"] == 1
    assert result["sub"] == 25.00
    assert result["tax"] == 2.00
    assert result["total"] == 27.00
    assert result["st"] == "COMPLETED"


def test_vip_order_applies_10_percent_discount():
    order = {
        "id": 2,
        "items": [{"p": 29.99, "q": 2}, {"p": 9.99, "q": 1}],
        "c": "VIP"
    }
    # subtotal = 29.99*2 + 9.99*1 = 69.97
    # VIP discount 10%: 69.97 - 6.997 = 62.973 -> round = 62.97
    # tax = 62.97 * 0.08 = 5.0376 -> round = 5.04
    # total = 62.97 + 5.04 = 68.01
    result = proc(order)

    assert result["order_id"] == 2
    assert result["sub"] == 62.97
    assert result["tax"] == 5.04
    assert result["total"] == 68.01
    assert result["st"] == "COMPLETED"


def test_employee_order_applies_20_percent_discount():
    order = {
        "id": 3,
        "items": [{"p": 100.00, "q": 1}],
        "c": "EMPLOYEE"
    }
    # subtotal = 100.00
    # EMPLOYEE discount 20%: 100.00 - 20.00 = 80.00
    # tax = 80.00 * 0.08 = 6.40
    # total = 86.40
    result = proc(order)

    assert result["order_id"] == 3
    assert result["sub"] == 80.00
    assert result["tax"] == 6.40
    assert result["total"] == 86.40
    assert result["st"] == "COMPLETED"


def test_empty_items_list_sets_empty_status():
    order = {
        "id": 4,
        "items": [],
        "c": "REGULAR"
    }
    result = proc(order)

    assert result["order_id"] == 4
    assert result["sub"] == 0
    assert result["tax"] == 0
    assert result["total"] == 0
    assert result["st"] == "EMPTY"


def test_negative_quantity_is_treated_as_zero():
    order = {
        "id": 5,
        "items": [{"p": 10.00, "q": -5}, {"p": 20.00, "q": 1}],
        "c": "REGULAR"
    }
    # negative q clamped to 0, so first item contributes 0
    # subtotal = 0 + 20.00*1 = 20.00
    # tax = 20.00 * 0.08 = 1.60
    # total = 21.60
    result = proc(order)

    assert result["order_id"] == 5
    assert result["sub"] == 20.00
    assert result["tax"] == 1.60
    assert result["total"] == 21.60
    assert result["st"] == "COMPLETED"
