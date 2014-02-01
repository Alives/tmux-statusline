tmux-statusline
===============

Python Tmux Statusline that runs in the background.

This uses the powerline format for output, but that can be easily changed.

[![Status Line](http://i.imgur.com/fuqjepo.png?1)](http://i.imgur.com/fuqjepo.png?1)

This should use much less resources than the tradtional bash scripts.  Also note that the updates are generated as needed, so if you are not attached, there should be no extra load on your system.

Use the `statusline.sh` script for your tmux status-right:

    set -g status-right "#(${HOME}/tmux-statusline/tmux_statusline.sh)"

Configure the python script to show the modules you want and the order you want.
