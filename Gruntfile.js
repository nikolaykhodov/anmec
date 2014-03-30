module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),


    bowerOrganiser: {
      options: {
        includeName: false
      },
      mapping: {
        js: 'client/app/lib/vendor-js',
        css: 'client/app/lib/vendor-css'
      }
    },

    concat: {
      options: {
        // define a string to put between each file in the concatenated output
        separator: ';'
      },
      'libs.js': {
        src: [
          'client/vendor/jquery/jquery.min.js',
          'client/vendor/isotope/jquery.isotope.min.js',
          'client/vendor/bootstrap/docs/assets/js/bootstrap.min.js',
          'client/vendor/jqplot/jquery.jqplot.min.js',
          'client/vendor/jqplot/plugins/jqplot.pieRenderer.min.js',
          'client/vendor/jqplot/plugins/jqplot.enhancedLegendRenderer.min.js',
          'client/vendor/jqplot/plugins/jqplot.dateAxisRenderer.min.js',
          'client/vendor/jqplot/plugins/jqplot.highlighter.min.js',

          'client/vendor/bootstrap-select/bootstap-select.min.js',
          'client/vendor/bootstrap-datepicker/bootstap-datepicker.min.js',
          'client/vendor/bootstrap-timepicker/bootstap-timepicker.min.js',

          'client/vendor/angular/angular.min.js',
          'client/vendor/angular-sanitize/angular-sanitize.min.js',
          'client/vendor/angular-strap/dist/angular-strap.min.js',
          'client/vendor/underscore/underscore-min.js',
          'client/vendor/ngInfiniteScroll/ng-infinite-scroll.js'
        ],
        dest: 'client/app/lib/libs.js'
      },

      'libs.css': {
        src: [
          'client/app/lib/vendor-css/**/*.css',
          'client/vendor/bootstrap-select/bootstrap-select.min.js'
        ],
        dest: 'client/app/lib/libs.css'
      }
    },

    clean: {
      'vendor-js': "client/app/lib/vendor-js/",
      'vendor-css': "client/app/lib/vendor-css/"
    }
  });

  grunt.loadNpmTasks('grunt-bower-organiser');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-clean');

  // Default task(s).
  grunt.registerTask('default', ['bowerOrganiser', 'concat', 'clean']);

};
