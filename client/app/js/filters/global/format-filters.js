"use strict";

angular.module('global').filter('formatNumber', function() {
    return function(input) {
        if(typeof input != 'number') {
            return '—';
        }

        var parts = input.toString().split('.')
        var number = parts[0];
        var fractional = parts.length == 2 ? '.' + parts[1].slice(0,2) : '';

        var out = number.slice(-3);
        var number = number.slice(0, -3);
        while(number != '') {
            out = number.slice(-3) + ' ' + out;
            number = number.slice(0, -3);
        }

        return out + fractional;
    };
});
