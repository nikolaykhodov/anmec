"use strict";

angular.module('search').filter('groupType', function() {
    return function(input) {
        var types = ['', 'Группа', 'Встреча', 'Паблик'];

        return types[input];
    };
}).filter('groupPrivacy', function() {
    return function(input) {
        var types = ['Открытая', 'Закрытая', 'Частная'];
        return types[input];
    }
}).filter("gidsToQuery", function() {
    return function(gids) {
        var mids;
        if(typeof gids == 'number') {
            mids = [gids];
        } else {
            mids = angular.copy(gids);
        }

        mids = _.map(mids, function(gid) {
            return -gid;
        });

        return encodeURIComponent(JSON.stringify({mids: mids}));
    }
});
