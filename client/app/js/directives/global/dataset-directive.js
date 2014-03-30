"use strict";

angular.module('global').directive('dataset', function() {
    function getByKey(dict, path) {
        var parts = path.split('.');

        var value = dict;
        for(var i = 0; i < parts.length; i++) {
            value = value[parts[i]];
        }

        return value;
    }
    function sortDataset(dataset, key, order) {
        return dataset.sort(function(a, b) {
            return order * (getByKey(a, key) - getByKey(b, key));

        });
    }

    function isDatasetUpdatedInternally(state, key) {
        if(state.isUpdating[key]) {
            state.isUpdating[key] = false;
            return true;
        }

        return false;
    }

    function preventCreatingShadows(state) {
        for(var key in state.isUpdating) {
            state.isUpdating[key] = true;
        }
    }


    return {
        restrict: 'A',

        compile: function(element, attrs, transclude) {
            var dataset = attrs.dataset;
            var key = attrs.datasetKey;
            var displayedEntries = parseInt(attrs.displayedEntries);

            var content = element[0].innerHTML;

            return function(scope, el, attrs) {
                if(typeof scope.$datasets != 'object') {
                    scope.$datasets = {};
                }

                if(!scope.$datasets[dataset]) {
                    scope.$datasets[dataset] = {
                        shadow: null,
                        currentKey: '',
                        // > 0 - in ascending order, < 0 - in desceding order
                        order: 1,
                        isUpdating: {}
                    };
                }
                scope.$datasets[dataset].isUpdating[key] = false;

                scope.$watch(dataset, function(newValue) {
                    var state = scope.$datasets[dataset];

                    if(isDatasetUpdatedInternally(state, key)) {
                        return;
                    }

                    if(newValue) {
                        // Copy array
                        state.shadow =  _.without(scope[dataset], []);
                    }
                });
                    
                el[0].onclick = function() {
                    var state = scope.$datasets[dataset];

                    if(state.currentKey == key) {
                        state.order *= -1;
                    } else {
                        state.currentKey = key;
                        state.order = 1;
                    }

                    scope[dataset] = sortDataset(
                        state.shadow, 
                        state.currentKey, 
                        state.order
                    )
                    if(displayedEntries > 0) {
                        scope[dataset] = scope[dataset].slice(0, displayedEntries);
                    }

                    preventCreatingShadows(state);
                    scope.$apply();

                    angular.element('.dataset-arrow').remove();
                    el[0].innerHTML = content + '<i class="dataset-arrow icon-arrow-' + (scope.$datasets[dataset].order < 0 ? 'up' : 'down') + '"></i>';
                };
            }
        }
    };
});
