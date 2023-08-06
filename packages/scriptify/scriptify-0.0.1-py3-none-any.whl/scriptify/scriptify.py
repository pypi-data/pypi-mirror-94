from argparse import ArgumentParser
from inspect import getargspec


def scriptify(fn):
    parser = ArgumentParser(description=fn.__name__.replace('_', ' '))

    argspec = getargspec(fn)
    defaults = [] if argspec.defaults is None else argspec.defaults
    num_non_kwargs = len(argspec.args) - len(defaults)

    for i, arg in enumerate(argspec.args):
        if i < num_non_kwargs:
            parser.add_argument(f'--{arg}', required=True)

        else:
            default = defaults[i - num_non_kwargs]
            if type(default) in (int, float, str):
                parser.add_argument(
                    f'--{arg}',
                    type=type(default),
                    required=False,
                    default=default)

            elif default is True:
                parser.add_argument(f'--{arg}', action='store_false')

            elif default is False:
                parser.add_argument(f'--{arg}', action='store_true')

            else:
                parser.add_argument(f'--{arg}', required=False, default=default)

    parsed_args = parser.parse_args()

    passed_args = {}
    for arg in argspec.args:
        passed_args[arg] = _parse_arg_from_string(getattr(parsed_args, arg))

    fn(**passed_args)


def _parse_arg_from_string(arg, allow_list=True):
    if type(arg) is not str:
        return arg

    try:
        return int(arg)
    except ValueError:
        pass

    try:
        return float(arg)
    except ValueError:
        pass

    if arg == 'True':
        return True

    elif arg == 'False':
        return False

    elif arg == 'None' or arg == '':
        return None

    if allow_list:
        try:
            return _parse_list(arg)
        except ValueError:
            pass

    return arg


def _parse_list(arg):
    if not (arg.startswith('[') and arg.endswith(']')):
        raise ValueError

    if arg == '[]':
        return []

    l = []
    t = None

    for elem in arg[1:-1].split(','):
        x = _parse_arg_from_string(elem.strip(), allow_list=False)

        if type(x) is str:
            if x.startswith("'") and x.endswith("'") and x != "'":
                x = x[1:-1]
            else:
                raise ValueError

        if x is not None:
            if t is None:
                t = type(x)

            elif t != type(x):
                raise ValueError

        l.append(x)

    return l
