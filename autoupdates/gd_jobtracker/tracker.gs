var Tracker = {
  init: function(spreadsheet, activeJobsSheet, doneJobsSheet) {
    this.spreadsheet = spreadsheet;
    this.activeJobsSheet = activeJobsSheet;
    this.doneJobsSheet = doneJobsSheet;
  },
  
  _findTask: function(sheet, taskId) {
    var range = sheet.getRange(
      2, //top
      1, //left
      9999,
      6 // job name, task id, started at, step, progress, finished at
    );
    
    var task =  _(range.getValues()).find(function(item) {
      return item[1] == taskId;
    });    
    
    return task;
  },
  
  _updateTask: function(sheet, taskId, data) {
    var range = sheet.getRange(
      2, //top
      1, //left
      1000,
      6 // job name, task id, started at, step, progress, finished at
    );
    var tasks = range.getValues();
    
    var finished = false;
    for(var j = 0, tasksLength = tasks.length; j < tasksLength && !finished; j++) {
      var task = tasks[j];
      
      if(task[1] === taskId) {
        for(var i = 0; i < Math.min(task.length, data.length); i++) {
          task[i] = data[i];
        }      
        
        finished = true;
      }
    }
    
    Utils.insertValues(sheet, tasks, {top: 2, left: 1});
  },
  
  _deleteTask: function(sheet, taskId) {
    var range = sheet.getRange(
      2, //top
      1, //left
      99,
      6 // job name, task id, started at, step, progress, finished at
    );
    
    var tasks = _(range.getValues()).filter(function(task) {
      return task[1] != taskId;
    });
    tasks.push(['', '', '', '', '', '']);
    
    range.setValues(tasks);
  },
  
  _addTask: function(sheet, taskId, data) {
    sheet.appendRow(data);
  },
  
  start: function(name, taskId) {
    if(typeof taskId != 'string' || taskId === '') {
      throw new Error("taskId should non-empty string");
    }
    var sheet = Utils.getSheetByName(this.spreadsheet, this.activeJobsSheet);
    var task = this._findTask(sheet, taskId);
    
    if(task !== undefined) {
      throw new Error("There is already task with id=" + taskId);
    }
    
    this._addTask(sheet, taskId, [name, taskId, new Date(), '<unknown>', '<unknown>', 'Not finished yet']);
  },
  
  step: function(taskId, message) {
    if(typeof taskId != 'string' || taskId === '') {
      throw new Error("taskId should non-empty string");
    }

    var sheet = Utils.getSheetByName(this.spreadsheet, this.activeJobsSheet);
    var data = this._findTask(sheet, taskId);
    
    if(data === undefined) {
      throw new Error("Unknown task with id=" + taskId);
    }
    
    Logger.log(data);
    
    // current step
    data[3] = message;
    
    this._updateTask(sheet, taskId, data);
  },
  
  progress: function(taskId, progress) {
    if(typeof taskId != 'string' || taskId === '') {
      throw new Error("taskId should non-empty string");
    }

    var sheet = Utils.getSheetByName(this.spreadsheet, this.activeJobsSheet);
    var data = this._findTask(sheet, taskId);
    
    if(data === undefined) {
      throw new Error("Unknown task with id=" + taskId);
    }
    
    // progress
    data[4] = progress;
    
    this._updateTask(sheet, taskId, data);
  },
  
  finish: function(taskId) {
    if(typeof taskId != 'string' || taskId === '') {
      throw new Error("taskId should non-empty string");
    }

    var activeJobs = Utils.getSheetByName(this.spreadsheet, this.activeJobsSheet);
    var doneJobs = Utils.getSheetByName(this.spreadsheet, this.doneJobsSheet);    
    var data = this._findTask(activeJobs, taskId);    

    if(data === undefined) {
      throw new Error("Unknown task with id=" + taskId);
    }
    
    // Step
    data[3] = "Finished"
    // finished at
    data[5] = new Date();
    
    this._deleteTask(activeJobs, taskId);
    this._addTask(doneJobs, taskId, data);
    
  },
  
  getTooLongRunningTasks: function(name, hours) {
    if(typeof name != 'string' || name === '') {
      throw new Error("taskId should non-empty string");
    }

    var activeJobs = Utils.getSheetByName(this.spreadsheet, this.activeJobsSheet);
    
    var range = activeJobs.getRange(
      2, //top
      1, //left
      9999,
      6 // job name, task id, started at, step, progress, finished at
    );
    
    var now = new Date();
    var tasks =  _(range.getValues()).filter(function(task) {
      // ID
      if(task[1] === '') {
        return false;
      }
      
      var startedAt = task[2];
      return now.getTime() - startedAt.getTime() > hours * 3600 * 1000;
    });    
    
    return tasks;
  },
  
  getTasksThatWereLaunchedRecently: function(name, lessThanHoursAgo) {
    if(typeof name != 'string' || name === '') {
      throw new Error("taskId should non-empty string");
    }

    var doneJobs = Utils.getSheetByName(this.spreadsheet, this.doneJobsSheet);
    
    var range = doneJobs.getRange(
      2, //top
      1, //left
      9999,
      6 // job name, task id, started at, step, progress, finished at
    );
    
    var now = new Date();
    var tasks =  _(range.getValues()).filter(function(task) {
      // ID
      if(task[1] === '') {
        return false;
      }
      
      var finishedAt = task[5];
      return now.getTime() - finishedAt.getTime() < lessThanHoursAgo * 3600 * 1000;
    });    
    
    return tasks;    
  }
};
