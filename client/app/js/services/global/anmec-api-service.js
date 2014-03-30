"use strict";

angular.module('search').service('anmecApi', function($http, $q, config) {
    function processParams(params) {
        var new_params = {};

        for(var key in params) {
            if(typeof params[key] != 'undefined') {
                new_params[key] = params[key];
            }
        }

        return new_params;
    }

    return {
        /*
         * Return promise
         */
        findGroups: function(params) {
            var new_params = {};

            return $http({
                method: 'POST',
                url: config.API_ROOT + '/findGroups/',
                data: params,
                withCredentials: true
            });
        },

        /*
         * Return promise
         */
        findPosts: function(params) {
            var new_params = {};

            return $http({
                method: 'POST',
                url: config.API_ROOT + '/findPosts/',
                data: params,
                withCredentials: true
            });
        },

        /*
         * Request for proxified request to vk.com
         *
         * @params {Array} groups List of gids
         * @return {Object} Promise
         */
        getAdmins: function(groups) {
            var urls = {};

            groups.forEach(function(id) {
                urls[id] = 'http://vk.com/al_page.php?act=a_get_contacts&al=1&oid=-' + (id);
            });

            return $http({
                method: 'POST',
                url: config.API_ROOT + '/proxy/',
                data: urls,
                withCredentials: true
            }).then(function(results) {
                var adminsRegExp = /<a href="[^"]+" onclick="return nav\.[^"]+">[^<]+<\/a>/g;
                var contactsRegExp = /<a href="\/([^"]+)" onclick="return nav\.[^"]+">([^<]+)<\/a>/;

                var retVal = {};

                for(var key in results.data) {
                    var admins = results.data[key].match(adminsRegExp);
                    retVal[key] = [];
                    if (!admins) {
                        continue;
                    }

                    admins.forEach(function(admin) {
                        var matches = admin.match(contactsRegExp);
                        retVal[key].push({
                            name: matches[2],
                            screen_name: matches[1]
                        });
                    });
                }

                return retVal;
            });
        }
    }
});
