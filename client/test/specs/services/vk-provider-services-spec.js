"use strict";
describe('VK Wall Provider', function() {
    var rootScope;

    beforeEach(module('global'));
    beforeEach(module('config'));
    beforeEach(module('feed'));

    beforeEach(inject(function($rootScope) {
        rootScope = $rootScope;
    }));

    it('should connect to VK API', inject(function(vkWallProv, $httpBackend) {
        $httpBackend.expectJSONP('https://api.vk.com/method/places.getCities?access_token=1&callback=JSON_CALLBACK&code=').respond({});

        vkWallProv.run([1,2,3,4]).then();

        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    }));
});
