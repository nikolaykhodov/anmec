function tooLongRunningTasks() {
  Tracker.init(
    Config.spreadsheet,
    Config.activeJobsSheet,
    Config.doneJobsSheet
  );
  
  var tasks = [];
  for(job in Config.tooLongRunning) {
    _.extend(tasks, Tracker.getTooLongRunningTasks(job, Config.tooLongRunning[job]));
  }
  
  if(tasks.length > 0) {
    var body = "Hello, admin!\n\n".
    body = "Anmec Watchdog would like to inform you that there are " + tasks.length + " tasks that are being run too long\n\n";
    
    Logger.log(tasks.toSource());
    
    tasks.forEach(function(task) {
      body = body + task.join(" ") + "\n";
    });
    
    Utils.sendBulkMail(Config.adminEmails, "Anmec watchdog: Too long running tasks", body);
  }
}

function werentLaunchedRecently() {
  Tracker.init(
    Config.spreadsheet,
    Config.activeJobsSheet,
    Config.doneJobsSheet
  );
  
  var unlaunchedTasks = [];
  for(job in Config.werentLaunchedRecently) {
    var tasks = Tracker.getTasksThatWereLaunchedRecently(job, Config.werentLaunchedRecently[job]);
    
    Logger.log(tasks);
    
    if(tasks.length === 0) {
      unlaunchedTasks.push(job);
    }
  }  
  
  if(unlaunchedTasks.length > 0) {
    var body = "Hello, admin!\n\n".
    body = "Anmec Watchdog would like to inform you that there are " + unlaunchedTasks.length + " tasks that haven't been launched at the proper time\n\n";
    
    body += "The following jobs are:\n\n" + unlaunchedTasks.join("\n");
    
    Utils.sendBulkMail(Config.adminEmails, "Anmec watchdog: The tasks that weren't launched recently", body);    
  }

}
