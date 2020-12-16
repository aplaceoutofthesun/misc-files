# -*- coding: utf-8 -*-
"""
    pygments.styles.harlequin

    Style based on the Harlequin vim scheme by whoever

"""

from pygments.style import Style
from pygments.token import (Comment,
                            Error,
                            Generic,
                            Keyword,
                            Name,
                            Number,
                            Operator,
                            Punctuation,
                            String,
                            Text,
                            Whitespace
                            )


class HarlequinStyle(Style):
    """Style based on the vim Harlequin colour scheme."""
#"text": "'#F8F8F2', 15"
# "text_bg": "'#1C1B1A', 234"
# "white": "'#FFFFFF', 15"
# "black": "'#000000', 0"
# "greys": "'#BEBEBE', 250, '#808080', 244, '#696969', 242,
#  '#545454', 240, '#343434', 236, '#080808', 232"
# "cerise": "'#FF0033', 197"
# "lime": "'#AEEE00', 154"
# "gold": "'#FFB829', 214"
# "brick": "'#CB4154', 167"
# "lilac": "'#AE81FF', 141"
# "frost": "'#2C89C7', 68"
# "sunny": "'#FFFC7F', 228"
# "mordant": "'#AE0C00', 124"
# "auburn": "'#7C0A02', 88"
# "moss": "'#004225', 22"

    default_style = ""

    styles = {
        Comment: 'italic #2c89c7',
        Comment.Preproc: '#2c89c7',
        Comment.Special: 'bold #2c89c7',

        Error: '#ae0c00',

        # Generic: '#080808',
        # Generic.Prompt: '#010101',

        Keyword: 'bold #ff006f',

        Name: '#f3f3f3',
        Name.Builtin: '#ffb829',
        Name.Constant: 'underline #ffb829',
        Name.Class: '#aeee00',
        Name.Function: '#ffb829',
        Name.Property: '#ff0033',

        Number: 'bold #be81ff',
        Number.Float: 'bold #ae81ff',
        Number.Integer: 'bold #ae81ff',
        Number.Hex: 'bold #ae81ff',
        Number.Oct: 'bold #ae81ff',
        Number.Bin: 'bold #ae81ff',

        Operator: '#ff0033',

        Punctuation: '#a0a0a0',

        String: '#fafc5f',
        String.Char: 'bold #ae81ff',
        String.Regex: '#fea1ff',
        String.Symbol: 'bold #fea1ff',

        Text: '#8f8f8f',

        Whitespace: '',
    }
