"use strict";

angular.module('global').service('utils', function($rootScope, $q) {
    return  {
        highlight: function(text, substring, minLength) {
            substring = substring || '';
            minLength = minLength || 4;

            if(!substring.length || substring.length === 0) {
                return text;
            }

            var keywords = substring.
                        split(/[!.?,;:'"-\\ ]/).
                        map(function(keyword) { 
                            // Remove whitespaces
                            return keyword.replace(/^\s+|\s+$/g, ''); 
                        }).filter(function(keyword) {
                            return keyword.length >= minLength;
                        });

            if(keywords.length === 0) {
                return text;
            }

            var tokens = [];
            keywords.forEach(function(keyword) {
                for(var tokenLength = keyword.length; tokenLength >= minLength; tokenLength--) {
                    tokens.push(keyword.slice(0, tokenLength));
                }
            });

            var regexp = new RegExp("(" + tokens.join("|") + ")", "ig");

            return (text || '').replace(regexp, function(match, contents, offset, s) {
                return "<span class='match'>" + contents + "</span>";
                console.log(arguments);
            });
        },

        fakePromise: function(data, fail) {
            var deferred = $q.defer();
            
            if(!fail) {
                deferred.resolve(data);
            } else {
                deferred.reject(data);
            }

            return deferred.promise;
        },

        rejectedPromise: function(data) {
            return this.fakePromise(data, true);
        },

        /*
         * zfill(123, 5) --> '00123'
         */
        zfill: function(integer, length) {
           var str = integer.toString();

           if (str.length < length) {
               var strLength = str.length;
               for(var i = 0; i < length - strLength; i++) str = '0' + str
           }

           return str; 
        },

        throttle: function(requestsPerSecond, func) {
            var queue = [];
            var intervalId = null;
            var delay = 1000.0 / requestsPerSecond;

            function intervalWorker() {
                // from the beginning of queue
                var task = queue.shift();

                if(!task) {
                    clearInterval(intervalId);
                    intervalId = null;
                } else {
                    task.deferred.resolve(task.args);
                    $rootScope.$apply();
                }
            }

            return function() {
                var isThrottled = intervalId != null;
                var deferred = $q.defer();
                
                // to the end of queue
                queue.push({
                    deferred: deferred, 
                    args: Array.prototype.slice.call(arguments)
                });

                if(!isThrottled) {
                    intervalId = setInterval(intervalWorker, delay);
                }

                return deferred.promise.then(function(args) {
                    return func.apply(null, args);
                });
            }
        }
    }
});
