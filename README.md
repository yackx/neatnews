# neatnews

**A news aggregator running on FastAPI. Read the news without the hassle.**

Currently supported:

- [Le Soir](https://lesoir.be)
- [La Libre](https://lalibre.be)
- [Le Vif](https://levif.be)

This project is provided for educational and personal use.

## Install

Tech stack:

- [FastAPI](https://fastapi.tiangolo.com/) - fast Python async web server
- [Jinja](https://jinja.palletsprojects.com/) - templating engine
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/) - HTML parser
- [Uvicorn](https://www.uvicorn.org/) - ASGI web server implementation for Python

You need to have Python 3.10 installed.

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Run

```
(venv) $ uvicorn main:app --reload
```

## Deploy

Deployment files for Heroku are included in the project. Refer to Heroku documentation to deploy the project to a private instance.

## Caveats

This is a "scratch your own itch" project intended for personal use. The source code is provided for educational purpose.

Some headlines may be missing. Some fragments like links to Twitter are not supported. Video and images are not supported by design.

## License

Licensed under GNU General Public License v3

[Favicon](static/favicon.ico) by [twemoji](https://twemoji.twitter.com/) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)