from pyduinocli.commands.base import CommandBase
from pyduinocli.constants import commands
from pyduinocli.constants import flags


class DebugCommand(CommandBase):

    def __init__(self, base_args):
        CommandBase.__init__(self, base_args)
        self._base_args.append(commands.DEBUG)

    def __call__(self, fqbn=None, input_dir=None, port=None, interpreter=None, info=None, programmer=None, sketch=None):
        args = []
        if fqbn:
            args.extend([flags.FQBN, CommandBase._strip_arg(fqbn)])
        if input_dir:
            args.extend([flags.INPUT_DIR, CommandBase._strip_arg(input_dir)])
        if port:
            args.extend([flags.PORT, CommandBase._strip_arg(port)])
        if interpreter:
            args.extend([flags.INTERPRETER, CommandBase._strip_arg(interpreter)])
        if info is True:
            args.append(flags.INFO)
        if programmer:
            args.extend([flags.PROGRAMMER, CommandBase._strip_arg(programmer)])
        if sketch:
            args.append(CommandBase._strip_arg(sketch))
        return self._exec(args)
