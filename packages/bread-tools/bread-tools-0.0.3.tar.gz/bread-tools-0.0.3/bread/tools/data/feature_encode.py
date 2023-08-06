def one_hot(length, current):
    """
    Standard one hot encoding.
    >>> one_hot(length=3,current=1)
    [0, 1, 0]
    """
    assert length > current
    assert current > -1
    code = [0] * length
    code[current] = 1
    return code
