# -*- coding: utf-8 -*-

"""
Filters for Markdown parsing in Jinja2 templates.
"""

from markdown import markdown

def markup(text, *args, **kwargs):
    """
    Parse text with markdown library.

    :param text:   - text for parsing;
    :param args:   - markdown arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
    :param kwargs: - markdown keyword arguments (http://freewisdom.org/projects/python-markdown/Using_as_a_Module);
    :return:       - parsed result.
    """
    return markdown(text, *args, **kwargs)