# websitediff

A small utility to check websites for changes.

## Usage

The tool expects a list of URLs in its configuration file (`$XDG_CONFIG_HOME/websitediff.conf`, defaults to `~/.config/websitediff.conf`) and checks all of them for modifications since the last time the tool ran. URLs can alternatively be passed on the command line; the configuration file is ignored in this case.

By default, the tool just prints the URLs that have changed. Modify the `print_diff` variable to get a textual diff.

## Configuration file format

One URL per line. Comments are started by #.

## Ideas

- Output an HTML rendering of the website with differences marked
