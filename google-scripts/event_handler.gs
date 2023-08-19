let domain = "";
let api_key = "";
let spreadsheetId = "";
let sheetName  = "Sheet";
let logSheetName = "LogSheet";
let headersRange = "A1:S1";
let onEditRange = [13,19];
let columnTelegramUsername = "Укажите пожалуйста свой телеграмм через @";
let columnUserProblem = `Опишите проблему подробнее

Почему это важно?
Укажите факты, которые подтверждают необходимость подсветки.
УТП или другие детали.`;
let notificationMessageColumnRange = [11, 15];
const logger = {
  log:(val)=>{
    SpreadsheetApp.openById(spreadsheetId).getSheetByName(logSheetName).appendRow([new Date(), `${val}`]);
  }
};

function sendTelegramMessage(e, username, payloadData) {
  let apiUrl = `https://${domain}/telegram/send_message`;
  let payload = {
    'chat_id': username,
    'data': payloadData,
    'event': e,
    'user_problem_column_name': columnUserProblem,
    'notification_message_column_range': notificationMessageColumnRange
  };
  let headers = {
    'api_key': api_key
  };
  let options = {
    'method' : 'post',
    'accept': 'application/json',
    'contentType': 'application/json',
    'payload' : JSON.stringify(payload),
    'headers': headers
  };
  try
  {
    logger.log(`make POST request to ${apiUrl} with data ${JSON.stringify(options)}]`)
    let response = UrlFetchApp.fetch(apiUrl, options);
    logger.log(`responseCode ${response.getResponseCode()}, contentText ${response.getContentText()}`);
    return response.getContentText();
  }
  catch (error){
    logger.log(error)
  }
}

function doEdit(e) {
  let spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let activeSheet = spreadsheet.getActiveSheet();
  if ((activeSheet.getSheetName() != sheetName) || (e.oldValue == e.value)) {
    logger.log("Active is not target sheet");
    return null;
  }
  if (e.range.columnStart > onEditRange[0] && e.range.columnEnd <= onEditRange[1]){
    logger.log(`doEdit triggered on event: ${JSON.stringify(e)}`);
    const sheet = SpreadsheetApp.openById(spreadsheetId).getSheetByName(sheetName);

    let headersData = sheet.getRange(headersRange).getValues();
    let editedValues = sheet.getRange(e.range.rowStart, 1, 1, sheet.getLastColumn()).getValues();
    let rowData = editedValues[0];
    let rowObject = {};

    for (let j = 0; j < headersData[0].length; j++) {
      rowObject[headersData[0][j]] = rowData[j];
    }
    logger.log((JSON.stringify(rowObject)));
    let respData = sendTelegramMessage(e, rowObject[columnTelegramUsername], rowObject);
    let respDataObj = JSON.parse(respData);

    respDataObj.message_id ? sheet.getRange(e.range.rowStart, 18).setValue(respDataObj.message_id) : null;
    sheet.getRange(e.range.rowStart, 19).setValue(respDataObj.is_notified).insertCheckboxes();
    logger.log("--------------------------------------------")
  } else {
    logger.log(`columnStart=${e.columnStart}) not in onEditRange=${onEditRange.toString()}`);
  }
}