function parseArgs(args) {
  args = (args || {}).parameters || {};
  var parsed = {};
  
  for(var key in args) {
    parsed[key] = args[key][0];
  }
  
  return parsed;
}

function doGet(args) {
  var params = parseArgs(args);
  
  Tracker.init(
    Config.spreadsheet,
    Config.activeJobsSheet,
    Config.doneJobsSheet
  );
  
  if(params.action === 'start') {
    Tracker.start(params.name, params.taskId)
  } else if (params.action === 'step') {
    Tracker.step(params.taskId, params.message);
  } else if (params.action === 'progress') {
    Tracker.progress(params.taskId, params.progress);
  } else if(params.action === 'finish') {
    Tracker.finish(params.taskId);
  }
  
  var template = HtmlService.createHtmlOutput();
  template.append(parseArgs(args).toSource());
  return template;
  
}
