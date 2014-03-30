"use strict";

angular.module('search').controller('searchVkPostsController', function($scope, $rootScope, $location, vkApi, anmecApi, $routeParams, utils) {
    /*
     * Retrieves list of groups
     */
    $scope.findHandler = function(data, status) {
        $scope.searchIsInProgress = false;

        $scope.posts = $scope.posts || [];
        data.posts = data.posts || [];
        data.posts.forEach(function(post) {
          try {
            post.attachments = JSON.parse(post.attachments);
          } catch(e) {
            console.log(e);
          }
        });
        data.posts.forEach(function(post) {
          $scope.posts.push(post);
        });

        var keyword;

        try {
          keyword = $scope.query.keyword.value;
        } catch(e) { }

        highlight($scope.posts, keyword)

        $scope.count = data.count;
        $scope.page = data.page;
        $scope.maxPage = data.maxPage;
    };

    /*
     * Highlight substring that is looking for
     */
    function highlight(posts, keyword) {
        posts = posts || [];

        posts.forEach(function(post) {
            post.text = utils.highlight(post.text, keyword);
        });
    }


    /*
     * Find posts
     */
    $scope.findPosts = function() {
        anmecApi.findPosts($scope.query).
            success($scope.findHandler).
            error($scope.findHandler);
        $scope.searchIsInProgress = true;
    }

    $scope.search = function(offset) {
        if(offset !== undefined) {
          $scope.query.offset = offset;
        }

        $location.search('query', JSON.stringify($scope.query));
        $scope.findPosts();
    };

    $scope.query = {};
    $scope.query.offset = 0;

    if($routeParams.query) {
        try {
            $scope.query = JSON.parse($routeParams.query);
            $scope.findGroups();
        } catch(e) {
        }
    }

    $scope.$watch('query.orderBy', function(newValue) {
        if(newValue) {
            $scope.search();
        }
    }, true);


    $scope.loadMore = function() {
      if($scope.posts === undefined || $scope.posts.length === 0) {
        return;
      }
      $scope.query.offset += ($scope.resultsPerPage + 1);
      $scope.search();
    };
});
