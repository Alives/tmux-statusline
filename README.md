tmux-statusline
===============

Python Tmux Statusline that runs in the background.

This should use much less resources than the tradtional bash scripts.  Also note that the updates are generated as needed, so if you are not attached, there should be no extra load on your system.

Use the `statusline.sh` script for your tmux status-right:

    set -g status-right "#(${HOME}/tmux-statusline/statusline.sh)"

Configure the python script to show the modules you want and the order you want.
