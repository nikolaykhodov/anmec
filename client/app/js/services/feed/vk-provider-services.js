"use strict";

angular.module('feed').service('vkWallProv', function($q, vkApi) {
    return {
        /*
         * @param {Array} mids List of members IDs
         */
        run: function(mids, finalDate, onProgressChange) {
            function prepareCode(tasks) {
                var request = {};
                tasks.forEach(function(task) {
                    var entry = '#API.wall.get({"owner_id": {{ owner_id }}, "offset": {{ offset }}, "count": 100})#'.
                                    replace('{{ owner_id }}', task.mid).
                                    replace('{{ offset }}', task.offset);
                    request[task.mid + '_' + task.offset] = entry;
                });
                request = JSON.stringify(request);

                var code = request.replace(/#"/g, '').replace(/"#/g, '');
                // Replace JSON-escaped double quotes with double quotes
                var code = code.replace(/\\"/g, '"');

                console.log(code);

                return "return " + code + ";";
            }
            function postProcessPost(posts, finalDate) {
                posts = _.filter(posts, function(post) {
                    return post.date >= finalDate;
                });
                posts.forEach(function(post) {
                    if(post.likes.count == 0) {
                        post.repostLikeRatio = 0;
                    } else {
                        post.repostLikeRatio = Math.ceil(post.reposts.count * 100.0 / post.likes.count);
                    }
                });

                posts.sort(function(a,b) {
                    return a.date - b.date;
                });

                return posts;
            }

            function isWallLoaded(state, wall) {
                if(wall.length <= 1) {
                    return true;
                }

                var lastPost = wall[wall.length - 1];
                var itsDate = lastPost.date;

                return itsDate <= state.finalDate;
            }

            function requestHandler(state, walls, errReason) {
                state.runningRequests--;
                if(errReason) {
                    state.errors.push(errReason);
                    return step(state);
                }

                for(var key in walls) {
                    var matches = key.match(/^(-?\d+)_(\d+)$/);
                    if(!matches) {
                        state.errors.push('Неизвестный ключ ' + key);
                        continue;
                    }

                    var wall = walls[key] || [];
                    var mid = parseInt(matches[1]);
                    var offset = parseInt(matches[2]);

                    if(!isWallLoaded(state, wall)) {
                        state.queue.push({mid: mid, offset: offset + 100});
                    }

                    state.posts = _.union(state.posts, wall.slice(1));
                }

                step(state);
            }

            function step(state) {
                if(state.queue.length == 0 && state.runningRequests <= 0) {
                    var posts = postProcessPost(state.posts, state.finalDate);
                    return state.deferred.resolve(posts);
                }

                // 12 - magic constant: VK can't manage to handle more 12 groups per request
                var magic = 5;
                var tasks = state.queue.slice(0, magic);
                state.queue = state.queue.slice(magic);

                state.runningRequests++;

                var code = prepareCode(tasks);
                vkApi.request('execute', {code: code}).then(
                    function(walls) {
                        requestHandler(state, walls);
                    },

                    function(reason) {
                        requestHandler(state, null, reason);
                    }
                );


            }

            var state = {
                queue: [],
                posts: [],
                errors: [],
                deferred: $q.defer(),
                runningRequests: 0,
                finalDate: finalDate
            };

            mids.forEach(function(mid) {
                state.queue.push({mid: mid, offset: 0});
            });

            if(typeof finalDate != 'number') {
                state.deferred.reject('Должна быть задана дата');
            } else {
                step(state);
            }

            return state.deferred.promise;
        }
    }
});
