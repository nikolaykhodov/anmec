"use strict";

angular.module('global').
filter('formatUnixTime', function(utils) {
    return function(timestamp) {
        var date = new Date(timestamp * 1000);

        return utils.zfill(date.getDate(), 2) + '.' + 
               utils.zfill(date.getMonth() + 1, 2) + '.' + 
               date.getFullYear() + ' ' + 
               utils.zfill(date.getHours(), 2) + ':' + 
               utils.zfill(date.getMinutes(), 2)
    }
});
