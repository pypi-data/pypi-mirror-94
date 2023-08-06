import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1'
PACKAGE_NAME = 'jarvis-assistant'
AUTHOR = 'Michał Kacprzak'
AUTHOR_EMAIL = 'michal.kacprzak999@gmail.com'
URL = 'https://github.com/MichalKacprzak99/jarvis'

LICENSE = 'MIT License'
DESCRIPTION = 'Jarvis - Voice Personal Assistant'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'playsound',
      'gTTS',
      'requests',
      'pyjokes==0.6.0',
      'pyttsx3',
      'numpy',
      'pytemperature',
      'wikipedia',
      'textblob',
      'pymongo',
      'nltk',
      'SpeechRecognition',
      'pyaudio',
      'python-dotenv',
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,

      packages=find_packages(),

      )