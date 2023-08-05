from pyduinocli.commands.base import CommandBase
from pyduinocli.constants import commands
from pyduinocli.constants import flags


class UploadCommand(CommandBase):

    def __init__(self, base_args):
        CommandBase.__init__(self, base_args)
        self._base_args.append(commands.UPLOAD)

    def __call__(self, sketch=None, fqbn=None, input_dir=None, input_file=None, port=None, verify=None, programmer=None):
        args = []
        if fqbn:
            args.extend([flags.FQBN, CommandBase._strip_arg(fqbn)])
        if input_dir:
            args.extend([flags.INPUT_DIR, CommandBase._strip_arg(input_dir)])
        if input_file:
            args.extend([flags.INPUT_FILE, CommandBase._strip_arg(input_file)])
        if port:
            args.extend([flags.PORT, CommandBase._strip_arg(port)])
        if verify is True:
            args.append(flags.VERIFY)
        if sketch:
            args.append(CommandBase._strip_arg(sketch))
        if programmer:
            args.extend([flags.PROGRAMMER, CommandBase._strip_arg(programmer)])
        return self._exec(args)
