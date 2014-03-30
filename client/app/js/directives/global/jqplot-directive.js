angular.module('global').directive('jqplot', function () {
  "use strict";
  return {
    restrict:'A',
    scope: {
      data: '=jqplotData',
      params: '=jqplotParams'
    },

    link: function(scope, element, attrs, controller) {

      if(scope.data) {
        $(element).jqplot(scope.data, scope.params);
      }

      scope.$watch('data', function(newValue) {
        if(!newValue) {
          return;
        }
        $(element).jqplot(scope.data, scope.params);
      });
      scope.$watch('params', function(newValue) {
        if(!newValue) {
          return;
        }
        $(element).jqplot(scope.data, scope.params);
      });    

      $.jqplot.config.enablePlugins = true;
    }
  }
});
