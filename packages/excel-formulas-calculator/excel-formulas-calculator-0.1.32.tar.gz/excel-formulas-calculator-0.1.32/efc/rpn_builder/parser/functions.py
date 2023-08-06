# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import re
from functools import wraps

from six import integer_types, string_types
from six.moves import range, zip_longest

from efc.rpn_builder.parser.operands import (
    BadReference, CellRangeOperand, CellSetOperand, EmptyOperand, ErrorOperand, NamedRangeOperand, NotFoundErrorOperand,
    RPNOperand, SetOperand, SimpleOperand, SimpleSetOperand, SingleCellOperand, ValueErrorOperand, ValueNotAvailable,
)
from efc.utils import is_float

__all__ = ('EXCEL_FUNCTIONS',)


def _get_type_id(obj):
    if isinstance(obj, bool):
        return 2
    elif isinstance(obj, string_types):
        return 1
    return 0


def type_mixin(a, b):
    if a is None:
        a_type = (1, '') if isinstance(b, string_types) else (0, 0)
    else:
        a_type = (_get_type_id(a), a)

    if b is None:
        b_type = (1, '') if isinstance(a, string_types) else (0, 0)
    else:
        b_type = (_get_type_id(b), b)
    return a_type, b_type


def set_mixin(foo):
    @wraps(foo)
    def wrapper(op1, op2):
        fill_value = None

        op1_is_set = isinstance(op1, SetOperand)
        op2_is_set = isinstance(op2, SetOperand)

        if op1_is_set or op2_is_set:
            if not op1_is_set:
                op1, fill_value = tuple(), op1
            elif not op2_is_set:
                op2, fill_value = tuple(), op2

            result = SimpleSetOperand()
            for v1, v2 in zip_longest(op1, op2, fillvalue=fill_value):
                result.add_cell(ValueNotAvailable() if v1 is None or v2 is None else SimpleOperand(foo(v1, v2)))
        else:
            result = foo(op1, op2)
        return result

    return wrapper


@set_mixin
def add(op1, op2):
    return op1.digit + op2.digit


def add_func(op1, op2=None):
    if isinstance(op2, EmptyOperand):
        op2 = None

    if op2 is not None:
        return add(op1, op2)
    else:
        return op1.digit


@set_mixin
def sub(op1, op2):
    return op1.digit - op2.digit


def subtract_func(op1, op2=None):
    if isinstance(op2, EmptyOperand):
        op2 = None

    if op2 is not None:
        return sub(op1, op2)
    else:
        return -op1.digit


@set_mixin
def divide_func(op1, op2):
    return op1.digit / op2.digit


@set_mixin
def multiply_func(op1, op2):
    return op1.digit * op2.digit


@set_mixin
def concat_func(op1, op2):
    if isinstance(op1, ErrorOperand):
        raise op1
    if isinstance(op2, ErrorOperand):
        raise op2
    return op1.string + op2.string


@set_mixin
def exponent_func(op1, op2):
    return op1.digit ** op2.digit


@set_mixin
def compare_not_eq_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 != op2


@set_mixin
def compare_gte_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 >= op2


@set_mixin
def compare_lte_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 <= op2


@set_mixin
def compare_gt_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 > op2


@set_mixin
def compare_lt_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 < op2


@set_mixin
def compare_eq_func(op1, op2):
    op1, op2 = type_mixin(op1.value, op2.value)
    return op1 == op2


def iter_elements(*args):
    for arg in args:
        if isinstance(arg, RPNOperand):
            arg = arg.evaluated_value

        if isinstance(arg, (CellRangeOperand, CellSetOperand)):
            for cell in arg:
                yield cell
        else:
            yield arg


def iter_digits(*args):
    for op in iter_elements(*args):
        if not op.is_blank:
            try:
                yield op.digit
            except (ValueError, TypeError):
                pass


def sum_func(*args):
    return sum(d or 0 for d in iter_digits(*args))


def mod_func(op1, op2):
    return op1.digit % op2.digit


def if_func(expr_op, op1, op2=None):
    if isinstance(op2, EmptyOperand):
        op2 = None

    if op2 is None:
        op2 = False
    return op1 if expr_op.value else op2


def if_error_func(op1, op2):
    if isinstance(op1, RPNOperand):
        op1 = op1.evaluated_value
    return op2 if isinstance(op1, ErrorOperand) else op1


def is_error_func(op):
    if isinstance(op, RPNOperand):
        op = op.evaluated_value
    return isinstance(op, ErrorOperand)


