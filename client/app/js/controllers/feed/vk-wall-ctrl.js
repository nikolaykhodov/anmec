"use strict";

angular.module('feed').controller('feedVkWallController', function($rootScope, $location, $scope, $routeParams, config, vkApi, utils, vkWallProv, $filter, modal) {
    function filterPosts(posts) {
        function onlyImagesFilter(post) {
            var attachments = _.filter(post.attachments, function(attach) {
                return attach.type === 'photo' || attach.type === 'posted_photo';
            });

            return attachments.length === post.attachments.length && attachments.length > 0;
        }

        function withMusicFilter(post) {
            return _.filter(post.attachments, function(attach) {
                return attach.type === 'audio';
            }).length > 0;
        }

        function withVideoFilter(post) {
            return _.filter(post.attachments, function(attach) {
                return attach.type === 'video';
            }).length > 0;
        }

        var likesMin = parseInt($scope.query.likesMin);
        var repostsMin = parseInt($scope.query.repostsMin);
        var repostLikeRatioMin = parseInt($scope.query.repostLikeRatioMin);

        var attachmentFilters = {
            onlyImages: onlyImagesFilter,
            withMusic: withMusicFilter,
            withVideo: withVideoFilter
        };
        var attachmentFilter = function() { return true; };


        if ($scope.query.attachmentFilter in attachmentFilters) {
            attachmentFilter = attachmentFilters[$scope.query.attachmentFilter];
        }
        
        var filteredPosts =  _.filter(posts, function(post) {
            if(!isNaN(likesMin)) {
                if(post.likes.count < likesMin) {
                    return false;
                }
            }

            if(!isNaN(repostsMin)) {
                if(post.reposts.count < repostsMin) {
                    return false;
                }
            }

            if(!isNaN(repostLikeRatioMin)) {
                if(post.repostLikeRatio < repostLikeRatioMin) {
                    return false
                }
            }

            return attachmentFilter(post);
        });


        return filteredPosts;
    }
    $scope.removeEntity = function(mid) {
        $scope.entities = _.filter($scope.entities, function(item) {
            return item.mid !== mid;
        });
    }
		
    $scope.addEntity = function() {
        $scope.addingNewEntity = true;
        function getIdHandler(entity) {
            $scope.entityLink = '';
            $scope.addingNewEntity = false;
            $scope.entities.push(entity);
        }

        function getIdFail(reason) {
            $scope.entityLink = '';
            $scope.addingNewEntity = false;
            modal.alertDialog($scope, 'Ошибка', reason);
        }

        vkApi.getId($scope.entityLink).then(
            getIdHandler,
            getIdFail
        );
    };

    $scope.analyze = function() {
        function analyzeFinished(posts) {

            $scope.searchIsInProgress = false;
            console.log(posts);
            $scope.posts = filterPosts(posts); 
        }

        function analyzeFailed(reason) {
            $scope.searchIsInProgress = false;
            modal.alertDialog($scope, 'Ошибка', reason);
        }

        $scope.searchIsInProgress = true;
        var days =  $scope.query.timeLength || 1;
        var now = Math.round((new Date()).getTime() / 1000);


        vkWallProv.run($scope.query.mids, now - 3600 * 24 * days).then(
            analyzeFinished,
            analyzeFailed
        );

        $location.search('query', JSON.stringify($scope.query));
    }

    $scope.entities = [];

    try {
        $scope.query = JSON.parse($routeParams.query);
    } catch(e) {
        $scope.query = {mids: []};
    }

    try {
        $scope.searchIsInProgress = true;
        vkApi.resolveMids($scope.query.mids).then(function(entities) {
            $scope.searchIsInProgress = false;
            $scope.entities = entities;
        }, function(reason) {
            $scope.searchIsInProgress = false;
            modal.alertDialog($scope, 'Ошибка', reason);
        });
    } catch(e) {
    }

    /*
     * Keep $scope.query.mids aligned with $scope.entities
     */
    $scope.$watch('entities', function(newValue) {
        if(!(newValue instanceof Array) || newValue.length == 0) {
            return;
        }

        $scope.query.mids = _(newValue).map(function(item) {
            return item.mid;
        });
        $location.search('query', JSON.stringify($scope.query));
    }, true);
});
