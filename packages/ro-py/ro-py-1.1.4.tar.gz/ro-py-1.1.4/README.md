<h1 align="center">
    <img src="https://raw.githubusercontent.com/rbx-libdev/ro.py/main/resources/header.png" alt="ro.py" width="400" />
    <br>
</h1>
<h4 align="center">ro.py is a powerful Python 3 wrapper for the Roblox Web API by <a href="https://github.com/jmkd3v">@jmkd3v</a> and <a href="https://github.com/iranathan">@iranathan</a>.</h4>

<p align="center">
    <a href="https://j-mk.ml/ro.py"><img src="https://img.shields.io/discord/761603917490159676?style=flat-square&logo=discord" alt="ro.py Discord"/></a>
    <a href="https://pypi.org/project/ro-py/"><img src="https://img.shields.io/pypi/v/ro-py?style=flat-square" alt="ro.py PyPI"/></a>
    <a href="https://pypi.org/project/ro-py/"><img src="https://img.shields.io/pypi/dm/ro-py?style=flat-square" alt="ro.py PyPI Downloads"/></a>
    <a href="https://pypi.org/project/ro-py/"><img src="https://img.shields.io/pypi/l/ro-py?style=flat-square" alt="ro.py PyPI License"/></a>
    <a href="https://github.com/rbx-libdev/ro.py"><img src="https://img.shields.io/github/commit-activity/w/rbx-libdev/ro.py?style=flat-square" alt="ro.py GitHub Commit Activity"/></a>
    <a href="https://github.com/rbx-libdev/ro.py"><img src="https://img.shields.io/github/last-commit/rbx-libdev/ro.py?style=flat-square" alt="ro.py GitHub Last Commit"/></a>
</p>

<p align="center">
    <a href="#information">Information</a> |
    <a href="http://j-mk.ml/ro.py">Discord</a> |
    <a href="#requirements">Requirements</a> |
    <a href="#disclaimer">Disclaimer</a> |
    <a href="#documentation">Documentation</a> |
    <a href="https://github.com/rbx-libdev/ro.py/tree/main/examples">Examples</a> |
    <a href="#credits">Credits</a> |
    <a href="https://github.com/rbx-libdev/ro.py/blob/main/LICENSE">License</a>
</p>

## Information
Welcome, and thank you for using ro.py!  
ro.py is an object oriented, asynchronous wrapper for the Roblox Web API (and other Roblox-related APIs) with many new and interesting features.  
ro.py allows you to automate much of what you would do on the Roblox website and on other Roblox-related websites.

## Update: ro.py on Discord
I’ve set up a small ro.py Discord server. It’s obviously very tiny, but some of you can be the first people to help found the server. If you need support for the library, you can ask your questions here if you need faster support. http://j-mk.ml/ro.py

## Get Started
If you are looking for a full tutorial on ro.py, check out [the new DevForum article!](https://devforum.roblox.com/t/use-python-to-interact-with-the-roblox-api-with-ro-py/1006465)

## Requirements
- httpx (for sending requests)
- iso8601 (for parsing dates)
- signalrcore (for recieving notifications)

#### Previous Requirements
- cachecontrol (for caching requests)
- requests-async (for sending requests, might be updated to a new lib soon)
- ~~pytweening (for animations, see below)~~
- ~~wxPython (for the "prompts" extension, optional)~~
- ~~wxasync (see above)~~

#### Prompts Extension Requirements
You'll need to install `wxPython`, `wxasync` and `pytweening` to use the prompts extension. If it is not present, an error will be raised. 

## Disclaimer
We are not responsible for any malicious use of this library.  
If you use this library in a way that violates the [Roblox Terms of Use](https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use) your account may be punished.

## Documentation
You can view documentation for ro.py at [ro.py.jmksite.dev](https://ro.py.jmksite.dev/).  
If something's missing from docs, feel free to dive into the code and read the docstrings as most things are documented there.
The docs are generated from docstrings in the code using pdoc3.

## Installation
You can install ro.py from pip:
```
pip install ro-py
```
If you want the latest bleeding-edge version, clone from git (you'll need [git-scm](https://git-scm.com/downloads) installed):
```
pip install git+git://github.com/rbx-libdev/ro.py.git
```
Known issue: wxPython sometimes has trouble building on certain devices. I put wxPython last on the requirements so Python attempts to install it last, so you can safely ignore this error as everything else should be installed.

## Contributors
<a href="https://github.com/rbx-libdev/ro.py/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=rbx-libdev/ro.py" />
</a>


## Other Libraries
ro.py not for you? Come check out these other libraries!
Name                                                        | Language   | OOP     | Async | Maintained | More Info                       |
------------------------------------------------------------|------------|---------|-------|------------|---------------------------------|
[ro.py](https://github.com/rbx-libdev/ro.py)                | Python 3   | Yes     | Yes   | Yes        | You are here!                   |
[robloxapi](https://github.com/iranathan/robloxapi)         | Python 3   | Yes     | Yes   | No         | Predecessor to ro.py.           |
[robloxlib](https://github.com/NoahCristino/robloxlib)      | Python 3   | Yes?    | No    | No         |                                 |
[pyblox](https://github.com/RbxAPI/Pyblox)                  | Python 3   | Partial | No    | Yes        |                                 |
[bloxy](https://github.com/Visualizememe/bloxy)             | Node.JS    | Yes     | Yes   | Yes        |                                 |
[noblox.js](https://github.com/suufi/noblox.js)             | Node.JS    | No      | Yes   | Yes        |                                 |
[roblox.js](https://github.com/sentanos/roblox-js)          | Node.JS    | No      | Yes?  | No         | Predecessor to noblox.js.       |
[cblox](https://github.com/Meqolo/cblox)                    | C++        | Yes     | No?   | Yes        |                                 |
[robloxapi](https://github.com/gamenew09/RobloxAPI)         | C#         | Yes     | Yes   | Maybe      |                                 |
[roblox4j](https://github.com/PizzaCrust/Roblox4j)          | Java       | Yes     | No?   | No         |                                 |
[javablox](https://github.com/RbxAPI/Javablox)              | Java       | Yes     | No?   | No         |                                 | 
robloxkt                                                    | Kotlin     | ?       | ?     | No         | I have no information on this.  |
[KotlinRoblox](https://github.com/PizzaCrust/KotlinRoblox)  | Kotlin     | Yes?    | No?   | No         |                                 |
[rbx.lua](https://github.com/iiToxicity/rbx.lua)            | Lua        | N/A     | No?   | Yes?       |                                 |
robloxcomm                                                  | Lua        | N/A     | ?     | ?          | Again, no info on this or link. |
[tsblox](https://github.com/Dionysusnu/TSBlox)              | TypeScript | Yes     | Yes   | No         |                                 | 
roblophp                                                    | PHP        | ?       | ?     | ?          | Repo seems to be deleted.       |
