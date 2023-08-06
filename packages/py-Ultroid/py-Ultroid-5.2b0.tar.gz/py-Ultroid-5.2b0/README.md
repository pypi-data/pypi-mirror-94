# Ultroid - UserBot
A stable pluggable Telegram userbot, based on Telethon.

![Python Version](https://img.shields.io/badge/Python-v3.9-red)
![Stars](https://img.shields.io/github/stars/CrazyCreatorr/ultroid)
![Forks](https://img.shields.io/github/forks/CrazyCreatorr/ultroid)
![Contributors](https://img.shields.io/github/contributors/TeamUltroid/Ultroid)
![License](https://img.shields.io/github/license/CrazyCreatorr/ultroid?style=flat-square)
![Size](https://img.shields.io/github/repo-size/CrazyCreatorr/ultroid)

<details>
<summary>More Info</summary>
<br>
  A stable, telethon based Telegram UserBot.  <br />
</details>

# Deploy 
- [Heroku](https://github.com/CrazyCreatorr/ultroid#Deploy-to-Heroku)
- [Local Machine](https://github.com/CrazyCreatorr/ultroid#Deploy-Locally)

## Deploy to Heroku
- Get your `API_ID` and `API_HASH` from [here](https://my.telegram.org/) and click the below button!  <br />  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Deploy Locally
- Get your `API_ID` and `API_HASH` from [here](https://my.telegram.org/)
- Clone the repository: <br />
`git clone https://github.com/TeamUltroid/Ultroid.git`
- Go to the cloned folder: <br />
`cd Ultroid`
- Create a virtual env:   <br />
`virtualenv -p /usr/bin/python3 venv`   
`. ./venv/bin/activate`
- Install the requirements:   <br />
`pip install -r requirements.txt`   
- Generate your `SESSION`:   
`bash sessiongen`
- Fill your details in a `.env` file, as given in [`.env.sample`](https://github.com/CrazyCreatorr/ultroid/blob/main/.env.sample).    
(You can either edit and rename the file or make a new file.)
- Run the bot:   
`python3 -m ultroid`

Made with 💕 by [@TeamUltroid](https://t.me/TeamUltroid). <br />

# Credits
* [Lonami](https://github.com/LonamiWebs/) for [Telethon](https://github.com/LonamiWebs/Telethon)

