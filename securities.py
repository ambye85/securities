#!/usr/bin/env python
from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List


def build_securities(
        raw_securities: List[Dict],
        raw_attributes: List[Dict],
        raw_facts: List[Dict]
) -> Dict[str, Security]:
    securities = {security['id']: security['symbol'] for security in raw_securities}
    attributes = {attr['id']: attr['name'] for attr in raw_attributes}
    facts = defaultdict(dict)
    for fact in raw_facts:
        security_id = securities[fact['security_id']]
        attribute_id = attributes[fact['attribute_id']]
        value = float(fact['value'])
        facts[security_id][attribute_id] = value

    return {symbol: Security(symbol, **attrs) for symbol, attrs in facts.items()}


@dataclass(frozen=True)
class Security:
    symbol: str
    price: float
    eps: float
    dps: float
    sales: float
    ebitda: float
    free_cash_flow: float
    assets: float
    liabilities: float
    debt: float
    shares: float


def load_csv(path: str) -> List[Dict]:
    with open(path, 'r') as f:
        in_file = csv.DictReader(f)
        lines = [row for row in in_file]
    return lines


def main():
    raw_securities = load_csv('securities.csv')
    raw_attributes = load_csv('attributes.csv')
    raw_facts = load_csv('facts.csv')

    securities = build_securities(raw_securities, raw_attributes, raw_facts)
    print(securities)


if __name__ == '__main__':
    main()
