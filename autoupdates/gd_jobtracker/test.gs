function expect(value) {
    return {
      toEqual: function(val) {
        if(value.toSource() !== val.toSource()) {
          throw new Error('Expected ' + val.toSource() + ' is ' + value.toSource());
        }
      }
    }
  }

function test() {
  /*
   * Utils.getSheetByName
   */  
  var ss = SpreadsheetApp.openByUrl('https://docs.google.com/a/valt.me/spreadsheet/ccc?key=0Ak38hVaEdUXmdGRVckpydFRIQTVuNFc0cXFsT1RDbFE#gid=1')
  var sheet1 = Utils.getSheetByName(ss, 'Sheet1');
  var sheet2 = Utils.getSheetByName(ss, 'Sheet2');  
  expect(sheet1.getName()).toEqual('Sheet1');       
  expect(sheet2.getName()).toEqual('Sheet2');
  
  var sheet = sheet1;
  

  /*
   * Delete all entries in Unit Test tab
   */
  var values = [];
  for(var i = 0; i < 10; i++) {
    var value = [];
    values.push(['', '', '', '', '', '']);
  }
  sheet.getRange(2,1,10,6).setValues(values);
  
  /*
   * Utils.insertValues
   */    
  var data = [[0.1, '101a'], [0.2, '102a'], [0.3, '103a']];
  var newData = [[0.1, '101a'], [0.2, '102a'], [0.3, '103a'], [0.4, '104a']];
  
  Utils.insertValues(sheet, data, {left: 1, top: 2});
  Utils.insertValues(sheet, newData, {left: 1, top: 2});
  expect(sheet.getRange(2,1,4,2).getValues()).toEqual(newData);    

  /*
   * Delete all entries in Sheet1 tab
   */
  var values = [];
  for(var i = 0; i < 10; i++) {
    var value = [];
    values.push(['', '', '', '', '', '']);
  }
  sheet.getRange(2,1,10,6).setValues(values);
  
  /*
   * Delete all entries in Sheet2 tab
   */
  var values = [];
  for(var i = 0; i < 10; i++) {
    var value = [];
    values.push(['', '', '', '', '', '']);
  }
  sheet2.getRange(2,1,10,6).setValues(values);

  

  /*
   * Tracker.init
   */
  Tracker.init(
    'https://docs.google.com/a/valt.me/spreadsheet/ccc?key=0Ak38hVaEdUXmdGRVckpydFRIQTVuNFc0cXFsT1RDbFE#gid=1', 
    'Sheet1', 
    'Sheet2'
  );

  /*
   * Tracker.start
   */  
  Tracker.start('update:groups', 'a1');
  Tracker.start('update:groups', 'b2');
  Tracker.start('update:posts', 'c3');
  
  var values = sheet.getRange(2,1,3,6).getValues();

  // set "started at" field to null and check if its type is Date
  values = _(values).map(function(value) {
    expect(value[2] instanceof Date).toEqual(true);
    value[2] = null;
    return value;
  });
  
  expect(values).toEqual([
    ['update:groups', 'a1', null, '<unknown>', '<unknown>', 'Not finished yet'],
    ['update:groups', 'b2', null, '<unknown>', '<unknown>', 'Not finished yet'],
    ['update:posts', 'c3', null, '<unknown>', '<unknown>', 'Not finished yet']
  ]);

  /*
   * Tracker.step
   */

  Tracker.step('c3', 'Step 3.1');

  Tracker.step('b2', 'Step 2.1');
  Tracker.step('a1', 'Step 1.1');
  
  Tracker.step('b2', 'Step 2.2');
  Tracker.step('c3', 'Step 3.2');
  
  Tracker.step('c3', 'Step 3.3');
  Tracker.start('update:something', 'd4');
  
  var values = sheet.getRange(2,1,4,6).getValues();

  // set "started at" field to null
  values = _(values).map(function(value) {
    value[2] = null;
    return value;
  });
  
  expect(values).toEqual([
    ['update:groups', 'a1', null, 'Step 1.1', '<unknown>', 'Not finished yet'],
    ['update:groups', 'b2', null, 'Step 2.2', '<unknown>', 'Not finished yet'],
    ['update:posts', 'c3', null, 'Step 3.3', '<unknown>', 'Not finished yet'],
    ['update:something', 'd4', null, '<unknown>', '<unknown>', 'Not finished yet']
  ]);
  
  /*
   * Tracker.progress
   */
  
  Tracker.progress('a1', '2/200');
  Tracker.progress('b2', '3/100');
  Tracker.progress('d4', '99/100');  
  
  var values = sheet.getRange(2,1,4,6).getValues();

  // set "started at" field to null
  values = _(values).map(function(value) {
    value[2] = null;
    return value;
  });
  
  expect(values).toEqual([
    ['update:groups', 'a1', null, 'Step 1.1', '2/200', 'Not finished yet'],
    ['update:groups', 'b2', null, 'Step 2.2', '3/100', 'Not finished yet'],
    ['update:posts', 'c3', null, 'Step 3.3', '<unknown>', 'Not finished yet'],
    ['update:something', 'd4', null, '<unknown>', '99/100', 'Not finished yet']
  ]);
  
  /*
   * Tracker.finish
   */
  Tracker.finish('a1');
  Tracker.finish('c3');

  var values = sheet1.getRange(2,1,2,6).getValues();

  // set "started at" field to null and check if its type is Date
  values = _(values).map(function(value) {
    value[2] = null;
    return value;
  });
  
  expect(values).toEqual([
    ['update:groups', 'b2', null, 'Step 2.2', '3/100', 'Not finished yet'],
    ['update:something', 'd4', null, '<unknown>', '99/100', 'Not finished yet']
  ]);  
 
  var values = sheet2.getRange(2,1,2,6).getValues();

  // set "started at" and "finished at" fields to null and check if its type is Date
  values = _(values).map(function(value) {
    expect(value[2] instanceof Date).toEqual(true);
    expect(value[5] instanceof Date).toEqual(true);
    value[2] = null;
    value[5] = null;
    return value;
  });
  
  expect(values).toEqual([
    ['update:groups', 'a1', null, 'Finished', '2/200', null],
    ['update:posts', 'c3', null, 'Finished', '<unknown>', null]
  ]);   
}
