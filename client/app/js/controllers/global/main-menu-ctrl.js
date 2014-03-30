"use strict";

angular.module('global').controller('mainMenuController', function($scope, $rootScope, $location) {
    $scope.menu = [
        //{url: '/prices', title: 'Цены'}
        {url: '/account', title: 'Аккаунт'},
        {url: '/login', title: 'Войти'}
    ];

    $scope.currentUrl = $location.path();
    $rootScope.$on('$routeChangeStart', function() {
        $scope.currentUrl = $location.path();
    });
});
 
