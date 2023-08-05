# chrys

[![CircleCI](https://circleci.com/gh/netbek/chrys.svg?style=svg)](https://circleci.com/gh/netbek/chrys)

A collection of color palettes for visualisation in JavaScript, Python and Sass.

## Demo

[netbek.github.io/chrys](https://netbek.github.io/chrys#colour-schemes)

## Installation

### Node.js and Sass

```shell
npm install chrys
```

### Python 3.6 and up

```shell
pip install chrys
```

## Usage

For instructions, refer to [the docs](https://netbek.github.io/chrys#usage).

## Development

Install Node and Python dependencies:

```shell
./scripts/install.sh
```

Build palette data:

```shell
npm run build-data
```

Build JavaScript and Python distribution packages, Sass, CSS, Illustrator scripts:

```shell
npm run build-dist
```

Deploy documentation to GitHub Pages:

```shell
npm run deploy
```

Publish JavaScript and Python distribution packages:

```shell
npm publish
```

## Credit

Palettes from:

* [Bokeh](https://github.com/bokeh/bokeh) (BSD 3-Clause)
* [Vega](https://github.com/vega/vega) (BSD 3-Clause)

## License

Copyright (c) 2017 Hein Bekker. Licensed under the BSD 3-Clause License.
