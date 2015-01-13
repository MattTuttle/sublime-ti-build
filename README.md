[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](README.md) [![Package Control](https://img.shields.io/badge/Package%20Control-Titanium%20Build-orange.svg?style=flat)](https://packagecontrol.io/packages/Titanium%20Build)

# Titanium Appcelerator build for Sublime Text

A build script for Appcelerator Titanium's CLI in Sublime Text. Select 'Titanium' from the Tools->Build System list to use. Each time you build you'll be prompted with build options.

## Features

* Quickly build and run a Titanium project (android, iphone, mobileweb)
* Pulls iOS provisioning profiles into a dropdown list when deploy to a device
* Syntax highlighting for Alloy TSS files
* Auto-completion (thanks to Tita plugin)
* Clean build directories

## Installation

The best way to install is to use [Package Control](http://wbond.net/sublime_packages/package_control) for Sublime Text. Search for "Titanium Build" as the package name.

## Usage

`super+b` - select build options from drop downs

or

`super+shift+p` then select `Build: Titanium` from the Command Palette - select build options from drop downs

## Todo

* Store presets for quick access (no need to go through 5 different quick panels)

## Credits

* Auto completion pulled from Tita - https://github.com/tsteur/sublimetext-tita

## MIT License

Copyright (C) 2012-2015 Matt Tuttle

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
