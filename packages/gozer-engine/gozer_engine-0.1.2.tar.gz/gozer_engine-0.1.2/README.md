# Gozer: A Gopher Protocol Client

# About Gozer

Gozer is a terminal based browser for the Gopher protocol. It started a project I gave myself to explore the process of building something straight from an RFC spec. It adheres to the syntax specified in RFC [1436](https://tools.ietf.org/html/rfc1436) and RFC [4266](https://tools.ietf.org/html/rfc4266). 

![alt text](gozer-screencap.png "Gozer Screencap")

Gozer currently supports navigation to Gopherholes via command line argument, text input into the TUI interface and menu item selection in the TUI. The project uses [Lark](https://github.com/lark-parser/lark) as a dependency for parsing Gopher page source code. The TUI uses Python curses.

The project started as a simple client, but will shift into an extensible framework that will allow users to select and/or create their own frontends (e.g. picotui, blessed, PyQt, etc).

The project is currently in Alpha and is being actively developed. Bugs and feature requests are tracked in the Issues section this GitLab project.

## Installation
* If you want to install Gozer to a specific Python virtaul environment, activate that environment
* Clone this repo locally
* From the project root run `python -m setup.py`, this will generate a While file in the `dist` directory.
* Run `pip install path/to/wheel`

## Usage

Open a terminal and run `gozer`
| Keystroke | Action |
| --------- | ------ |
| g | Edit address bar |
| Enter | Submit address input into address bar or select highlighted link |
| Page up | Move up one page |
| Page down | Move down one page |
| Up arrow | Move up one line |
| Down arrow | Move down one line |
| Left arrow | Go back one page in history |
| Right arrow | Go forward one page in history |
| Tab | Jump to the next link |
| Shift+Tab | Jump to the previous link |
| q | Exit Gozer |

## Troubleshooting

### The installation process was successful, but when I run `gozer` I get a `command not found` error.

* This is due to the fact that the directory containing Gozer is not in your current PATH. Run `ls $(python -m site --user-base)/bin`. Is `gozer` there? If so, add its parent directory to your PATH. If not, check any other standard Python package binary locations for `gozer` or use the `find` command to search.

## TODO (As of 2021-01-24)
* Fix History Bug (#28)
* Add reload (#27)
* Reverse Cycle Through Links Bug (#15)
* Access plaintext URIs from CLI (#18)
* Add Sphinx Docs (#32)
* Publish Package to PyPI (#33)

## About Gopher

The Gopher protocol was an Internet protocol that was popular in the early 1990s. Created in 1991 (the same year as HTTP), it was one of the dominant competitors in the World Wide Web space in the early 1990s. Gopher's emphasis was on modeling a hierarchical file-like structure of content on the web and simplicity in implementing server and client software.

With an interface utilized menu-like functionality for navigating through web content, Gopher was suited for text based browsers. Lynx still currently maintains native Gopher support. Though Gopher was eventually overtaken in adoption by HTTP, a community of active Gopherholes continues to this day.

If you are unfamiliar with Gopher, these links will provide some context:

- [Wikipedia entry on Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol))
- [Floodgap Public Gopher Proxy](https://gopher.floodgap.com/gopher/gw)
- [DistroTube's video on Gopher](https://www.youtube.com/watch?v=lUBhOgK5zQI)
- [The Rise and Fall of the Gopher Protocol](https://www.minnpost.com/business/2016/08/rise-and-fall-gopher-protocol/)
- [Interview with the Developers of Gopher](https://www.youtube.com/watch?v=oR76UI7aTvs)
- [RFC 1436 - The Internet Gopher Protocol (a distributed document search and retrieval protocol)](https://tools.ietf.org/html/rfc1436)
- [RFC 4266 - The Gopher URI Scheme)](https://tools.ietf.org/html/rfc4266)

