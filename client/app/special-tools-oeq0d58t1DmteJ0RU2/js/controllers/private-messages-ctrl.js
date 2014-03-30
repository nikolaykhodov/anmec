angular.module('specialTools').controller('privateMessagesController', function($rootScope, $scope, config, vkApi, $q, utils) {
  "use strict";
  console.log('/private-messages');

  $scope.vkAppId = config.VK_PRIV_MSG_APP_ID;

  /*
   * Return an array of numeric mids
   */
  function parseRecipients() {
    var deferred = $q.defer();
    var lines = ($scope.recipients || '').split('\n');
    var promises = [];

    lines.forEach(function(line) {
      promises.push(vkApi.getId(line.trim()));
    });

    $q.all(promises).then(function() {
      var responses = arguments[0] || [];
      var mids = [];

      responses.forEach(function(response) {
        if(response === undefined || typeof(response.mid) !== 'number') {
          return;
        }
        var mid = response.mid;
        if(mid > 0) {
          mids.push(mid);
        }
      });

      deferred.resolve(mids);
    });

    return deferred.promise;
  }

  function parseToken() {
    var token = $scope.accessToken || '';
    if(token.indexOf('https://') === 0) {
      var matches = token.match(/access_token=([a-z0-9]+)/);
      token = matches ? matches[1] : '';
    }

    console.log('token = ', token);
    return token;
  }

  function send(mids, message, token) {
    $scope.progressAll = mids.length;
    $scope.progressCurrent = 0;

    var request = utils.throttle(2, vkApi.request);
    var promises = [];
    mids.forEach(function(mid) {

      var promise = request(
        'messages.send', 
        {
          user_id: mid, 
          message: message,
          guid: Math.ceil(Math.random() * 1000000000)
        }, 
        token
      ).then(function(response) {
        $scope.progressCurrent++;
        return response;
      }, function() {
        $scope.progressCurrent++;
      });

      promises.push(promise);
    });

    return $q.all(promises);
  }

  $scope.send = function() {
    var token = parseToken();
    var message = $scope.message;

    parseRecipients().then(function(mids) {
      return send(mids, message, token);
    }).then(function(responses) {
      console.log(responses);
    });
  };
});
