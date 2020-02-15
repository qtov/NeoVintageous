# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

import os

_autocmds = []  # type: list


def add_autocmd(event: str, pat: str, cmd: str, **kwargs) -> None:

    autocmd = {
        'event': event.lower(),
        'pat': pat,
        'cmd': cmd
    }

    # print("add_autocmd()", autocmd, 'kwargs =', kwargs)

    found = False
    for a in _autocmds:
        if autocmd == a:
            found = True

    if not found:
        _autocmds.append(autocmd)


def _get_view_file_type(view) -> str:
    file_name = view.file_name()
    if not file_name:
        return ''

    ext = os.path.splitext(file_name)[1]
    if not ext:
        return ''

    if ext[0] == '.':
        ext = ext[1:]

    return ext


def _get_filetype_autocmds(extention: str) -> list:
    return [a for a in _autocmds if a['event'] == 'filetype' and a['pat'] == extention]


def do_autocmds(view) -> None:
    from NeoVintageous.nv.ex_cmds import do_ex_cmdline

    ext = _get_view_file_type(view)
    if ext:
        for filetype_autocmd in _get_filetype_autocmds(ext):
            print('run autocmd Filetype:', filetype_autocmd)
            cmd = filetype_autocmd['cmd']

            if cmd[0] != ':':
                cmd = ':' + cmd

            print('run autocmd Filetype:', cmd)
            do_ex_cmdline(view.window(), cmd)
