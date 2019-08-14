# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.refactoring import (
    FalsyConstantCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import (
    WrongConstantCompareVisitor,
)

wrong_comparators = (
    ('some', '[]'),
    ('some', '{}'),  # noqa: P103
    ('some', '()'),
    ('[]', 'some'),
    ('{}', 'some'),  # noqa: P103
    ('()', 'some'),
)


@pytest.mark.parametrize('comparators', wrong_comparators)
def test_falsy_constant(
    assert_errors,
    parse_ast_tree,
    comparators,
    eq_conditions,
    default_options,
):
    """Testing that compares with falsy contants are not allowed."""
    tree = parse_ast_tree(eq_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [FalsyConstantCompareViolation])


@pytest.mark.parametrize('comparators', wrong_comparators)
def test_falsy_constant_not_eq(
    assert_errors,
    parse_ast_tree,
    comparators,
    other_conditions,
    default_options,
):
    """Testing that compares with falsy contants are not allowed."""
    tree = parse_ast_tree(other_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('comparators', [
    ('some', '[1, 2]'),
    ('some', '{1, 2}'),
    ('some', '{"1": 2}'),
    ('some', '(1, 2)'),
    ('some', 'None'),
    ('some', 'False'),
    ('some', 'True'),
    ('some', '0'),
    ('some', '1'),
    ('some', '""'),
    ('some', '"a"'),
    ('some', 'other'),
    ('some', 'other()'),
    ('some', 'other.attr'),
    ('some', 'other.method()'),
    ('some', 'other[0]'),

    ('None', 'some'),
])
def test_correct_constant_compare(
    assert_errors,
    parse_ast_tree,
    comparators,
    simple_conditions,
    default_options,
):
    """Testing that normal compares are allowed."""
    tree = parse_ast_tree(simple_conditions.format(*comparators))

    visitor = WrongConstantCompareVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])