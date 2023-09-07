<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

<p align="center">
  <img src="./resources/extras/logo_readme.jpg" alt="Logo">
</p>
<h1 align="center">
  <b>OreO - UserBot</b>
</h1>

<b>A stable pluggable Telegram userbot + Voice & Video Call music bot, based on Telethon.</b>

[![](https://img.shields.io/badge/OreO-v0.9-crimson)](#)
[![Stars](https://img.shields.io/github/stars/itzNightmare17/OREO?style=flat-square&color=yellow)](https://github.com/itzNightmare17/OREO/stargazers)
[![Forks](https://img.shields.io/github/forks/itzNightmare17/OREO?style=flat-square&color=orange)](https://github.com/itzNightmare17/OREO/fork)
[![Size](https://img.shields.io/github/repo-size/itzNightmare17/OREO?style=flat-square&color=green)](https://github.com/itzNightmare17/OREO/)   
[![Python](https://img.shields.io/badge/Python-v3.10.3-blue)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/itzNightmare17/OREO/graphs/commit-activity)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/itzNightmare17/OREO)
[![Contributors](https://img.shields.io/github/contributors/itzNightmare17/OREO?style=flat-square&color=green)](https://github.com/itzNightmare17/OREO/graphs/contributors)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![License](https://img.shields.io/badge/License-AGPL-blue)](https://github.com/itzNightmare17/OREO/blob/main/LICENSE)
----

### Local / VPS Deploy
- Get your [Necessary Variables](#Necessary-Variables)
- Clone the repository:    
  - `git clone https://github.com/itzNightmare17/Oreo oreo`
- Go to the cloned folder:
  - `cd oreo`
- Create a virtual env:      
  - `virtualenv -p /usr/bin/python3 venv`

  - `. ./venv/bin/activate`
- Install the requirements:      
  - `pip(3) install -r reso*/star*/optional-requirements.txt`

  - `pip(3) install -r requirements.txt`
- Generate your `SESSION`:
  - From Telegram Bot : [@StringFatherBot](https://t.me/StringFatherBot)
- Fill your details in a `.env` file, as given in [`.env.sample`](https://github.com/itzNightmare17/OREO/blob/main/.env.sample).
(You can either edit and rename the file or make a new file named `.env`.)
- Make `screen`:
  - `screen -S oreo`
- Run the bot:
  - Linux Users:
   `bash startup`
  - ubuntu users:
    `python(3) -m pyOreo`
  - Windows Users:
    `python(3) -m pyOreo`
- Detach `screen`:
  - `Ctrl+A` & `Ctrl+D`
---

## Necessary Variables
- `SESSION` - SessionString for your accounts login session. Get it from [@StringFatherBot](https://t.me/StringFatherBot)

One of the following database:
- For **Redis** (tutorial [here](./resources/extras/redistut.md))
  - `REDIS_URI` - Redis endpoint URI, from [redislabs](http://redislabs.com/).
  - `REDIS_PASSWORD` - Redis endpoint Password, from [redislabs](http://redislabs.com/).
- For **MONGODB**
  - `MONGO_URI` - Get it from [mongodb](https://mongodb.com/atlas).
- For **SQLDB**
  - `DATABASE_URL`- Get it from [elephantsql](https://elephantsql.com).

---

# License
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
OreO is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

---

# Credits
* [Lonami](https://github.com/LonamiWebs/) for [Telethon.](https://github.com/LonamiWebs/Telethon)
* [MarshalX](https://github.com/MarshalX) for [PyTgCalls.](https://github.com/MarshalX/tgcalls)

> Made with 💕 by [@bad_OreO](https://t.me/bad_oreo).
