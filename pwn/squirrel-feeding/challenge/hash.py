def hash(name):
    return sum(c * 31 for c in name)


if __name__ == '__main__':
    print(hash(b'eaaaa'))
    print(hash(b'aeaaa'))
    print(hash(b'aaeaa'))
    print(hash(b'aaaea'))
    print(hash(b'aaaae'))