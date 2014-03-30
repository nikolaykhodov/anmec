angular.module('config', []).service('config', function() {
    var isLocalhost = document.location.href.match(/^http:\/\/localhost/) || document.location.href.match(/^http:\/\/www-debug\./);
    console.log('isLocalhost: ' + isLocalhost);
    return {
        DEBUG: isLocalhost,
        ACCESS_TOKEN: '',
        API_ROOT: !isLocalhost ? 'http://app.anmec.me' : 'http://app-debug.anmec.me:8000',

        VK_APP_ID: 2836076,
        VK_AUTH_REDIRECT_URI: (!isLocalhost ? 'http://app' : 'http://app-debug') + '.anmec.me' + (isLocalhost ? ':8000' : '') + '/account/auth/vk/'
    };
});

