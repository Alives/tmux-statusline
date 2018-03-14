#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Network module for tmux-statusline."""


import os
from subprocess import PIPE, Popen
from time import time


class Network():
  """Get network stats and return throughput rates.

  This class determines the statistics for all local network adapters other than
  lo and determines the rate since the last query. It then humanizes the output
  into b/s, KB/s, MB/s, or GB/s.
  """
  PREFIX = '#[fg=colour27,bg=colour0]#[bg=colour27]'
  SUFFIX = '#[fg=colour0,bg=colour27]#[bg=colour0]'

  def __init__(self, conf):
    self.os_type = os.uname()[0]
    if 'interface' in conf:
      self.interface = conf['interface']
    else:
      self.interface = 'all'
    self.prev_stats = {'rxbytes': 0, 'txbytes': 0, 'time': 0}
    self.curr_stats = {'rxbytes': 0, 'txbytes': 0, 'time': 0}
    self.rates = {'rx': {'icon': '↓', 'rate': 0, 'units': ''},
                  'tx': {'icon': '↑', 'rate': 0, 'units': ''}}
    self.Update()

  def GetNetBytes(self):
    """Get network statistics depending on platform.

    Sums the interface statistics for all interfaces other than lo and records
    the time they were captured.
    """
    self.curr_stats['rxbytes'] = 0
    self.curr_stats['txbytes'] = 0
    interfaces = []
    if self.os_type == 'Darwin':
      output = Popen(['netstat', '-nbi'], stdout=PIPE,
          shell=False).communicate()[0]
      self.curr_stats['time'] = time()
      for line in output.split('\n'):
        data = line.split()
        if len(data) < 10:
          continue
        if 'lo' in data[0] or 'Name' in data[0]:
          continue
        interface = data[0]
        if interface != self.interface and self.interface != 'all':
          continue
        if interface in interfaces:
          continue
        try:
          self.curr_stats['rxbytes'] += int(data[6])
          self.curr_stats['txbytes'] += int(data[9])
        except:
          continue
        interfaces.append(interface)

    elif self.os_type == 'Linux':
      proc_net_dev = open('/proc/net/dev')
      output = proc_net_dev.readlines()
      proc_net_dev.close()
      self.curr_stats['time'] = time()
      if self.interface not in output:
        self.interface = 'all'
      for line in output:
        data = line.split()
        if 'lo' in data or 'Inter-' in data or 'face' in data:
          continue
        interface = data[0].split(':')[0]
        if interface != self.interface and self.interface != 'all':
          continue
        if interface in interfaces:
          continue
        try:
          self.curr_stats['rxbytes'] += int(data[1])
          self.curr_stats['txbytes'] += int(data[9])
        except:
          continue
        interfaces.append(interface)

    return

  def GetRates(self):
    """Determine the rate of change since the last collection."""
    delta_time = self.curr_stats['time'] - self.prev_stats['time']
    for key in self.rates.keys():
      byte_key = '%sbytes' % key
      try:
        self.rates[key]['rate'] = (
            (self.curr_stats[byte_key] - self.prev_stats[byte_key]) / delta_time)
      except:
        self.rates[key]['rate'] = 0

  def GetUnits(self):
    """Convert to human readable units."""
    for key in self.rates.keys():
      rate = self.rates[key]['rate']
      units = ''
      if rate >= 1073741824:
        units = 'GB/s'
        rate = str(rate / 1073741824.0)[0:4]
      elif rate >= 1048576:
        units = 'MB/s'
        rate = str(rate / 1048576.0)[0:4]
      elif rate >= 1024:
        units = 'KB/s'
        rate = str(rate / 1024.0)[0:4]
      else:
        units = ' b/s'
        rate = str(rate)[0:4]

      if rate[-1] == '.':
        rate = '%s ' % rate[0:-1]
      self.rates[key]['rate'] = rate
      self.rates[key]['units'] = units

  def GetStatusLine(self):
    for key in self.curr_stats:
      self.prev_stats[key] = self.curr_stats[key]
    status = '%s ' % self.PREFIX
    for key in self.rates.keys():
      status += ('#[fg=colour249]%s#[fg=colour255]%s#[fg=colour249]%s ' %
                 (self.rates[key]['icon'], self.rates[key]['rate'],
                  self.rates[key]['units']))
    status += self.SUFFIX
    self.status_line = status
    return

  def Update(self):
    """Update the stats and return them."""
    self.GetNetBytes()
    self.GetRates()
    self.GetUnits()
    self.GetStatusLine()
    return self.status_line
