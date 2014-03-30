'use strict';

angular.module('global', ['config', '$strap.directives', 'infinite-scroll']);

angular.module('vk', ['config', 'global']);
angular.module('fb', ['config', 'global']);
angular.module('twitter', ['config', 'global']);

angular.module('feed', ['ngSanitize', 'config', 'global', 'vk']);
angular.module('search', ['ngSanitize', 'config', 'global', 'vk']);
angular.module('home', ['config']);

angular.module('adminFinder', ['feed', 'search', 'global', 'home', 'config']).
    config(['$routeProvider', '$locationProvider', function($routeProvider, $location) {
        var invalidator = '?' + Math.random();

        $routeProvider.when('/home', {templateUrl: 'partials2/home/home.html', controller: "homeController"});
        $routeProvider.when('/prices', {templateUrl: 'partials2/home/prices.html', controller: "pricesController"});

        $routeProvider.when('/vk/search/groups', {templateUrl: 'partials/search/vk-groups.html' + invalidator, controller: "searchVkGroupsController", reloadOnSearch: false});
        $routeProvider.when('/vk/search/posts', {templateUrl: 'partials/search/vk-posts.html' + invalidator, controller: "searchVkPostsController", reloadOnSearch: false});
        $routeProvider.when('/vk/feed/wall', {templateUrl: 'partials/feed/vk-wall.html' + invalidator, controller: "feedVkWallController", reloadOnSearch: false});
        $routeProvider.when('/vk/stat', {templateUrl: 'partials/vk/stat.html' + invalidator, controller: 'vkStatController'});

        $routeProvider.when('/login', {templateUrl: 'partials2/home/login.html', controller: "loginController"});
        $routeProvider.when('/logout', {templateUrl: 'partials2/home/logout.html', controller: "logoutController"});
        $routeProvider.when('/account', {templateUrl: 'partials2/home/account.html', controller: "accountController"});
        $routeProvider.when('/unauthenticated', {templateUrl: 'partials2/global/unauthenticated.html' + invalidator, controller: "unauthenticatedController"});
        $routeProvider.otherwise({redirectTo: '/home'});

        if(document.location.href.indexOf('www.anmec.me') >= 0) {
            $location.html5Mode(true);
        }
    }]);
