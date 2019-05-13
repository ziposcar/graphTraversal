"""kvparser -- A simple hierarchical key-value text parser.

(c) 2004 HAS

kvparser parses text containing simple key-value pairs and/or nested blocks using a simple event-driven model. The text format is intended to be human readable and writeable, so is designed for simplicity and consistency with a low-noise syntax. The error handling for malformed text is strict by default - the text format is simple enough that it should not be hard to write valid text.

Example text:

#######

person:
	first-name=Joe
	last-name=Black
	email:
		nickname=joe.black
		address=joe@foo.com
	email:
		nickname=fuzzy
		address=fuzzy@bar.org

#######


1. Simple key-value pairs take the form:

NAME=VALUE

NAME must contain only alphanumeric and/or hyphen characters, and be at least 1 character in length with the first character being a letter. (Note: Periods are permitted in names as well. However, these should be used only to indicate ad-hoc namespaces, e.g. 'foo.bar' where 'bar' is an attribute of the 'foo' namespace.)

NAME and VALUE are separated by an '=' (equals) character. Whitespace before the '=' is not permitted. Everything after the '=' is the VALUE.

VALUE can contain any characters except newline, and may be 0 or more characters in length. 

Each line must end in a newline (ASCII 10) character.

The Parser class provides backslash escaping for the following characters in VALUE:
	\n --> newline character (ASCII 10)
	\r --> return character (ASCII 13)
	\t --> tab character (ASCII 9)
	\\ --> \


2. Key-value blocks are indicated by the line:

NAME:

followed by zero or more lines containing simple key-value pairs and/or blocks indented with a single tab character (ASCII 9).

The colon must be followed immediately by a newline character; trailing whitespace and other characters is not allowed.

Blocks can be nested within other blocks to any depth.


3. Empty lines and lines containing only tabs are permitted; these are simply ignored.


4. Full-line comments are permitted; any line beginning with zero or more tabs followed by '#' is ignored.


5. The parser will, by default, raise a ParseError if it encounters a malformed key-value item or block, or an incorrectly indented line. This behaviour can be overridden in subclasses if desired.


#######
NOTES

- See parser classes and test code for more information and examples of use.

- The restricted NAME format ensures names can be directly mapped to C-style identifiers simply by substituting the hyphen with an underscore.

- kvparser doesn't [yet?] provide any special features for working with NAME namespaces.

"""

# kvparser -- A simple key-value text parser with support for nested blocks.
#
# Copyright (C) 2004 HAS <hamish.sanderson@virgin.net>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

# coding = utf-8
import re as _re

_emptyLinePattern = _re.compile('\t*$|\t*#')
_parseLinePattern = _re.compile('(\t*)([.a-zA-Z][.a-zA-Z0-9-]+)(?:(:)|=(.*))')


class ParseError(Exception):
    def __init__(self, msg, lineNo, lineStr):
        self.msg = msg
        self.lineNo = lineNo
        self.lineStr = lineStr

    def __str__(self):
        return self.msg + ' at line %i: %r' % (self.lineNo, self.lineStr)


class Parser:
    """Subclass this and override parsing event handlers to do useful work."""

    lineDelimiter = '\n'
    escapeChar = '`'
    charSubs = 'r\r', 'n\n', 't\t'

    def unescape(self, s):
        """Unescape value part of a key=value pair."""
        for old, new in self.charSubs + (self.escapeChar * 2,):
            s = s.replace(self.escapeChar + old, new)
        return s

    # Main method; call it with the text to be parsed as its sole argument

    def parse(self, text):
        # TO DO: change 'ParseError' usage to 'parseError' events so that
        # subclasses can provide their own error handling/recovery behaviour.
        lines = text.split(self.lineDelimiter)
        blockDepth = 0
        for lineNo in range(len(lines)):
            lineStr = lines[lineNo]
            if not _emptyLinePattern.match(lineStr):
                lineMatch = _parseLinePattern.match(lineStr)
                if not lineMatch:
                    self.parseError('Malformed line', lineNo, lineStr)
                indentStr, name, isBlock, value = lineMatch.groups()
                depth = len(indentStr)
                if depth > blockDepth:
                    self.parseError('Bad indentation', lineNo, lineStr)
                while depth < blockDepth:
                    blockDepth -= 1
                    self.closeBlock()
                if isBlock:
                    self.openBlock(name)
                    blockDepth += 1
                else:
                    self.addItem(name, self.unescape(value))
        for _ in range(blockDepth):
            self.closeBlock()

    # Optionally override the following error event handler to provide your own error handling:

    def parseError(self, desc, lineNo, lineStr):
        raise ParseError(desc, lineNo, lineStr)

    # Override the following parser event handlers:

    def openBlock(self, name):
        pass

    def addItem(self, name, value):
        pass

    def closeBlock(self):
        pass


class TestParser(Parser):
    def openBlock(self, name):
        print 'OPEN %r' % name

    def addItem(self, name, value):
        print 'ADD %r %r' % (name, value)

    def closeBlock(self):
        print 'CLOSE'


#######


class ListParser(Parser):
    """Use to parse text into a nested list; e.g.

            foo=1
            bar:
                baz=3

        produces:

            [
                ('foo', '1'), 
                ('bar', [
                    ('baz', '3')
                    ]
                )
            ]

    """

    class _Stack:
        def __init__(self, lst): self.__stack = lst

        def push(self, val): self.__stack.append(val)

        def pop(self): return self.__stack.pop()

        def top(self): return self.__stack[-1]

        def depth(self): return len(self.__stack)

    def parse(self, text):
        self.stack = self._Stack(
            [(None, [])])  # each stack entry is two-item tuple: (block name, list of items in block)
        Parser.parse(self, text)
        result = self.stack.pop()[1]
        del self.stack
        return result

    def openBlock(self, name):
        self.stack.push((name, []))

    def addItem(self, name, value):
        self.stack.top()[1].append((name, value))

    def closeBlock(self):
        block = self.stack.pop()
        self.stack.top()[1].append(block)


#######
# TEST

if __name__ == '__main__':
    s = """
	# this is a comment line
email:
	address=user@domain
	real-name=Real Name

encryption:
	format=PGP
	key=some key
connection:
	address=123.123.123.123
	port=99
	connection-type=INET
	address-type=IP4
"""
    TestParser().parse(s)
    print
    print ListParser().parse(s)

