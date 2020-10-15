#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import dataclasses
import json
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Union


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


class Interpreter:
    def __init__(self, securities: Dict[str, Security]) -> None:
        self._securities = securities

    def execute(self, query: Dict) -> float:
        security = self._securities[query['security']]
        expression_tree = self._parse(query['expression'], security)
        return self._evaluate(expression_tree)

    def _parse(self, expression: Dict, security: Security) -> Dict:
        return {
            'operator': expression['fn'],
            'a': self._evaluate_operand(expression['a'], security),
            'b': self._evaluate_operand(expression['b'], security),
        }

    def _evaluate_operand(
            self, expression: Union[int, float, str, Dict], security: Security
    ) -> Union[float, str, Dict]:
        if type(expression) == dict:
            return self._parse(expression, security)
        elif type(expression) == float or type(expression) == int:
            return float(expression)
        else:
            return dataclasses.asdict(security)[expression]

    def _evaluate(self, expression: Union[float, str, Dict]) -> float:
        if type(expression) == float:
            return expression

        operations = {
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
        }

        return operations[expression['operator']](
            self._evaluate(expression['a']),
            self._evaluate(expression['b'])
        )


def load_csv(path: str) -> List[Dict]:
    with open(path, 'r') as f:
        in_file = csv.DictReader(f)
        lines = [row for row in in_file]
    return lines


def main() -> None:
    """Currently only supports happy path."""
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='the query to perform')
    args = parser.parse_args()

    raw_securities = load_csv('securities.csv')
    raw_attributes = load_csv('attributes.csv')
    raw_facts = load_csv('facts.csv')

    securities = build_securities(raw_securities, raw_attributes, raw_facts)
    interpreter = Interpreter(securities)
    result = interpreter.execute(json.loads(args.query))
    print(result)


if __name__ == '__main__':
    main()
