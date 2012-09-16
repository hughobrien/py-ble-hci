def pack(input):
    #returns 'packed' aka hex encoded string of input e.g.
    #>>> pack("00 aa ff")
    #    '\x00\xaa\xff' 
    return input\
           .replace(' ', '')\
           .replace('\n','')\
           .decode('hex')

def pretty(input):
    # >>> pretty("\x01\x02\x03\xff")
    #       '01 02 03 FF'
    input = input.encode('hex')
    a=0
    out = ''
    for i in range(len(input)):
        if a == 2:
            out = out + ' '
            a = 0
        out = out + input[i].capitalize()
        a = a + 1
    return out

def print_container(cont,indent=0):

    tabs = "\t" * indent
    for i in cont:
        #todo: replace with isinstance
        if cont[i].__class__.__name__ == 'Container':
            print "%sContainer: %s" % (tabs, i)
            print_container(cont[i], indent + 1)
        else:
            print "%s%s: %s" % (tabs, i, cont[i])

def dict_to_csv(data, dest):
    out = ''
    for i in data:
        out = out + str(i) + ',' + str(data[i]) + '\n'

    cleanout = out.replace(' ', '')\
               .replace('[', '')\
               .replace(']', '')

    f = open(dest, 'w')
    f.write(cleanout)
    f.close
