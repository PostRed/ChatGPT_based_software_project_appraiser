#!/usr/bin/env python3
# The MIT License (MIT)
#
# Copyright (c) 2021-2024 Yegor Bugayenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import sys
from typing import Any

import javalang


def doer_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> float:
    """Ratio between the number of attributes that are data primitives and the number of attributes that are pointers to objects.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    num_primitives = 0
    num_pointers = 0

    for path, node in fields:
        del path
        if node.type.name in ['int', 'float', 'double', 'boolean', 'char', 'byte', 'short', 'long']:
            num_primitives += 1
        else:
            num_pointers += 1

    if (total := num_primitives + num_pointers) == 0:
        return 0
    return num_primitives / total


def ahf_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> float:
    """Ratio of private/protected attributes to all attributes in a class.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    hidden = 0
    total = 0
    for path, node in fields:
        del path
        if 'private' in node.modifiers or 'protected' in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def sahf_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> float:
    """Ratio of private/protected attributes to static attributes in a class.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    hidden = 0
    total = 0
    for path, node in fields:
        del path
        if 'static' not in node.modifiers:
            continue
        if 'private' in node.modifiers or 'protected' in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def nomp_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Total number of parameters in all class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    total = 0
    for path, node in mlist:
        del path
        total += len(node.parameters)
    return total


def nosmp_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Total number of parameters in static class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    total = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            continue
        total += len(node.parameters)
    return total


def mxnomp_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Maximum number of parameters in all class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    maximum = 0
    for path, node in mlist:
        del path
        maximum = max(maximum, len(node.parameters))
    return maximum


def mxnosmp_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Maximum number of parameters in static class methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    maximum = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            continue
        maximum = max(maximum, len(node.parameters))
    return maximum


def nom_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Number of methods that are annotated with @Override.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    total = 0
    for path, node in mlist:
        del path
        annotations = list(annotation.name for annotation in node.annotations)
        if 'Override' in annotations:
            total += 1
            continue
    return total


def attrs_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count non-static attributes.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    found = 0
    for path, node in fields:
        del path
        if 'static' not in node.modifiers:
            found += 1
    return found


def sattrs_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count static attributes.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.FieldDeclaration)
    fields = list(field for field in declaration)
    found = 0
    for path, node in fields:
        del path
        if 'static' in node.modifiers:
            found += 1
    return found


def ctors_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count constructors.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.ConstructorDeclaration)
    clist = list(method for method in declaration)
    return len(clist)


def methods_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count non-static methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    found = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            found += 1
    return found


def smethods_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count static methods.
    :rtype: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    found = 0
    for path, node in mlist:
        del path
        if 'static' in node.modifiers:
            found += 1
    return found


def mhf_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> float:
    """Calculate Method Hiding Factor (MHF), which is the ratio
    between private+protected methods and all methods.
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    hidden = 0
    total = 0
    for path, node in mlist:
        del path
        if 'public' not in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def smhf_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> float:
    """Calculate Static Method Hiding Factor (SMHF), which is the ratio
    between private+protected methods and all methods (which are static).
    :rtype: float
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    mlist = list(method for method in declaration)
    hidden = 0
    total = 0
    for path, node in mlist:
        del path
        if 'static' not in node.modifiers:
            continue
        if 'public' not in node.modifiers:
            hidden += 1
        total += 1
    if total == 0:
        return 0
    return hidden / total


def ncss_(parser_class: javalang.tree.CompilationUnit) -> int:
    """Count the NCSS (non-commenting source statement) lines.
    :rtype: int
    """
    value = 0
    for path, node in parser_class:
        del path
        node_type = str(type(node))
        if 'Statement' in node_type:
            value += 1
        elif node_type == 'VariableDeclarator':
            value += 1
        elif node_type == 'Assignment':
            value += 1
        elif 'Declaration' in node_type \
                and 'LocalVariableDeclaration' not in node_type \
                and 'PackageDeclaration' not in node_type:
            value += 1
    return value


def impls_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count the number of interfaces the class implements.
    r:type: int
    """
    return len(tlist[0][1].implements or [])


def extnds_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Count the number of classes this class extends (0 or 1).
    r:type: int
    """
    return 0 if tlist[0][1].extends is None else 1


def final_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Return 1 if the class is final, zero otherwise.
    r:type: int
    """
    return 1 if 'final' in tlist[0][1].modifiers else 0


def gnrcs_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Return number of type parameters (generics).
    r:type: int
    """
    return len(tlist[0][1].type_parameters or [])


def annts_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Return number of annotations of the class.
    r:type: int
    """
    return len(tlist[0][1].annotations or [])


def varcomp_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> float:
    """Return average number of parts in variable names in class.
    r:type: float
    """
    parts = 0
    variables = 0
    for _, node in tlist[0][1].filter(javalang.tree.VariableDeclarator):
        if (name := node.name) == '':
            continue
        variables += 1
        # Java only allows "$" and "_" as special symbols in variable names.
        # Split variable name by them to only count words and numbers.
        components = [comp for comp in re.split(r'[\$_]+', name) if comp != '']
        if len(components) == 0:
            parts += 1
            continue
        for component in components:
            parts += 1
            prev_char = component[:1]
            for char in component[1:]:
                if prev_char.isdigit() != char.isdigit():
                    parts += 1
                elif prev_char.islower() and char.isupper():
                    parts += 1
                prev_char = char
    return (parts / variables) if variables != 0 else 0


def nop_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Return number of polymorphic methods in main class.
    Methods of nested classes are skipped.
    r:type: int
    """
    declaration = tlist[0][1].filter(javalang.tree.MethodDeclaration)
    methods_count: dict[str, int] = {}

    for path, node in declaration:
        # Methods of nested classes has path > 2.
        if len(path) > 2:
            continue
        if node.name in methods_count:
            methods_count[node.name] += 1
            continue
        methods_count[node.name] = 1
    return sum(1 for count in methods_count.values() if count > 1)


def nulls_(tlist: list[tuple[Any, javalang.tree.ClassDeclaration]]) -> int:
    """Return number of null references used in the class.
    r:type: int
    """
    null_count = 0
    for _, node in tlist[0][1].filter(javalang.tree.Literal):
        if str(node.value) == 'null':
            null_count += 1
    return null_count
