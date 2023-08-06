def float_as_currency(self, val: float):
    return "${:,.2f}".format(round(val, 2))


def int_tryParse(self, value):
    try:
        return int(value)
    except:
        return False