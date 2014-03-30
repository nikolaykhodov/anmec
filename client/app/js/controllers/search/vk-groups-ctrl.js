"use strict";

angular.module('search').controller('searchVkGroupsController', function($scope, $rootScope, $routeParams, utils, $location, vkApi, anmecApi) {
    /*
     * Retrieves list of cities for given country
     */
    $scope.citiesHandler = function(cities, status) {
        $scope.citiesLoading = false;
        $scope.cities = cities;
    };

    /*
     * Retrieves list of groups
     */
    $scope.findHandler = function(data, status) {
        $scope.searchIsInProgress = false;

        $scope.groups = $scope.groups || [];
        if(data.groups instanceof Array) {
          data.groups.forEach(function(group) {
            $scope.groups.push(group);
          });
        }

        var groupName = '';
        try{
            groupName = $scope.query.groupName.value;
        } catch(e) {}

        highlight($scope.groups, groupName);

        if(!$scope.$$phase) {
          $scope.$apply();
        }
    };

    /*
     * Highlight substring that is looking for
     */
    function highlight(groups, keywords) {
        groups = groups || [];
        groups.forEach(function(group) {
            group.name = utils.highlight(group.name, keywords);
        });
    }

    /*
     * Find groups
     */
    $scope.findGroups = function() {
        anmecApi.findGroups($scope.query).
            success($scope.findHandler).
            error($scope.findHandler);
        $scope.searchIsInProgress = true;
    }

    $scope.search = function(offset, loadMore) {
        if(offset !== undefined) {
          $scope.query.offset = offset;
          if(offset === 0) {
            $scope.groups = [];
          }
        }

        $scope.selectAllGroupsTicked = false;
        $location.search('query', JSON.stringify($scope.query));
        $scope.findGroups();
    };

    /*
     * Tick/untick checkbox for given td row
     */
    $scope.selectGroup = function(gid) {
        if(gid in $scope.selectedGroups) {
            $scope.selectedGroups[gid] = !$scope.selectedGroups[gid];
        } else {
            $scope.selectedGroups[gid] = true;
        }
    };

    $scope.selectAllGroups = function() {
        $scope.groups.forEach(function(group) {
            $scope.selectedGroups[group.gid] = $scope.selectAllGroupsTicked;
        });
    }

    $scope.clearSelectedGroups = function() {
        $scope.selectedGroups = {};
        $scope.selectAllGroupsTicked = false;
    };

    $scope.isGroupSelected = function(gid) {
        return gid in $scope.selectedGroups && $scope.selectedGroups[gid] === true;
    };

    $scope.selectedGroupIDs = function() {
        var gids = [];
        for(var gid in $scope.selectedGroups) {
            if($scope.selectedGroups[gid] === true) {
                gids.push(gid);
            }
        }

        return gids;
    }

    $scope.getAdmins = function() {
        $scope.searchIsInProgress = true;

        var groups = [];
        for(var gid in $scope.selectedGroups) {
            if($scope.selectedGroups[gid]){
                groups.push(gid);
            }
        }
        anmecApi.getAdmins(groups).then(function(admins) {
            $scope.searchIsInProgress = false;
            $scope.foundAdmins = admins;
        });
    };


    $scope.collapse = function(criterion) {
        $scope.uncollapsed[criterion] = !$scope.uncollapsed[criterion] || !$scope.empty($scope.query[criterion]);
    }
    $scope.empty = function(query) {
        query = query || {};

        var retVal = true;
        for(var key in query) {
            retVal = retVal && !query[key];
        }
        return retVal;
    }

    /*
     * Default values
     */
    $scope.selectedGroups = [];
    $scope.query = {};
    $scope.query.offset = 0;
    $scope.uncollapsed = {};
    $scope.resultsPerPage = 20;

    if($routeParams.query) {
        try {
            $scope.query = JSON.parse($routeParams.query);
            $scope.findGroups();
        } catch(e) {
        }
    }

    $scope.$watch('query.orderBy', function(newValue) {
        if(newValue) {
            $scope.search(0);
        }
    }, true);


    for(var criterion in $scope.query) {
        $scope.uncollapsed[criterion] = !$scope.empty($scope.query[criterion]);
    }

    $scope.countries = vkApi.countries();
    $scope.$watch('query.region.country', function(newValue) {
        if(newValue) {
            $scope.citiesLoading = true;
            vkApi.cities(newValue).
                then($scope.citiesHandler);
        }
    });


    $scope.loadMore = function() {
      if($scope.groups === undefined || $scope.groups.length === 0) {
        return;
      }

      var newOffset = $scope.offset + $scope.resultsPerPage + 1;
      $scope.search(newOffset);
    };
});
