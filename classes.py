class Account:
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        return self.balance


def bind_method(value, instance):
    if callable(value):

        def method(*args):
            return value(instance, *args)

        return method
    else:
        return value


def make_instance(cls):
    def get_value(name):
        if name in attributes:
            return attributes[name]
        else:
            value = cls["get"](name)
            return bind_method(value, instance)

    def set_value(name, value):
        attributes[name] = value

    attributes = {}
    instance = {"get": get_value, "set": set_value}
    return instance


def init_instance(cls, *args):
    instance = make_instance(cls)
    init = cls["get"]("__init__")
    if init:
        init(instance, *args)
    return instance


def make_class(attributes, base_class=None):
    def get_value(name):
        if name in attributes:
            return attributes[name]
        elif base_class is not None:
            return base_class["get"](name)

    def set_value(name, value):
        attributes[name] = value

    def new(*args):
        return init_instance(cls, *args)

    cls = {"get": get_value, "set": set_value, "new": new}
    return cls


def make_account_class():
    interest = 0.02

    def __init__(self, account_holder):
        self["set"]("holder", account_holder)
        self["set"]("balance", 0)

    def deposit(self, amount):
        new_balance = self["get"]("balance") + amount
        self["set"]("balance", new_balance)
        return self["get"]("balance")

    def withdraw(self, amount):
        balance = self["get"]("balance")
        if amount > balance:
            return "Insufficient funds"
        self["set"]("balance", balance - amount)
        return self["get"]("balance")

    return make_class(locals())


a = Account("Dima")

AccountClass = make_account_class()

b = AccountClass["new"]("Dima")
print(b["get"]("holder"))
print(b["get"]("interest"))
print(b["get"]("deposit")(20))
print(b["get"]("withdraw")(15))
