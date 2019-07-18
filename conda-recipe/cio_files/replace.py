import sys


def replace(lst, path, assert_change=True, verbose=True):
    with open(path, 'rb') as fi:
        old_data = fi.read().decode('utf-8')

    data = old_data
    for a, b in lst:
        if verbose:
            print("replacing %r with %r in %s" % (a, b, path))
        data = data.replace(a, b)

    if assert_change:
        assert data != old_data, path

    with open(path, 'wb') as fo:
        fo.write(data.encode('utf-8'))


def usage():
    sys.stdout.write("""usage: replace [options] A B [FILE ...]

replaces string A with string B in FILE(s)

Options:
  --help     show this help message and exit
  --nvd      don't mind (nevermind) if FILE(s) did not change
""")
    sys.exit(0)


def main():
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == '--help':
        usage()

    assert_change = True
    if len(args) > 0 and args[0] == '--nvd':
        assert_change = False
        args = args[1:]

    if len(args) < 2:
        sys.exit("at least two arguments expected, try --help")

    for path in args[2:]:
        replace([args[:2]], path, assert_change)


if __name__ == '__main__':
    main()
