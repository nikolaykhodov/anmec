var Config = {
  spreadsheet: 'https://docs.google.com/a/valt.me/spreadsheet/ccc?key=0Ak38hVaEdUXmdDlvcHdZbnRfNDlpNEVhUDdwZDhtVlE#gid=0',
  activeJobsSheet: 'Active Jobs',
  doneJobsSheet: 'Done Jobs',
  adminEmails: ['i@valt.me'],
  
  tooLongRunning: {
    'update:groups': 24,
    'update:analytics': 24,
    'update:posts': 3
  },
  
  werentLaunchedRecently: {
    'update:groups': 24*14,
    'update:analytics': 24*14,
    'update:posts': 24
  }
};
