

def elo_expected(d:float,f:float=400)->float:
    """ Expected points scored in a match
    :param d:   Difference in rating
    :param f:   "F"-Factor
    :return:    Expected points
    """
    return 1. / (1 + 10 ** (d / f))

