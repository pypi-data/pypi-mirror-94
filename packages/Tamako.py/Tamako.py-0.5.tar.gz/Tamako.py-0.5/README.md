# Tamako.py
An easy to use and actually updated Python wrapper for the Tamako API.

## State of the project:
The wrapper is in constent development and will continue to be. Everything in the Tamako API.

## How to install:
```py
Windows:
pip install Tamako.py
```
```py
Linux/MacOS:
pip install Tamako.py
```

## Getting Started
Using Tamako.py is quite simple, see the documentation for more details. Nearly all of the features included in this API wrapper work without any api keys. To use the ChatBot feature please take a look at the [Tamako documentation](https://tamako.tech/docs/api/chatapi).

## Quick example of the chatbot:

```py
chatbot = Tamako.chatbot(username='', app_secret='', app_id='', name='', gender='', prefix='', dev='', userid='', message='')
print(chatbot)
```

## A quick example of printing a joke:

```py
import Tamako
from Tamako import Tamako

joke = Tamako.joke()
print(joke)
```

## A quick example of printing lyrics of a song:

```py
lyrics = Tamako.lyrics(song_name='Lucid Dreams')
print(lyrics)
```

## A quick example of printing facts of an animal:

```py
fact = Tamako.animal_fact(animal='cat')
print(fact)
```

## A quick example of printing the url of an image

```py
img = Tamako.image(animal='bird')
print(img)
```
