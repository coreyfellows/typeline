import argparse
import inspect
import sys

class Typeline(object):
    def __init__(self, name=None):
        self.commands = []
        self.groups = []
        self.name = name

    def run(self):
        parser = argparse.ArgumentParser()
        args = self.generate_parser(parser).parse_args()
        kwargs = {k:v for k,v in filter(lambda pair: not pair[0].startswith('_typeline_'), args._get_kwargs())}
        if hasattr(args, '_typeline_func'):
            args._typeline_func(**kwargs)
        else:
            import pdb; pdb.set_trace()
            parser.print_help()

    def generate_parser(self, parser):
        subparsers = parser.add_subparsers()
        for command in self.commands:
            cmd_parser = subparsers.add_parser(command.__name__)
            sig = inspect.signature(command)
            for p in sig.parameters:
                param = sig.parameters[p]
                cmd_name = p
                if param.kind == param.KEYWORD_ONLY:
                    cmd_name = f"--{cmd_name}"
                cmd_name = cmd_name.replace("_", "-")
                if param.annotation == param.empty:
                    cmd_parser.add_argument(cmd_name)
                else:
                    options = param.annotation()
                    if param.default != param.empty:
                        options['default'] = param.default
                    cmd_parser.add_argument(cmd_name, **options)
                cmd_parser.set_defaults(_typeline_func=command)

        for group in self.groups:
            group_parser = subparsers.add_parser(group.name)
            group.generate_parser(group_parser)
        return parser


    def group(self, group):
        if inspect.ismodule(group):
            self.groups.append(Typeline(group.__name__))
            self.groups[-1].module(group)
        else:
            self.groups.append(Typeline(group))
        return self.groups[-1]

    def command(self, fn):
        self.commands.append(fn)

    def module(self, module):
        for name, fn in inspect.getmembers(module, inspect.isfunction):
            self.command(fn)