# !/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    import atexit
    import os
    import readline
    import rlcompleter
    import sys
    import termios
    import textwrap

    HISTFILE = os.path.expanduser("~/.pyhistory")

    def term_supports_colors():
        import sys
        file = sys.stdout
        try:
            import curses
            assert file.isatty()
            curses.setupterm()
            assert curses.tigetnum("colors") > 0
        except Exception:
            return False
        else:
            return True

    if term_supports_colors():
        def hilite(s, ok=True, bold=False):
            """Return an highlighted version of 'string'."""
            attr = []
            if ok is None:  # no color
                pass
            elif ok:   # green
                attr.append('32')
            else:   # red
                attr.append('31')
            if bold:
                attr.append('1')
            return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), s)
    else:
        def hilite(s, *a, **k):
            return s

    def print_(s):
        print(hilite(s))

    # tab-completion.
    pdb.Pdb.complete = rlcompleter.Completer(locals()).complete
    if sys.platform.startswith("darwin"):
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind('tab: complete')

    # load history
    if os.path.exists(HISTFILE):
        readline.read_history_file(HISTFILE)

    # save history on exit
    def save_history(path):
        import readline;
        readline.set_history_length(10000)
        readline.write_history_file(path)

    atexit.register(save_history, HISTFILE)

    # Taken from https://gist.github.com/1125049
    # There are a couple of edge cases where you can lose terminal
    # echo. This should restore it next time you open a pdb.
    termios_fd = sys.stdin.fileno()
    termios_echo = termios.tcgetattr(termios_fd)
    termios_echo[3] = termios_echo[3] | termios.ECHO
    termios_result = termios.tcsetattr(termios_fd, termios.TCSADRAIN, termios_echo)

    help_ = textwrap.dedent("""\
        h(elp) [obj]  : same as help(obj)
        w(here)       : print a stack trace, with the most recent frame at the
                        bottom. An arrow indicates the current frame.
        d(own)        : move the current frame one level down in the stack
                        trace
        u(p)          : move the current frame one level up in the stack trace
        b(reak) [[filename:]lineno | function[, condition]]
                      : sets breakpoint
        tbreak [[filename:]lineno | function[, condition]]
                      : sets a temporary breakpoint, which is removed
                        automatically when it is first hit
        cl(ear) [filename:lineno | bpnumber [bpnumber ...]]
                      : clear breakpoints
        s(tep)        : step into function
        n(ext)        : next line
        unt(il)       : continue execution until the line with the line number
                        greater than the current one is reached or when
                        returning from current frame
        r(eturn)      : continue execution until the current function returns
        c(ont(inue))  : continue execution
        j(ump) lineno : set the next line that will be executed; this lets you
                        jump back and execute code again, or jump forward to
                        skip code that you don’t want to run.
        l(ist) [first[, last]]
                      : list source code for the current file; without
                        arguments, list 11 lines around the current line;
                        with one argument, list 11 lines around at that line;
                        with two arguments, list the given range;
        a(rgs)        : print the argument list of the current function
        p expression  : evaluate the expression in the current context and
                        print its value
        pp <obj>      : pretty print obj
        alias [name [command]]
                      : creates an alias
        [!]statement  : escape commands
        run [args ...]: restart the debugged Python program;
        q(uit)        : quit
        """)
    print_(help_)

main()
del main
