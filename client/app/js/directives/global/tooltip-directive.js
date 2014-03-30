"use strict";
angular.module('global').directive('tooltip', function () {
    return {
        restrict:'A',
        link: function(scope, element, attrs)
        {
            if(!$(element).attr('title')) {
                $(element).attr('title',scope.$eval(attrs.tooltip))
            }
            $(element).tooltip({placement: 'top'});
        }
    }
});
