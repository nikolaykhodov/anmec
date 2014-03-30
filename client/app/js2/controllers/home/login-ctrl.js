"use strict";

angular.module('home').controller('loginController', function($scope, config, $routeParams) {
    console.log('/login');
    $scope.vkAppId = config.VK_APP_ID;
    $scope.vkAuthRedirectUri = config.VK_AUTH_REDIRECT_URI;
    $scope.developerMode = config.DEBUG;
    $scope.next = encodeURIComponent('#' + $routeParams.next || '');
    //console.log('$scope.next = ', $scope.next);
});
