# Study Area Map Maker

This is a simple web program to create study area maps suitable for use within publications, journals, research papers, reports, etc.

## Features
- Customisable inset locator map
- Support for multiple distinct study areas
- Scale bar and north compass
- Native coordinate reference system (CRS) support

## Usage
### Local install
To install locally, download the source code and from the root directory (in a virtual environment):
1. `$ pip install .`
2. `$ fastapi dev src/studyareamapmaker/main.py`

Upon running the script, the URL to the website will be presented (http://127.0.0.1:8000 by default). 

### Website
A web-hosted instance of the API is located [here](https://studyareamapmaker.onrender.com). Please note that the website will take some time to boot up from hibernation at first, and the processing is very slow as it is freely hosted at the moment.

## Examples
![Study map example](https://github.com/derekchai/studyareamapmaker/blob/70738a853a6ad02eaa5a82a61d4fde74dd9b0cae/examples/mapmaker-example.png)
