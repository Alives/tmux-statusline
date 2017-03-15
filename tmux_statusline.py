#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Generate an informative statusline for tmux.

Using classes defined within, output the right side of the status line for tmux
as a string when a client connects.  This uses sockets which has the advantage
of not running when it is not needed as the updates are only generated on
request.
"""


import json
import os
import signal
import socket
from modules.tmux_network import Network
from modules.tmux_load import Load
from modules.tmux_clock import Clock


class StatusLine():
  """The main statusline class."""
  HOST = '127.0.0.1'
  PORT = 61234
  STATUSLINE_LOCK = '%s/.tmux.statusline.pid' % os.environ['HOME']
  TMUX_CONF = '%s/.tmux.conf' % os.environ['HOME']

  def __init__(self):
    self.GetLock()
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  def CheckPid(self, pid):
    """Check if a pid is valid (running)."""
    try:
      os.kill(pid, 0)
    except:
      return False
    else:
      return True

  def UnLock(self):
    """Give up the lock."""
    os.unlink(self.STATUSLINE_LOCK)
    return

  def Lock(self):
    """Set the lock."""
    lock = open(self.STATUSLINE_LOCK, 'w')
    lock.write(str(os.getpid()))
    lock.close()

  def GetLock(self):
    """Simple process locking using a pid."""
    try:
      lock = open(self.STATUSLINE_LOCK)
      pid = int(lock.readline())
      lock.close()
    except:
      pid = None
    if not self.CheckPid(pid):
      self.Lock()
    else:
      print 'Can\'t get lock, another process is already running.'
      exit(1)
    return

  def SigHandler(self, SIG, FRM):
    print 'Caught signal %s, exiting.' % SIG
    self.sock.close()
    self.UnLock()
    exit(0)

  def Run(self, modules):
    """Listen on self.PORT for a connection and update stats and return them."""
    self.sock.bind((self.HOST, self.PORT))
    self.sock.listen(3)
    while True:
      conn = self.sock.accept()[0]
      statusline = ''
      for module in modules:
        statusline += '%s' % module.Update()
      conn.send(statusline)
      conn.close()


if __name__ == "__main__":
  conf_file = os.path.join(os.path.expanduser('~'), '.tmux_statuslinerc')
  if os.path.exists(conf_file):
    with open(conf_file) as f:
      conf = json.load(f)
    if 'network' not in conf or 'interface' not in conf['network']:
      conf['network'] = {'interface': 'all'}
  else:
    conf = {'network': {'interface': 'all'}}

  sl = StatusLine()

  # Setup the signal handler.
  for signum in [1, 2, 15]:
    signal.signal(signum, sl.SigHandler)

  # Setup modules.
  network = Network(conf['network'])
  load = Load()
  clock = Clock()

  # List modules in the order they should appear in the statusline output.
  sl.Run([network, load, clock])
