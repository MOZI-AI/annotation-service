__author__ = 'Abdulrahman Semrie<xabush@singularitynet.io>'

import string

_BASE = 64

alphabet = string.ascii_letters + string.digits + "-" + "_"


def encode(guid):
    """
    A simple function to generate a short string using a GUID
    :param guid:
    :return:
    """
    dividend = guid.time_low

    ls = []

    while len(ls) < 7:
        dividend, rem = divmod(dividend, _BASE)
        ls.append(rem)

    arr = []
    for i in ls:
        arr.append(alphabet[i])

    return "".join(arr)