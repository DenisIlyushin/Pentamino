import cmd
import inspect


CALLED = lambda: inspect.stack()[1][3]


class MainCli(cmd.Cmd):
    GAME_MODES = ['1']
    SERVICE_COMMANDS = ['exit', 'help']

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.ruler = '—'
        self.intro = ('Добро пожаловать в игру "Пентамино"\n'
                      'Для справки наберите "help"')
        self.doc_header = ('Доступные команды (для справки по конкретной '
                           'команде наберите "help _команда_)')

    def default(self, line):
        print('Несуществующая команда')

    def preloop(self):
        print('Какую доску будете заполнять?')

    def postcmd(self, stop: bool, line: str) -> bool:
        if line not in self.SERVICE_COMMANDS:
            self.control_panel()
        return stop

    def do_start(self, args):
        """start - Начать игровой процесс n-го режима"""
        print(f'Аргумениты команды {CALLED()[3:]} {args=}')
        if args == '1':
            print("Игровой процесс 1го режима")
            # ModeGame1Cli().cmdloop()
            print('ModeGame1Cli().cmdloop()')
        else:
            print('Выбирите режим игры')
            print(f'Cписок режимов: {self.GAME_MODES}')

    def do_exit(self, arg):
        """exit - выход из игры"""
        print('Вы покинули игру!')
        return True

    def do_about(self, args):
        """about - Информация о игре"""
        print("Информация о игре")
        # print(f'Аргумениты команды {CALLED()[3:]} {args=}')

    def do_board(self, arg):
        """board - Показать доску"""
        test_board = [
            '  1234567891011  ',
            'a ·FFI····· · · a',
            'b FF·I····· · · b',
            'c ·F·I····· · · c',
            'e ···I····· · · e',
            'd ···I····· · · d',
            '  1234567891011  ',
        ]
        self.own_print_topics(
            'Доска', test_board, 15, len(test_board[0]), ruler=False
        )

    def control_panel(self):
        '''Выводит возможные варианты команд'''
        names = self.get_names()
        cmds_doc = []
        cmds_undoc = []
        help = {}
        for name in names:
            if name[:5] == 'help_':
                help[name[5:]] = 1
        names.sort()
        # There can be duplicates if routines overridden
        prevname = ''
        for name in names:
            if name[:3] == 'do_':
                if name == prevname:
                    continue
                prevname = name
                cmd1 = name[3:]
                if cmd1 in help:
                    cmds_doc.append(cmd1)
                    del help[cmd1]
                elif getattr(self, name).__doc__:
                    cmds_doc.append(cmd1)
                else:
                    cmds_undoc.append(cmd1)
        self.own_print_topics('Возможные действия', cmds_doc, 15, 80)

    def own_print_topics(self, header, cmds, cmdlen, maxcol, ruler=True):
        if cmds:
            self.stdout.write("\n")
            self.stdout.write("%s\n"%str(header))
            if ruler and self.ruler:
                self.stdout.write("%s\n"%str(self.ruler * len(header)))
            self.columnize(cmds, maxcol-1)
            # self.stdout.write("\n")


if __name__ == "__main__":
    try:
        MainCli().cmdloop()
    except KeyboardInterrupt:
        print("завершение сеанса...")
