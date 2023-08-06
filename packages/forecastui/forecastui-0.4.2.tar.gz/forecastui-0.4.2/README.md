# ForecastUI

An user interface designed to acquire and log data from the Forecast board.

Currently the main user interface of the [Forecast Framework](https://gitlab.com/altairLab/elasticteam/forecastnucleoframework)

<div align="center"><img src="client/src/assets/logo.svg" height="256"/></div>

[[_TOC_]]

## How to install

### Linux

Refer to the automated installer [script collection](https://gitlab.com/altairLab/elasticteam/forecast/get-forecast)

### Windows
Make sure to have Python installed (version >= 3.5), otherwise download it from [here](https://www.python.org).
```bash
pip install forecastui
```

### From source
Installing from source is not recommended and should be done only by developers and maintainers.

Still here? You are required to have node installed to compile the frontend. As such I suggest [nvm](https://github.com/nvm-sh/nvm) to manage nodejs versions.

Clone the repository
```bash
git clone https://gitlab.com/altairLab/elasticteam/forecast-atlas.git
cd forecast-atlas
```
Compile the frontend
```bash
make build
```
Install the package
```bash
pip install -e .
```

Start the app
```bash
forecastui
```

## License

Copyright © 2021 Altair Robotics Laboratory

This program comes with absolutely no warranty. See the [MIT License](LICENSE) for details.