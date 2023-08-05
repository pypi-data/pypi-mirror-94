#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Viewer Team, all rights reserved

import sys
import datetime
import shutil

from glxviewer.utils import center_text
from glxviewer.utils import bracket_text
from glxviewer.utils import resize_text
from glxviewer.colors import Colors, convert_color_text_to_colors


class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args)
        return cls.instance


class Viewer(object, metaclass=Singleton):
    """
    The class viewer
    """

    def __init__(self):
        # protected variables
        self.__with_date = None
        self.__status_text = None
        self.__status_text_color = None
        self.__status_symbol = None
        self.__text_column_1 = None
        self.__text_column_2 = None
        self.__text_column_3 = None
        self.__size_line_actual = None
        self.__size_line_previous = None

        # init property's
        self.with_date = None
        self.status_text = None
        self.status_text_color = None
        self.status_symbol = None
        self.text_column_1 = None
        self.text_column_2 = None
        self.text_column_3 = None
        self.size_line_actual = None
        self.size_line_previous = None

    @property
    def with_date(self):
        """
        Property use for show date

        :return: with date property value
        :rtype: str
        """
        return self.__with_date

    @with_date.setter
    def with_date(self, value):
        """
        set the with_date property

        Default value is True

        :param value: the `with_date` property value
        :type value: bool
        :raise TypeError: if ``value`` is not a bool type
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError("'with_date' property must be a bool type")
        if self.with_date != value:
            self.__with_date = value

    @property
    def status_text(self):
        """
        Property it store text of the status text like "DEBUG" "LOAD"

        Later the Viewer will add bracket's around it text, and set the color during display post-processing.

        see: ``status_text_color`` property

        :return: status_text property value
        :rtype: str
        """
        return self.__status_text

    @status_text.setter
    def status_text(self, value=None):
        """
        Set the status_text property value

        :param value: the status_text property value
        :type value: str
        :raise TypeError: if ``value`` is not a str type
        """
        if value is None:
            value = "DEBUG"
        if type(value) != str:
            raise TypeError("'status_text' property must be a str type")
        if self.status_text != value:
            self.__status_text = value

    @property
    def allowed_colors(self):
        """
        Allowed colors:

        ORANGE, RED, RED2, YELLOW, YELLOW2, WHITE, WHITE2, CYAN, GREEN, GREEN2

        Note that Upper, Lower, Tittle case are allowed

        :return: A list of allowed colors
        :rtype: list
        """
        return ["ORANGE", "RED", "RED2", "YELLOW", "YELLOW2", "WHITE", "WHITE2", "CYAN", "GREEN", "GREEN2"]

    @property
    def status_text_color(self):
        """
        Property it store one allowed color value, it value will be use to display ``status_text`` color.

        see: ``status_text`` property for more details

        :return: the ``status_text_color`` property value
        :rtype: str
        """
        return self.__status_text_color

    @status_text_color.setter
    def status_text_color(self, value):
        """
        Set the value of the ``status_text_color`` property.

        see: ``allowed_colors`` for more details

        :param value: The ``status_text_color`` property value
        :type value: str
        :raise TypeError: When ``status_text_color`` is not a str
        :raise ValueError: When ``status_text_color`` value is not a allowed color
        """
        if value is None:
            value = "ORANGE"
        if type(value) != str:
            raise TypeError("'status_text_color' property must be a str type")
        if value.upper() not in self.allowed_colors:
            raise ValueError("{0} is not a valid color for 'status_text_color' property")
        if self.status_text_color != value:
            self.__status_text_color = value

    @property
    def status_symbol(self):
        """
        Property it store a symbol of one letter. like ! > < / - | generally for show you application fo something.

        it thing exist that because i use it for show if that a input or output message.

        Actually the symbol use CYAN color, and have 1 space character on the final template. Certainly something it can
        be improve. Will see in future need's ...

        :return: status_symbol character
        :rtype: str
        """
        return self.__status_symbol

    @status_symbol.setter
    def status_symbol(self, value):
        """"
        Set the symbol of ``status_symbol`` you want. Generally > or < or ?

        :param value: the symbol of ``status_symbol``
        :type value: str
        :raise TypeError: when ``status_symbol`` value is not a str type
        """
        if value is None:
            value = " "
        if type(value) != str:
            raise TypeError("'status_symbol' property must be set with str value")
        if self.status_symbol != value:
            self.__status_symbol = value

    @property
    def text_column_1(self):
        """
        Property it store ``text_column_1`` value. It value is use by template for display the column 1

        :return: The ``text_column_1`` value
        :rtype: str
        """
        return self.__text_column_1

    @text_column_1.setter
    def text_column_1(self, value):
        """
        Set the ``text_column_1`` value.

        :param value: The text you want display on it column
        :type value: str
        :raise TypeError: When ``text_column_1`` value is not a str type
        """
        if value is None:
            value = ""
        if type(value) != str:
            raise TypeError("'text_column_1' property must be set with str value")
        if self.text_column_1 != value:
            self.__text_column_1 = value

    @property
    def text_column_2(self):
        """
        Property it store ``text_column_2`` value. It value is use by template for display the column 2

        :return: The ``text_column_2`` value
        :rtype: str
        """
        return self.__text_column_2

    @text_column_2.setter
    def text_column_2(self, value):
        """
        Set the ``text_column_2`` value.

        :param value: The text you want display on it column
        :type value: str
        :raise TypeError: When ``text_column_2`` value is not a str type
        """
        if value is None:
            value = ""
        if type(value) != str:
            raise TypeError("'text_column_2' property must be set with str value")
        if self.text_column_2 != value:
            self.__text_column_2 = value

    @property
    def text_column_3(self):
        """
        Property it store ``text_column_3`` value. It value is use by template for display the column 3

        :return: The ``text_column_3`` value
        :rtype: str
        """
        return self.__text_column_3

    @text_column_3.setter
    def text_column_3(self, value):
        """
        Set the ``text_column_3`` value.

        :param value: The text you want display on it column
        :type value: str
        :raise TypeError: When ``text_column_3`` value is not a str type
        """
        if value is None:
            value = ""
        if type(value) != str:
            raise TypeError("'text_column_3' property must be set with str value")
        if self.text_column_3 != value:
            self.__text_column_3 = value

    @property
    def size_line_actual(self):
        return self.__size_line_actual

    @size_line_actual.setter
    def size_line_actual(self, value=None):
        if value is None:
            value = shutil.get_terminal_size()[0]
        if type(value) != int:
            raise TypeError("'size_line_actual' property value must be a int type or None")
        if self.size_line_actual != value:
            self.__size_line_actual = value

    @property
    def size_line_previous(self):
        return self.__size_line_previous

    @size_line_previous.setter
    def size_line_previous(self, value=None):
        if value is None:
            value = shutil.get_terminal_size()[0]
        if type(value) != int:
            raise TypeError("'size_line_previous' property value must be a int type or None")
        if self.size_line_previous != value:
            self.__size_line_previous = value

    @staticmethod
    def flush_a_new_line():
        """
        Flush a new line. It consist to a \n write on stdout
        """
        sys.stdout.write("\n")
        sys.stdout.flush()

    @property
    def formatted_date(self):
        return str(datetime.datetime.now().replace(microsecond=0).isoformat())

    def flush_infos(
            self,
            with_date=True,
            status_text="DEBUG",
            status_text_color="ORANGE",
            status_symbol=" ",
            column_1="",
            column_2="",
            column_3="",
            prompt=None,
    ):
        """
        Flush a line a bit like you want

        :param with_date: show date if True
        :type with_date: bool
        :param status_text: The text to display ton the status part
        :type status_text: str
        :param status_text_color: allowed : ORANGE, RED, RED2, YELLOW, YELLOW2, WHITE, WHITE2, CYAN, GREEN, GREEN2
        :type status_text_color: str
        :param status_symbol: str or None
        :param column_1: A Class name
        :type column_1: str or None
        :param column_2: The thing to print in column 2
        :type column_2: str or None
        :param column_3: The thing to print in column 3
        :type column_3: str or None
        :param prompt: value
        :type prompt: None, -1, +1
        """

        self.with_date = with_date
        self.status_text = status_text
        self.status_text_color = status_text_color
        self.status_symbol = status_symbol
        self.text_column_1 = column_1
        self.text_column_2 = column_2
        self.text_column_3 = column_3

        status_text_color = convert_color_text_to_colors(status_text_color)

        status_symbol_color = Colors.BOLD + Colors.CBEIGE

        # Status Clean up
        status_text = resize_text(text=status_text, max_width=5)
        status_text = center_text(text=status_text, max_width=5)
        status_text = bracket_text(text=status_text)

        # Column state
        if self.with_date:
            string_print = "{0:} {1:<5} {2:<3} {3:<10} {4:<10}".format(
                Colors.CWHITEBG + Colors.CGREY + self.formatted_date + Colors.end,
                status_text_color + status_text + Colors.end,
                status_symbol_color + self.status_symbol + Colors.end,
                self.text_column_1,
                self.text_column_2,
            )
            self.size_line_actual = len("{0:} {1:<5} {2:<3} {3:<10} {4:<10}".format(
                self.formatted_date,
                status_text,
                self.status_symbol,
                self.text_column_1,
                self.text_column_2
            ))
        else:
            string_print = "{0:<5} {1:<3} {2:<10} {3:<10}".format(
                status_text_color + status_text + Colors.end,
                status_symbol_color + status_symbol + Colors.end,
                self.text_column_1,
                self.text_column_2,
            )

            self.size_line_actual = len("{0:<5} {1:<3} {2:<10} {3:<10}".format(
                status_text, status_symbol, self.text_column_1, self.text_column_2
            ))

        sys.stdout.write(" " * shutil.get_terminal_size()[0])
        sys.stdout.write("\b" * shutil.get_terminal_size()[0])
        sys.stdout.write(string_print)

        if prompt is None:
            sys.stdout.write("\n")

        elif int(prompt) < 0:
            # sys.stdout.write("\b" * self.size_line_actual)
            sys.stdout.write("\b" * int(shutil.get_terminal_size()[0] - len(string_print)))
            if with_date:
                sys.stdout.write("\b" * self.size_line_actual)
            else:
                sys.stdout.write("\b" * int(len(string_print) - self.size_line_actual))
        else:
            sys.stdout.write("\b" * shutil.get_terminal_size()[0])

            # sys.stdout.write("\b" * shutil.get_terminal_size()[0])

        # Only on final flush, that because that ultra slow
        self.size_line_previous = len(string_print)

        # sys.stdout.write("\b" * shutil.get_terminal_size()[0])
        sys.stdout.flush()

        # lines = textwrap.wrap(
        #     str(text_column_2),
        #     width=int(_get_terminal_width() - 30)
        # )
        # count = 1
        # for line in lines:
        #     set_prompt_type(prompt)
        #     sys.stdout.write(' ')
        #     sys.stdout.write(line)
        #     sys.stdout.write('\n')
        #     line_length = len(line)
        #     sys.stdout.write("\b" * line_length)
        #     sys.stdout.flush()
        #     count += 1
