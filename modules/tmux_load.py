#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Load average module for tmux-statusline."""


import os


class Load():
  """Get the current load and return it for output."""
  PREFIX = '#[fg=colour34,bg=colour0]#[fg=colour255,bg=colour34]'
  SUFFIX = '#[fg=colour0,bg=colour34]'

  def Update(self):
    load = ' '.join(['%0.2f' % x for x in os.getloadavg()])
    status = '%s %s %s' % (self.PREFIX, load, self.SUFFIX)
    return status
