# **WORK IN PROGRESS**
Proper audio output logic is missing so far.

# extreme-feedback-tts

Yet another extreme feedback "lava lamp". This one is written in python and provides GUI and
audio output. Works with TeamCity build server API.

Application takes configuration JSON file via command line and based
on its definition watches all the builds defined in it.

# Usage

```
run.py -c path-to-config-json-file [-g] [-f] [-d]

arguments:
  -c, --config          path to config file JSON
  -g, --gui             show also GUI
  -f, --fullscreen      show GUI in fullscreen mode (if GUI is requested)
  -d, --debug           enable debug logs
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
        "status_all_unavailable": "I have issues to retrieve info about builds. Put an eye on it.",
        "status_all_ok": "All builds are building successfully. Keep it like this.",
        "status_all_ok_long_time": "Everything is fine for a long time. Thumbs up guys.",
        "status_all_nok_long_time": "Houston, we have a proble for some time. Check it immediately.",
        "status_unavailable": "Unable to get info about",
        "status_ok_again": "is okay again.",
        "status_nok": "build has failed.",
        "status_running": "build is running right now on build server.",
        "you_broke_build": "you broke the build. Fix it now dude.",
        "you_committed": "hope that thi will pass."
    }
}
```