def max_func(*args):
    return max(list(d or 0 for d in iter_digits(*args)) or [0])


def min_func(*args):
    return min(list(d or 0 for d in iter_digits(*args)) or [0])


def left_func(op1, op2=1):
    if isinstance(op2, EmptyOperand):
        op2 = 1

    return op1.string[:int(op2)]


def right_func(op1, op2=1):
    if isinstance(op2, EmptyOperand):
        op2 = 1

    return op1.string[-int(op2):]


def mid_func(op1, op2, op3):
    left = int(op2) - 1
    right = left + int(op3)
    return op1.string[left:right]


def is_blank_func(a):
    while True:
        if isinstance(a, (NamedRangeOperand, SingleCellOperand)):
            a = SimpleOperand(a.address_to_value())
        elif isinstance(a, RPNOperand):
            a = a.evaluated_value
        else:
            break

    try:
        it = iter(a)
    except TypeError:
        return a.value is None

    new_set = SimpleSetOperand()
    for v in it:
        new_set.add_cell(SimpleOperand(v.value is None))
    return new_set


def or_function(*args):
    for op in iter_elements(*args):
        v = op.value
        if v is not None and not isinstance(v, string_types) and v:
            return True
    return False


def and_function(*args):
    for op in iter_elements(*args):
        v = op.value
        if v is not None and not isinstance(v, string_types) and not v:
            return False
    return True


def not_func(op):
    return not op.value


def small_function(r, op):
    items = sorted(iter_digits(r))
    index = int(op) - 1
    try:
        return items[index]
    except IndexError:
        return ValueErrorOperand()


def large_function(r, op):
    items = sorted(iter_digits(r), reverse=True)
    index = int(op) - 1
    try:
        return items[index]
    except IndexError:
        return ValueErrorOperand()


def round_function(a, b):
    b = int(b)
    v = round(a.digit, b)
    if b == 0:
        v = int(v)
    return v


def round_down_function(a, b):
    b = int(b)
    base = 10 ** b
    v = a.digit * base // 1 / base
    if b == 0:
        v = int(v)
    return v


def floor_function(a, multiple):
    multiple = int(multiple)
    return int(a.digit / multiple) * multiple


def count_function(*args):
    return len([op for op in iter_elements(*args) if isinstance(op.value, (integer_types, float))])


def abs_function(a):
    return abs(a.digit)


def match_function(op1, r, match_type=None):
    if isinstance(match_type, EmptyOperand):
        match_type = None

    match_type = 0 if match_type is None else int(match_type)

    expr = op1.value
    idx = None
    if match_type == 1:
        for idx, item in enumerate(r, 1):
            a, b = type_mixin(item.value, expr)
            if a == b:
                break
            elif a > b:
                idx -= 1
                break
    elif match_type == -1:
        for idx, item in enumerate(r, 1):
            a, b = type_mixin(item.value, expr)
            if a > b:
                break
        else:
            idx = None
    else:
        for idx, item in enumerate(r, 1):
            a, b = type_mixin(item.value, expr)
            if a == b:
                break
        else:
            idx = None
    if idx is None:
        raise NotFoundErrorOperand()
    return idx


COUNT_IF_EXPR = re.compile(r'^(?P<symbol><=|>=|<>|>|<|=)(?P<value>.+)$')


def get_check_function(expr):
    if isinstance(expr.value, string_types):
        match = COUNT_IF_EXPR.search(expr.value)
        if match:
            match = match.groupdict()
            operation = match['symbol']
            operand = match['value']
        else:
            operation = '='
            operand = expr.value
    else:
        operation = '='
        operand = expr.value

    if is_float(operand):
        operand = float(operand)

    check = ARITHMETIC_FUNCTIONS[operation]
    return check, SimpleOperand(operand)


def countif_function(cells, expr):
    check, operand = get_check_function(expr)
    return len([op for op in cells.value if check(op, operand)])


def counta_function(cells):
    return len([op for op in cells.value if op.value is not None])


def get_checks_from_args(args):
    args = iter(args)
    checks = []
    while True:
        check = []
        try:
            check.append(next(args))
        except StopIteration:
            break

        check.extend(get_check_function(next(args)))
        checks.append(check)
    return checks


