
angular.module('search').directive('orderBy', function($compile) {
  "use strict";

  return {
    restrict: 'A',
    compile: function(element, attrs, transclude) {
      var content = element[0].innerHTML;
      var orderBy = attrs.orderBy;

      return function(scope, el, attrs) {
        /*
         * Return sort order ('' or '-')
         */
        function getOrder() {
          if(typeof scope.query != "object") {
            scope.query = {};
          }

          var matches = (scope.query.orderBy || '').match(/(-)?(.*)$/);
          var order;
          if(matches.length && matches.length >= 3 && matches[2] == orderBy) {
              order = matches[1] !== undefined ? matches[1] : '';
          } else {
              order = '';
          }

          return order;
        }

        function changeOrder() {
          var order = getOrder();
          order = order === '-' ? '' : '-';
          scope.$apply(scope.query.orderBy = order + orderBy);
        }

        function setContent() {
          var order = getOrder();
          el[0].innerHTML = content + '<i class="icon-arrow-' + (order == '' ? 'up' : 'down') + '"></i>';
        }

        el[0].onclick = function() {
          changeOrder();
          setContent();
        };
        scope.$watch('query.orderBy', function(newValue) {
          if(newValue && newValue.indexOf(orderBy) == -1) {
            el[0].innerHTML = content;
          }
        }, true);

        var currentOrderBy = scope.query ? scope.query.orderBy ? scope.query.orderBy : '' : '';
        if(currentOrderBy.indexOf(orderBy) >= 0) {
          setContent();
        }
      }
    }
  };
});

