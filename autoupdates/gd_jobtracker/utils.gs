var Utils = {
  getSheetByName: function(ss, name) {
    if(typeof ss == 'string') {
        ss = SpreadsheetApp.openByUrl(ss);
    }
    return _(ss.getSheets()).find(function(sheet) {
      return sheet.getName() == name;
    });
  },
  
  /*
   * Insert values 
   * 
   */
  insertValues: function(sheet, values, topLeft) {
    var range = sheet.getRange(topLeft.top, topLeft.left, 9999, values[0].length);
    
    // Strip empty strings
    var newValues = _(range.getValues()).filter(function(item) {
      return item[0] != '';
    });
    
    _(values).each(function(value) {
      
      // Key = item[1] -- taskId
      var sourceValue = _(newValues).find(function(item) {
        return item[1] == value[1];
      });
      
      // If new value is in spreadsheet (with the same key),
      // then replace old value with new one
      if(sourceValue) {
        for(var j = 0; j < value.length; j++) {
          sourceValue[j] = value[j];
        }
      } else {
        newValues.push(value);
      }
    });       
  
    var range = sheet.getRange(topLeft.top, topLeft.left, newValues.length, values[0].length);
    range.setValues(newValues);
  },
  
  sendBulkMail: function(emails, subject, body) {
    emails.forEach(function(email) {
      MailApp.sendEmail(email, subject, body);
    });    
  }
};