def ifs_indexes(*args):
    good_indexes = None

    checks = get_checks_from_args(args)

    for op_range, check, expr in checks:
        check_good_indexes = None
        key = None
        if op_range.source and isinstance(op_range, CellRangeOperand):
            cache = op_range.source.ifs_range_cache

            if cache is not None:
                key = (op_range.ws_name, op_range.row1, op_range.column1, op_range.row2,
                       op_range.column2, check, expr.value)
                check_good_indexes = cache.get(key)
        else:
            cache = None

        if check_good_indexes is None:
            check_good_indexes = set()
            for idx, item in enumerate(op_range, 1):
                if item is None:
                    raise ValueErrorOperand
                else:
                    # convert expr value to item type
                    if isinstance(item.value, string_types) and not isinstance(expr.value, string_types):
                        expr = SimpleOperand(expr.string)
                    elif isinstance(item.value, (integer_types, float)) and not isinstance(expr.value,
                                                                                           (integer_types, float)):
                        try:
                            expr = SimpleOperand(expr.digit)
                        except ValueError:
                            pass

                    if check(item, expr):
                        check_good_indexes.add(idx)

            if cache is not None:
                cache[key] = check_good_indexes

        if good_indexes is None:
            good_indexes = check_good_indexes.copy()
        else:
            good_indexes &= check_good_indexes

        if not good_indexes:
            break

    return good_indexes


def sum_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return sum_func(*(c for idx, c in enumerate(op1, 1) if idx in good_indexes))


def sum_if_function(r, expr, op1):
    return sum_ifs_function(op1, r, expr)


def concatenate(*args):
    return ''.join(i.string for i in iter_elements(*args))


def average_function(*args):
    values = list(iter_digits(*args))
    return sum(values) / len(values)


def average_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return average_function(*(c for idx, c in enumerate(op1, 1) if idx in good_indexes))


def count_blank_function(cells):
    return len([op for op in iter_elements(cells) if op.is_blank])


def count_ifs_function(op1, *args):
    good_indexes = ifs_indexes(*args)
    return count_function(*(c for idx, c in enumerate(op1, 1) if idx in good_indexes))


def offset_function(cell, row_offset, col_offset, height=None, width=None):
    height_is_none = height is None or isinstance(height, EmptyOperand)
    width_is_none = width is None or isinstance(width, EmptyOperand)

    if isinstance(cell, SingleCellOperand):
        height = int(height) if not height_is_none else 1
        width = int(width) if not width_is_none else 1

        column = cell.column
        row = cell.row
    elif isinstance(cell, CellRangeOperand):
        height = int(height) if not height_is_none else cell.row2 - cell.row1 + 1
        width = int(width) if not width_is_none else cell.column2 - cell.column1 + 1

        column = cell.column1
        row = cell.row1
    else:
        return ValueErrorOperand()

    if height == width == 1:
        return SingleCellOperand(row=row + int(row_offset), column=column + int(col_offset),
                                 ws_name=cell.ws_name, source=cell.source)
    else:
        return CellRangeOperand(row1=row + int(row_offset),
                                column1=column + int(col_offset),
                                row2=row + int(row_offset) + height - 1,
                                column2=column + int(col_offset) + width - 1,
                                ws_name=cell.ws_name, source=cell.source)


def vlookup_function(op, rg, column, flag=None):
    if isinstance(flag, EmptyOperand):
        flag = None

    first_col = rg.offset()
    first_col.column2 = first_col.column1

    if flag is not None and flag.digit or flag is None:
        idx = match_function(op, first_col, 1)
        if flag is not None and flag.digit and idx != 1:
            a, b = type_mixin(list(first_col)[idx - 1].value, op.value)
            if a == b:
                idx -= 1
    else:
        idx = match_function(op, first_col, 0)
    return SingleCellOperand(row=(rg.row1 or 1) + idx - 1, column=(rg.column1 or 1) + column.digit - 1,
                             ws_name=rg.ws_name, source=rg.source)


def index_function(rg, row, column=None):
    if isinstance(column, EmptyOperand):
        column = None

    if isinstance(rg, RPNOperand):
        rg = rg.evaluated_value

    if isinstance(rg, SetOperand):
        set_type = SimpleSetOperand
        row1 = 1
        row2 = rg.rows_count
        column1 = 1
        column2 = rg.columns_count
    else:
        set_type = CellSetOperand
        row1 = rg.row1
        row2 = rg.row2
        column1 = rg.column1
        column2 = rg.column2

    rg_size = 2 if row1 != row2 and column1 != column2 else 1

    row = row.digit
    if column is not None:
        column = column.digit
    elif rg_size == 1:
        column = 1

    if rg_size == 1:
        if column1 is not None and column != 1:
            return BadReference()
    else:
        if column is None or row == 0 or column == 0:
            return BadReference()

    if row == 0:
        result = set_type()
        for c in range(column1, column2 + 1):
            result.add_cell(rg.get_cell(1, c))
    elif column == 0:
        result = set_type()
        for r in range(row1, row2 + 1):
            result.add_cell(rg.get_cell(r, 1))
    else:
        result = rg.get_cell(row, column)

    return result


