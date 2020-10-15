import securities


def test_builds_securities_from_raw_data():
    raw_securities = [
        {'id': '1', 'symbol': 'ABC'}, {'id': '2', 'symbol': 'BCD'}
    ]
    raw_attributes = [
        {'id': '1', 'name': 'price'}, {'id': '2', 'name': 'eps'},
        {'id': '3', 'name': 'dps'}, {'id': '4', 'name': 'sales'},
        {'id': '5', 'name': 'ebitda'}, {'id': '6', 'name': 'free_cash_flow'},
        {'id': '7', 'name': 'assets'}, {'id': '8', 'name': 'liabilities'},
        {'id': '9', 'name': 'debt'}, {'id': '10', 'name': 'shares'}
    ]
    raw_facts = [
        {'security_id': '1', 'attribute_id': '1', 'value': '1.0'},
        {'security_id': '1', 'attribute_id': '2', 'value': '2.0'},
        {'security_id': '1', 'attribute_id': '3', 'value': '3.0'},
        {'security_id': '1', 'attribute_id': '4', 'value': '4.0'},
        {'security_id': '1', 'attribute_id': '5', 'value': '5.0'},
        {'security_id': '1', 'attribute_id': '6', 'value': '6.0'},
        {'security_id': '1', 'attribute_id': '7', 'value': '7.0'},
        {'security_id': '1', 'attribute_id': '8', 'value': '8.0'},
        {'security_id': '1', 'attribute_id': '9', 'value': '9.0'},
        {'security_id': '1', 'attribute_id': '10', 'value': '10.0'},
        {'security_id': '2', 'attribute_id': '1', 'value': '2.0'},
        {'security_id': '2', 'attribute_id': '2', 'value': '4.0'},
        {'security_id': '2', 'attribute_id': '3', 'value': '6.0'},
        {'security_id': '2', 'attribute_id': '4', 'value': '8.0'},
        {'security_id': '2', 'attribute_id': '5', 'value': '10.0'},
        {'security_id': '2', 'attribute_id': '6', 'value': '12.0'},
        {'security_id': '2', 'attribute_id': '7', 'value': '14.0'},
        {'security_id': '2', 'attribute_id': '8', 'value': '16.0'},
        {'security_id': '2', 'attribute_id': '9', 'value': '18.0'},
        {'security_id': '2', 'attribute_id': '10', 'value': '20.0'}
    ]

    s = securities.build_securities(raw_securities, raw_attributes, raw_facts)
    assert len(s) == 2

    abc = s['ABC']
    bcd = s['BCD']

    assert abc.price == 1.0
    assert abc.eps == 2.0
    assert abc.dps == 3.0
    assert abc.sales == 4.0
    assert abc.ebitda == 5.0
    assert abc.free_cash_flow == 6.0
    assert abc.assets == 7.0
    assert abc.liabilities == 8.0
    assert abc.debt == 9.0
    assert abc.shares == 10.0

    assert bcd.price == 2.0
    assert bcd.eps == 4.0
    assert bcd.dps == 6.0
    assert bcd.sales == 8.0
    assert bcd.ebitda == 10.0
    assert bcd.free_cash_flow == 12.0
    assert bcd.assets == 14.0
    assert bcd.liabilities == 16.0
    assert bcd.debt == 18.0
    assert bcd.shares == 20.0
