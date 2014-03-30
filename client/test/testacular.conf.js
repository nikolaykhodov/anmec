basePath = '../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'app/lib/libs.js',
  'test/lib/angular/angular-mocks.js',

  'app/js2/app.js',
  'app/js2/**/*.js',
  'app/js/**/*.js',

  'test/specs/**/*.js',
  'test/data/**/*.js'
];

autoWatch = true;

browsers = ['Chrome'];

junitReporter = {
  outputFile: 'test_out/unit.xml',
  suite: 'unit'
};