def substitute_func(text, old_text, new_text, instance_num=None):
    if isinstance(instance_num, EmptyOperand):
        instance_num = None

    instance_num = instance_num.digit if instance_num is not None else -1
    return text.string.replace(old_text.string, new_text.string, instance_num)


def search_func(pattern, source, start_position=None):
    if isinstance(start_position, EmptyOperand):
        start_position = None

    try:
        start_position = start_position or 0
        return source.string[start_position:].lower().index(pattern.string.lower())
    except ValueError:
        return ValueErrorOperand()


TRIM_REGEXP = re.compile(r' {2,}')


def trim_func(op):
    value = op.string.strip()
    value = TRIM_REGEXP.sub(' ', value)
    return value


def len_func(op):
    value = op.string
    return len(value)


ARITHMETIC_FUNCTIONS = {
    '+': add_func,
    '-': subtract_func,
    '/': divide_func,
    '*': multiply_func,
    '&': concat_func,
    '^': exponent_func,
    '<>': compare_not_eq_func,
    '>=': compare_gte_func,
    '<=': compare_lte_func,
    '>': compare_gt_func,
    '<': compare_lt_func,
    '=': compare_eq_func,
}

EXCEL_FUNCTIONS = {}
EXCEL_FUNCTIONS.update(ARITHMETIC_FUNCTIONS)

EXCEL_FUNCTIONS['SUM'] = sum_func
EXCEL_FUNCTIONS['SUMIF'] = sum_if_function
EXCEL_FUNCTIONS['SUMIFS'] = sum_ifs_function
EXCEL_FUNCTIONS['MOD'] = mod_func
EXCEL_FUNCTIONS['IF'] = if_func
EXCEL_FUNCTIONS['IFERROR'] = if_error_func
EXCEL_FUNCTIONS['ISERROR'] = is_error_func
EXCEL_FUNCTIONS['MAX'] = max_func
EXCEL_FUNCTIONS['MIN'] = min_func
EXCEL_FUNCTIONS['LEFT'] = left_func
EXCEL_FUNCTIONS['RIGHT'] = right_func
EXCEL_FUNCTIONS['MID'] = mid_func
EXCEL_FUNCTIONS['ISBLANK'] = is_blank_func
EXCEL_FUNCTIONS['OR'] = or_function
EXCEL_FUNCTIONS['AND'] = and_function
EXCEL_FUNCTIONS['NOT'] = not_func
EXCEL_FUNCTIONS['ROUND'] = round_function
EXCEL_FUNCTIONS['ROUNDDOWN'] = round_down_function
EXCEL_FUNCTIONS['FLOOR'] = floor_function
EXCEL_FUNCTIONS['COUNT'] = count_function
EXCEL_FUNCTIONS['COUNTIF'] = countif_function
EXCEL_FUNCTIONS['COUNTBLANK'] = count_blank_function
EXCEL_FUNCTIONS['COUNTA'] = counta_function
EXCEL_FUNCTIONS['ABS'] = abs_function
EXCEL_FUNCTIONS['OFFSET'] = offset_function
EXCEL_FUNCTIONS['MATCH'] = match_function
EXCEL_FUNCTIONS['AVERAGE'] = average_function
EXCEL_FUNCTIONS['AVERAGEIFS'] = average_ifs_function
EXCEL_FUNCTIONS['VLOOKUP'] = vlookup_function
EXCEL_FUNCTIONS['SMALL'] = small_function
EXCEL_FUNCTIONS['LARGE'] = large_function
EXCEL_FUNCTIONS['COUNTIFS'] = count_ifs_function
EXCEL_FUNCTIONS['CONCATENATE'] = concatenate
EXCEL_FUNCTIONS['INDEX'] = index_function
EXCEL_FUNCTIONS['SUBSTITUTE'] = substitute_func
EXCEL_FUNCTIONS['SEARCH'] = search_func
EXCEL_FUNCTIONS['TRIM'] = trim_func
EXCEL_FUNCTIONS['LEN'] = len_func
