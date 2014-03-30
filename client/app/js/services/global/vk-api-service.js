"use strict";

angular.module('global').service('vkApi', function($rootScope, $http, $q, config, vkGeo, utils) {
    return {
        /*
         * Arbitrary request to VK API
         */
        request: function(method, params, access_token) {

            var vk_token;
            try {
              vk_token = $rootScope.account.vk_token;
            } catch(e) { }

            access_token = access_token || vk_token || '';

            var new_params = _.extend(params, {
                access_token: access_token,
                callback: "JSON_CALLBACK"
            });

            return $http.jsonp(
                'https://api.vk.com/method/' + method,
                {
                    params: new_params
                }
            ).then(function(response) {
                var answer = response.data;
                if(answer.error) {
                    return $q.reject('API Error: ' + answer.error.error_msg);
                } else {
                    return answer.response;
                }
            });
        },
        /*
         * Return list of countries
         */
        countries: function() {
            return vkGeo.countries();
        },

        /*
         * Return promise
         *
         * @param {number} country Country id
         */
        cities: function(country, access_token) {

            var cities = vkGeo.cities(country);
            if(cities) {
                return utils.fakePromise(cities);
            } else {
                access_token = access_token || config.ACCESS_TOKEN;
                return this.request('places.getCities', { country: country }, access_token).
                    then(function(cities) {
                        vkGeo.allCities()[country] = cities;
                        return cities;
                    });
            }
        },

        getId: function(url) {
            var self = this;
            var deferred = $q.defer();

            try {
                // Ссылка на стену или страницу владельца стены
                var matches = /^https?:\/\/vk\.com\/(id|public|event|club)(\d+)/.exec(url);

                if(!matches) {
                  throw new Error('');
                }

                var possible_id = parseInt(matches[2]);
                if(matches[1] !== 'id') {
                  possible_id = -possible_id;
                }
            } catch(e) {
                try {
                    // Ссылка на профиль с пользовательским именем
                    possible_id = /^(https?:\/\/vk\.com\/)?([a-z0-9_\.]+)/.exec(url)[2];
                } catch(e) {
                    return utils.rejectedPromise("Не подходящий формат ссылки для определения номера пользователя");
                }
            }
    
            var resolvedAsUser = false;
            var numericId = typeof(possible_id) === 'number';
            var is_group;

            if(numericId === true) {
              is_group = possible_id < 0;

              var method = is_group ? 'groups.getById' : 'users.get';
              var params = is_group ? {gid: -possible_id} : {uids: possible_id};

              self.request(
                method, params
              ).then(function(response) {
                deferred.resolve({
                  mid: possible_id,
                  name: is_group ? response[0].name : response[0].first_name + ' ' + response[0].last_name
                });
              }, function(reason) {
                var apiError = reason.indexOf('API Error') == 0;
                var msg = apiError ? "Эта ссылка ведет в никуда :("  : "Произошел технический сбой: " + reason;
              });
            }
            // Может быть пользователь
            self.request(
                'users.get', {uids: possible_id}
            ).then(function(users) {
                resolvedAsUser = true;

                deferred.resolve({
                    mid: users[0].uid, 
                    name: users[0].first_name + ' ' + users[0].last_name
                });
            },
            function(reason) {
                var apiError = reason.indexOf('API Error') == 0;
                if(apiError) {
                    // А может быть группа, паблик или событие
                    return self.request('groups.getById', {gid: possible_id});
                } else {
                    deferred.reject("Произошел технический сбой: " + reason);
                }
            }).then(function(groups) {
                if(resolvedAsUser) {
                    return;
                }
                deferred.resolve({
                    mid: -groups[0].gid, 
                    name: groups[0].name
                });
            }, function(reason) {
                var apiError = reason.indexOf('API Error') == 0;
                var msg = apiError ? "Эта ссылка ведет в никуда :("  : "Произошел технический сбой: " + reason;
                deferred.reject(msg);
            });    

            return deferred.promise;
        },

        resolveMids: function(mids) {

            var groups = _.filter(mids, function(mid) {
                return mid < 0;
            });
            var groups = _.map(groups, function(gid) {
                return Math.abs(gid);
            });

            var users = _.filter(mids, function(mid) {
                return mid > 0;
            });


            var deferred = $q.defer();

            var promises = [];

            if(users.length > 0) {
                promises.push(this.request('users.get', {uids: users.join(',')}));
            } else {
                promises.push(utils.fakePromise([]));
            }

            if(groups.length > 0) {
                promises.push(this.request('groups.getById', {gids: groups.join(',')}));
            } else {
                promises.push(utils.fakePromise([]));
            }

            $q.all(promises).then(function(responses) {
                var users = responses[0];
                var groups = responses[1];

                var entities = [];

                users.forEach(function(user) {
                    user.name = user.first_name + ' ' + user.last_name;
                    user.mid = user.uid;

                    entities.push(user);
                });

                groups.forEach(function(group) {
                    group.mid = -group.gid;
                    entities.push(group);
                });

                deferred.resolve(entities);
            }, function(reason) {
                deferred.reject(reason);
            });
            
            return deferred.promise;
        },

        getStats: function(gid, days) {

          function date2vkFormat(date) {
            var year = date.getFullYear();
            var month = date.getMonth();
            if (month < 10) { 
              month = "0" + (month + 1);
            }

            var day = date.getDate();
            if (day < 10) {
              day = "0" + day;
            }
            return year + '-' + month + '-' + day;
          }

          var to = new Date();
          var from = new Date(to.getTime() - days * 24 * 3600 * 1000);

          return this.request('stats.get', {
            gid: gid, 
            date_from: date2vkFormat(from),
            date_to: date2vkFormat(to)
          });
        },

        getLikeStats: function(gid, days) {
          var code = 
            'var groupId = '+ gid +';\n\
            var ofst = 0;\n\
            var _acl = 5;\n\
            var posts = API.wall.get({\n\
                owner_id: -groupId,\n\
                offset: ofst,\n\
                count: 100,\n\
                filter: "owner" \n\
            });\n\
            _acl = _acl - 1;\n\
            var count = posts[0];\n\
            var data = [[posts@.id, posts@.date, posts@.likes@.count, posts@.reposts@.count, posts@.comments@.count]];\n\
            ofst = ofst + 100;\n\
            while (_acl > 1 && ofst < count) {\n\
                var posts = API.wall.get({\n\
                    owner_id: -groupId,\n\
                    offset: ofst,\n\
                    count: 100,\n\
                    filter: "owner" \n\
                });\n\
                _acl = _acl - 1;\n\
                data = data + [[posts@.id, posts@.date, posts@.likes@.count, posts@.reposts@.count, posts@.comments@.count]];\n\
                ofst = ofst  + 100;\n\
            }\n\
            var result = {\n\
                count: count,\n\
                offset: ofst,\n\
                posts: data\n\
            };\n\
            return result;';

         return this.request('execute', {
            code: code
          });
        }
    };
});
