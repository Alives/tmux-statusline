#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Clock module for tmux-statusline."""


from time import strftime


class Clock():
  """Get the current time and return it for output."""
  PREFIX = '#[fg=colour220,bg=colour0]#[fg=colour0,bg=colour220]'
  SUFFIX = '#[default]'

  def Update(self):
    time_str = strftime('%l:%M:%S %p').lstrip()
    status = '%s %s %s' % (self.PREFIX, time_str, self.SUFFIX)
    return status
