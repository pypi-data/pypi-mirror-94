def delete_number(string: str):
    for i in range(10):
        string = string.replace(str(i), '')
    string = string.replace('-', '').replace('+', '')
    return string


def start_shell():
    while True:
        c = input('>>> ')
        if c.endswith(';'):
            c = c[:-1]
        if c.endswith(':'):
            tab = input('... ')
            while tab.replace(' ', '') != '':
                c += '\n' + tab
                tab = input('... ')
        if delete_number(c.split('.')[-1]) in ['quit()', 'exit()', '^Zreturn']:
            exit(0)
        try:
            exec(c)
        except:
            pass
