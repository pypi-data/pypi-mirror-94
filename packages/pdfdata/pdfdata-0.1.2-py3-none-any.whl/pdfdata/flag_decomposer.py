def flag_decomposer(flags: int) -> dict:
    """
    Make font flags human readable.

    :param flags: integer indicating binary encoded font attributes
    :return: dictionary of attributes names and their activation state
    """

    # defaults
    tmp = {"superscript": 0, "italic": 0, "serifed": 0, "monospaced": 0, "bold": 0}

    # check for activation state
    if flags & 2 ** 0:
        tmp["superscript"] = 1

    if flags & 2 ** 1:
        tmp["italic"] = 1

    if flags & 2 ** 2:
        tmp["serifed"] = 1

    if flags & 2 ** 3:
        tmp["monospaced"] = 1

    if flags & 2 ** 4:
        tmp["bold"] = 1

    # return
    return tmp
