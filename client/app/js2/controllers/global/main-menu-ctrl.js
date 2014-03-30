"use strict";

angular.module('global').controller('mainMenuController', function($scope, $rootScope, $location, account) {
    $scope.account = null;

    $rootScope.$watch('account', function(newValue) {
        $scope.account = newValue;
    }, true);

    account.summary().then(function(response) {
        $rootScope.account = $scope.account = response.data;
    });
});
 
