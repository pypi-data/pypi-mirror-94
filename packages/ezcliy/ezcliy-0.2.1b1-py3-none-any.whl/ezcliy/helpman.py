from collections import OrderedDict
from typing import Optional

from colorama import Style, Back, Fore

from ezcliy.parameters import Flag, KeyVal


class HelpRenderer:
    def __init__(self, command):
        """

        :param ezcli.Command command:
        """
        self.command = command
        self.sections = OrderedDict()

    def add(self, section_name: str, val: str, desc: str):
        section = self.sections.get(section_name, [])
        section.append((val, desc))
        self.sections.update({section_name: section})

    @property
    def firstline(self):
        fline = Back.WHITE + Fore.BLACK + 'Usage:' + Style.RESET_ALL + f' {self.command.name}'

        if self.command.commands:
            fline += ' [COMMANDS]'

        if self.command.positionals:
            for pos in self.command.positionals:
                fline += f' [{pos.name}]'
        if not self.command.restrict_to_positionals_only:
            fline += f' [VALUES...]'

        if self.command.parameters:
            fline += ' [PARAMETERS]'
        return fline

    @staticmethod
    def render_section(section_name: str, rows: list[tuple[str, Optional[str]]]):
        lines = [Style.BRIGHT + f'{section_name.strip().capitalize()}:' + Style.RESET_ALL]
        for row in rows:
            line = f'    {row[0]}'
            if row[1] is not None:
                line += f' - {row[1]}'
            lines.append(line)
        return '\n'.join(lines)

    def __str__(self):
        lines = [self.firstline] + [self.render_section(n, r) for n, r in self.sections.items()]
        return '\n'.join(lines)


class Helpman(Flag):
    def __init__(self):
        super().__init__('--help')
        self.description = 'no description has been provided'

    def pass_args(self, user_args: list[str]) -> list[str]:
        if self.value:
            return user_args
        return super(Helpman, self).pass_args(user_args)

    @staticmethod
    def render_help(command):
        """

        :param ezcli.Command command:
        :return:
        """
        hr = HelpRenderer(command)

        # Get commands
        if command.commands:
            for n, c in command.commands.items():
                hr.add('commands', n, c().description)

        # Some positionals
        if command.positionals:
            for pos in command.positionals:
                hr.add('positionals', pos.name, pos.description)

        # Get params
        if command.parameters:
            for flag in [f for f in command.parameters.values() if isinstance(f, Flag)]:
                hr.add('flags', ' '.join(flag.aliases), flag.description)
            for keyval in [kv for kv in command.parameters.values() if isinstance(kv, KeyVal)]:
                hr.add('keyed values', keyval.key + ' (value)', keyval.description)

        return hr.__str__()
