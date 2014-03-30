angular.module('config', []).service('config', function() {
    var isLocalhost = document.location.href.match(/^http:\/\/localhost/) || document.location.href.match(/^http:\/\/www-debug\./);
    console.log('isLocalhost: ' + isLocalhost);
    return {
        VK_PRIV_MSG_APP_ID: 2819470
    };
});

