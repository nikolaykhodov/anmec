'use strict';

angular.module('global', ['config']);
angular.module('specialTools', ['global', 'config']).
    config(['$routeProvider', '$locationProvider', function($routeProvider, $location) {
        var invalidator = '?' + Math.random();

        $routeProvider.when('/home', {templateUrl: 'special-tools-oeq0d58t1DmteJ0RU2/partials/home.html' + invalidator, controller: "homeController"});
        $routeProvider.when('/private-messages', {templateUrl: 'special-tools-oeq0d58t1DmteJ0RU2/partials/private-messages.html' + invalidator, controller: "privateMessagesController"});
        $routeProvider.otherwise({redirectTo: '/home'});

    }]);

