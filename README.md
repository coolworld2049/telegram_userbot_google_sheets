[![][black-shield]][black]

[black]: http://github.com/psf/black

[black-shield]: https://img.shields.io/badge/code%20style-black-black.svg?style=for-the-badge&labelColor=gray

# Telegram userbot for google sheets

Install [event_handler.gs](google-scripts/event_handler.gs) in "Extensions > Apps Scripts"

Then modify variables

```js
let domain = "";
let api_key = "";
let spreadsheetId = "";
let sheetName = "Sheet";
let logSheetName = "LogSheet";
let headersRange = "A1:S1";
let onEditRange = [13, 19];
let columnTelegramUsername = ``;
let columnUserProblem = ``;
let notificationMessageColumnRange = [11, 15];
```

Create a API account here: https://my.telegram.org/apps

`pip install pyrogram
`

`python src/session_maker/maker.py
`

`bash cli.sh startup
`

Application launched on https://127.0.0.1:80/docs

## Example

![Запросы_Единого_Окна - Google Таблицы](https://github.com/coolworld2049/telegram_userbot_google_sheets/assets/82733942/4ac8c19f-1d6e-4642-9670-9afdf1746f6a)


