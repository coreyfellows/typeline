import sys
import argparse
from collections.abc import Mapping


class Help(dict):
    def add_help(self, string):
        self['help'] = string
        return self

    def __call__(self):
        return self

def Flag():
    return {'action': 'store_true'}

def FalseFlag():
    return {'action': 'store_false'}

def StoreConst(const, default=None):
    def _():
        return {'action': 'store_const', 'const': const, 'default': default}
    return _

def Choices(choices, default=None):
    def _():
        return {'choices': choices, 'default': default, 'type': choices[0].__class__}
    return _

def TypedValue(type_):
    def _internal():
        return {'type': type_, 'help': type_.__name__}
    return _internal

def String():
    return TypedValue(str)()

def Float():
    return TypedValue(float)()

def Integer():
    return TypedValue(int)()

def File(mode, default_file):
    def _():
        return {'default': default_file, 'type': argparse.FileType(mode)}
    return _

def InFile():
    return File("r", sys.stdin)()

def OutFile():
    return File("w", sys.stout)()

def List(element_type=None, nargs="*"):
    if element_type is None and nargs == "*":
        return {'nargs': nargs, 'help': f'List length={nargs}'}
    def _():
        options = element_type() if element_type else {}
        options['nargs'] = nargs
        if options.get('help'):
            options['help'] = f"List<{options.get('help')}> length={nargs}"
        else:
            options['help'] = f'List length={nargs}'
        return options
    return _

def WithHelp(type_, doc):
    def _():
        options = type_()
        if (options.get('help')):
            options['help'] = f"{options.get('help')}: {doc}"
        else:
            options['help'] = doc
        return options
    return _

def Chain(*args):
    def _():
        options = {}
        doc = ''
        for type_ in args:
            options.update(type_())
            if options.get('help'):
                doc = f"{doc} {options['help']}"
        if doc:
            options['help'] = doc

        return options
    return _