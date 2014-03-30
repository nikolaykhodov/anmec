angular.module('global').service("account", function($http, config) {
    return {
        summary: function() {
            return $http({
                method: 'GET',
                url: config.API_ROOT + '/account/summary/',
                withCredentials: true
            });
        },

        logout: function() {
            return $http({
                method: 'GET',
                url: config.API_ROOT + '/account/auth/logout/',
                withCredentials: true
            });
        }
    };
});
