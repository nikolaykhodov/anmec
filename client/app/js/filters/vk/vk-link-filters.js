"use strict";

angular.module('vk').filter('vkLinkByMid', function() {
    return function(input) {
        var mid = parseInt(input);
        
        if(isNaN(mid)) {
            return '';
        }

        return 'https://vk.com/' + (mid > 0 ? 'id' + mid : 'club' + Math.abs(mid));
    }
}).filter('vkPostLink', function() {
    return function(post) {
        return 'http://vk.com/wall' + (!post.postId ? post.to_id + '_' + post.id : post.postId);
    }
});
