import cmd
import inspect


CALLED = lambda: inspect.stack()[1][3]


class MainCli(cmd.Cmd):
    GAME_MODES = ['1']

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.ruler = '—'
        self.intro = ('Добро пожаловать в игру "Пентамино"\n'
                      'Для справки наберите "help"')
        # self.doc_header = ('Доступные команды (для справки по конкретной '
        #                    'команде наберите "help _команда_)')
        self.doc_header = ''

    def default(self, line):
        print('Несуществующая команда')

    def preloop(self):
        print('Какую доску будете заполнять?')

    def postcmd(self, stop: bool, line: str) -> bool:
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
        print('Пока!')
        return True

    def do_about(self, args):
        """about - Информация о игре"""
        print("Информация о игре")
        print(f'Аргумениты команды {CALLED()[3:]} {args=}')

    def control_panel(self):
        print('Возможные действия')
        self.do_help('')

    def do_help(self, arg):
        '''List available commands with "help" or detailed help with "help cmd".'''
        if arg:
            # XXX check arg syntax
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc=getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n"%str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n"%str(self.nohelp % (arg,)))
                return
            func()
        else:
            print('else')
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help = {}
            for name in names:
                if name[:5] == 'help_':
                    help[name[5:]]=1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd=name[3:]
                    if cmd in help:
                        cmds_doc.append(cmd)
                        del help[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            self.stdout.write("%s\n"%str(self.doc_leader))
            self.print_topics(self.doc_header,   cmds_doc,   15,80)
            #self.print_topics(self.misc_header,  list(help.keys()),15,80)
            #self.print_topics(self.undoc_header, cmds_undoc, 15,80)
            print('end', self.doc_leader)
            print('end', self.get_names())
            print('cmds_doc', self.print_topics('', cmds_doc, 15, 80))
            # print('cmds_doc', self.print_topics(self.doc_header,   cmds_doc, 15, 80))


if __name__ == "__main__":
    try:
        MainCli().cmdloop()
    except KeyboardInterrupt:
        print("завершение сеанса...")
