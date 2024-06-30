empty = "empty"
suits = ["heart", "diamond", "spade", "club"]


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


def mutable_link():
    contents = empty

    def dispatch(message, value=None):
        nonlocal contents
        if message == "len":
            return len_link(contents)
        elif message == "getitem":
            return getitem_link(contents, value)
        elif message == "push_first":
            contents = link(value, contents)
        elif message == "pop_first":
            f = first(contents)
            contents = rest(contents)
            return f
        elif message == "str":
            return join_link(contents, ", ")

    return dispatch


def to_mutable_link(source):
    s = mutable_link()
    for element in reversed(source):
        s("push_first", element)
    return s


def print_partitions(n, m):
    lists = partitions(n, m)
    strings = apply_to_all_link(lambda s: join_link(s, " + "), lists)
    print(join_link(strings, "\n"))


def first_d(d):
    return d[0]


def rest_d(d):
    return d[1:]


def join_dict(d, separator):
    if len(rest_d(d)) == 0:
        key, value = first_d(d)
        return "(" + str(key) + "," + str(value) + ")"
    else:
        key, value = first_d(d)
        return (
            "("
            + str(key)
            + ","
            + str(value)
            + ")"
            + separator
            + join_dict(rest_d(d), separator)
        )


def dictionary():
    records = []

    def getitem(key):
        matches = [r for r in records if r[0] == key]
        if len(matches) == 1:
            key, value = matches[0]
            return value

    def setitem(key, value):
        nonlocal records
        non_matches = [r for r in records if r[0] != key]
        records = non_matches + [[key, value]]

    def dispatch(message, key=None, value=None):
        if message == "getitem":
            return getitem(key)
        elif message == "setitem":
            setitem(key, value)
        elif message == "str":
            return join_dict(records, ", ")

    return dispatch


four = link(1, link(2, link(3, link(4, empty))))
print_partitions(6, 4)

s = to_mutable_link(suits)
s("pop_first")
d = dictionary()
d("setitem", 3, 9)
d("setitem", 4, 16)
d("setitem", 5, 25)
print(d("str"))
