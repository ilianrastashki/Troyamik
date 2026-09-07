# -*- coding: utf-8 -*-
"""
Търсене без значение от главни/малки букви на кирилица в SQLite.

Вградените в SQLite lower(), upper() и LIKE обработват само латиница, затова
"кока" не намира "Кока-Кола". Тук ги заменяме с функции на Python, чиито
.lower()/.upper() разбират целия Unicode - и кирилицата в частност.

Засяга всички заявки с __icontains / __iexact: и админа, и търсачката в магазина.
"""
import re

from django.db.backends.signals import connection_created
from django.dispatch import receiver


def _like(pattern, value, escape=None):
    """SQL LIKE, но с Unicode-съобразено сравнение на главни и малки букви."""
    if pattern is None or value is None:
        return None

    pattern = str(pattern).lower()
    value = str(value).lower()

    # превръщаме LIKE шаблона в регулярен израз: % -> .*, _ -> .
    parts, i = [], 0
    while i < len(pattern):
        ch = pattern[i]
        if escape and ch == escape:
            i += 1
            if i < len(pattern):
                parts.append(re.escape(pattern[i]))
                i += 1
            continue
        if ch == '%':
            parts.append('.*')
        elif ch == '_':
            parts.append('.')
        else:
            parts.append(re.escape(ch))
        i += 1

    return 1 if re.match('(?s)^' + ''.join(parts) + '$', value) else 0


@receiver(connection_created)
def register_unicode_functions(sender, connection, **kwargs):
    if connection.vendor != 'sqlite':
        return
    conn = connection.connection
    if conn is None:
        return
    conn.create_function('lower', 1, lambda s: s.lower() if isinstance(s, str) else s)
    conn.create_function('upper', 1, lambda s: s.upper() if isinstance(s, str) else s)
    conn.create_function('like', 2, _like)
    conn.create_function('like', 3, _like)
