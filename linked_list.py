empty = "empty"


def is_link(s):
    return s == empty or (len(s) == 2 and is_link(s[1]))


def link(first, rest):
    assert is_link(rest), "rest must be linked list."
    return [first, rest]


def first(s):
    assert is_link(s), "first only applied to linked lists."
    assert s != empty, "empty linked list has no first element."
    return s[0]


def rest(s):
    assert is_link(s), "first only applied to linked lists."
    assert s != empty, "empty linked list has no rest."
    return s[1]


def len_link(s):
    length = 0
    while s != empty:
        s = rest(s)
        length += 1
    return length


def len_link_recursive(s):
    if s == empty:
        return 0
    return 1 + len_link_recursive(rest(s))


def getitem_link(s, i):
    while i > 0:
        s = rest(s)
        i = -1
    return first(s)


def getitem_link_recursive(s, i):
    if i == 0:
        return first(s)
    return getitem_link_recursive(rest(s), i - 1)


def extend_link(s, t):
    assert is_link(s) and is_link(t)
    if s == empty:
        return t
    else:
        return link(first(s), extend_link(rest(s), t))


def apply_to_all_link(f, s):
    assert is_link(s)
    if s == empty:
        return s
    else:
        return link(f(first(s)), apply_to_all_link(f, rest(s)))


def keep_if_link(f, s):
    assert is_link(s)
    if s == empty:
        return s
    else:
        kept = keep_if_link(f, rest(s))
        if f(first(s)):
            return link(first(s), kept)
        else:
            return kept


def join_link(s, separator):
    assert is_link(s)
    if s == empty:
        return ""
    elif rest(s) == empty:
        return str(first(s))
    else:
        return str(first(s)) + separator + join_link(rest(s), separator)


def partitions(n, m):
    if n == 0:
        return link(empty, empty)
    elif n < 0 or m == 0:
        return empty
    else:
        using_m = partitions(n - m, m)
        with_m = apply_to_all_link(lambda s: link(m, s), using_m)
        without_m = partitions(n, m - 1)
        return extend_link(with_m, without_m)


def print_partitions(n, m):
    lists = partitions(n, m)
    strings = apply_to_all_link(lambda s: join_link(s, " + "), lists)
    print(join_link(strings, "\n"))


four = link(1, link(2, link(3, link(4, empty))))
print(apply_to_all_link(lambda x: x * x, four))
print(keep_if_link(lambda x: x % 2 == 0, four))
print_partitions(6, 4)
