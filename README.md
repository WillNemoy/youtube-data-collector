# new-york-times-data-collector
Collect New York Times article data based on a search topic.


## Setup


Create and activate a virtual environment:

```sh
conda create -n youtubeAPI-env python=3.8

conda activate youtubeAPI-env
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration


[Obtain an API Key](https://developer.nytimes.com/) from The New York Times Developer Network.

Then create a local ".env" file and provide the key like this:

```sh
# this is the ".env" file...

NY_API_KEY="__________"
```


## Usage

Run the program:

```sh
python app.py
```





