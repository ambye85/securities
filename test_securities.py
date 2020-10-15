import json

import securities

RAW_SECURITIES = [
    {'id': '1', 'symbol': 'ABC'}, {'id': '2', 'symbol': 'BCD'},
]
RAW_ATTRIBUTES = [
    {'id': '1', 'name': 'price'}, {'id': '2', 'name': 'eps'},
    {'id': '3', 'name': 'dps'}, {'id': '4', 'name': 'sales'},
    {'id': '5', 'name': 'ebitda'}, {'id': '6', 'name': 'free_cash_flow'},
    {'id': '7', 'name': 'assets'}, {'id': '8', 'name': 'liabilities'},
    {'id': '9', 'name': 'debt'}, {'id': '10', 'name': 'shares'},
]
RAW_FACTS = [
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
    {'security_id': '2', 'attribute_id': '10', 'value': '20.0'},
]


def test_builds_securities_from_raw_data():
    s = securities.build_securities(RAW_SECURITIES, RAW_ATTRIBUTES, RAW_FACTS)

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


def test_multiplication_query():
    query = """{
        "expression": {"fn": "*", "a": "sales", "b": 2},
        "security": "ABC"
    }"""

    s = securities.build_securities(RAW_SECURITIES, RAW_ATTRIBUTES, RAW_FACTS)

    interpreter = securities.Interpreter(s)
    result = interpreter.execute(json.loads(query))

    assert result == 8.0


def test_division_query():
    query = """{
        "expression": {"fn": "/", "a": "price", "b": "eps"},
        "security": "BCD"
    }"""

    s = securities.build_securities(RAW_SECURITIES, RAW_ATTRIBUTES, RAW_FACTS)

    interpreter = securities.Interpreter(s)
    result = interpreter.execute(json.loads(query))

    assert result == 0.5


def test_addition_query():
    query = """{
        "expression": {"fn": "+", "a": "liabilities", "b": "debt"},
        "security": "ABC"
    }"""

    s = securities.build_securities(RAW_SECURITIES, RAW_ATTRIBUTES, RAW_FACTS)

    interpreter = securities.Interpreter(s)
    result = interpreter.execute(json.loads(query))

    assert result == 17.0


def test_subtraction_query():
    query = """{
        "expression": {"fn": "-", "a": "sales", "b": "debt"},
        "security": "BCD"
    }"""

    s = securities.build_securities(RAW_SECURITIES, RAW_ATTRIBUTES, RAW_FACTS)

    interpreter = securities.Interpreter(s)
    result = interpreter.execute(json.loads(query))

    assert result == -10.0


def test_nested_expressions_query():
    raw_securities = [
        {'id': '3', 'symbol': 'CDE'},
    ]
    raw_facts = [
        {'security_id': '3', 'attribute_id': '1', 'value': '3.0'},
        {'security_id': '3', 'attribute_id': '2', 'value': '6.0'},
        {'security_id': '3', 'attribute_id': '3', 'value': '9.0'},
        {'security_id': '3', 'attribute_id': '4', 'value': '12.0'},
        {'security_id': '3', 'attribute_id': '5', 'value': '15.0'},
        {'security_id': '3', 'attribute_id': '6', 'value': '18.0'},
        {'security_id': '3', 'attribute_id': '7', 'value': '21.0'},
        {'security_id': '3', 'attribute_id': '8', 'value': '24.0'},
        {'security_id': '3', 'attribute_id': '9', 'value': '27.0'},
        {'security_id': '3', 'attribute_id': '10', 'value': '30.0'},
    ]

    query = """{
        "expression": {
            "fn": "-", 
            "a": {"fn": "-", "a": "eps", "b": "shares"}, 
            "b": {"fn": "-", "a": "assets", "b": "liabilities"}
        },
        "security": "CDE"
    }"""

    s = securities.build_securities(raw_securities, RAW_ATTRIBUTES, raw_facts)

    interpreter = securities.Interpreter(s)
    result = interpreter.execute(json.loads(query))

    assert result == -21.0
