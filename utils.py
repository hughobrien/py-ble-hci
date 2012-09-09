def pack(input):
    """returns 'packed' aka hex encoded string of input e.g.
    >>> pack("00 aa ff")
        '\x00\xaa\xff' """
    return input\
           .replace(' ', '')\
           .replace('\n','')\
           .decode('hex')

def pretty(input):
    """ >>> pretty("\x01\x02\x03\xff")
            '01 02 03 FF'"""
    input = input.encode('hex')
    a=0
    out = ''
    for i in range(0, len(input)):
        if a == 2:
            out = out + ' '
            a = 0
        out = out + input[i].capitalize()
        a = a + 1
    return out
