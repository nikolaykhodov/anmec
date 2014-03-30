"use strict";

angular.module('global').controller('unauthenticatedController', function($location, $routeParams, $scope) {
  console.log($routeParams);
  $scope.next = $routeParams.next;
});
