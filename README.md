# extreme-feedback-tts

Yet another extreme feedback "lava lamp". This one is written in python and provides GUI and
audio output. Works with TeamCity build server API.

Application takes configuration JSON file via command line and based
on its definition watches all the builds defined in it.

# Usage

```
run.py -c path-to-config-json-fie [-g] [-f]

arguments:
  -c, --config          path to config file JSON
  -g, --gui             show also GUI
  -f, --fullscreen      show GUI in fullscreen mode (if GUI is requested)
```

# Dependencies

This application requires following python packages installed:

* gTTS
* pydub
* simpleaudio

You can install these as usual. With PIP, like this:

```
pip install -r requirements.txt
```

Moreover *pydub* needs some libraries installed on your system. Follow
[pydub dependencies link](https://github.com/jiaaro/pydub#dependencies).

*simpleaudio* needs ALSA when used on Linux. Anyway check its
[installation notes link](https://simpleaudio.readthedocs.io/en/latest/installation.html).

## Audio output

For audio output, audio files are used. These are created by Google Translate text-to-speech API
and saved as wav files (converted from mp3 to wav). During first run of the application with
concrete configuration file, audio files are saved to *assets* sub-directory.

You can define some audio messages by your own in definition of configuration file.

# Configuration file structure definition

Sample configuration:

```
{
    "build_server_url": "http://localhost:1880/",
    "tts_lang": "en",
    "builds": [
        {
            "build_type_id": "TeamCity_buildId_of_build_job",
            "branch": "master",
            "tts_name": "Awesome project",
            "gui_name": "Awesomme project x86"
        }
    ],
    "users": [
        {
            "team_city_name": "Pavel Hromada",
            "tts_name": "Pavel Hromada"
        }
    ],
    "tts_messages": {
        "you_broke_build": "you broke build",
        "build_success_again": "build is okay again. Thanks God.",
        "build_ongoing": "is building. I hope everything will be okay."
    }
}
```
