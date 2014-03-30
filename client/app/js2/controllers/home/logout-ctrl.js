angular.module('home').controller('logoutController', function($rootScope, account, $location) {
    $rootScope.account = {};
    document.cookie="sl_hash=deleted";
    document.cookie="sl_expires_at=deleted";

    function onLoggedOut() {
        window.location.replace('');
    };

    account.logout().then(
        onLoggedOut,
        onLoggedOut
    );

});
