"use strict";
describe('Vk API', function() {
    var rootScope;

    beforeEach(module('global'));
    beforeEach(module('config'));

    beforeEach(inject(function($rootScope) {
        rootScope = $rootScope;
    }));

    it('should return countries', inject(function(vkApi, $httpBackend) {
        expect(vkApi.countries()[1].title).toEqual('Австрия');
    }));

    it('should request /method/places.getCities and cache data if there are no cities for given country', inject(function(vkApi, $httpBackend) {
        $httpBackend.expectJSONP('https://api.vk.com/method/places.getCities?access_token=1&callback=JSON_CALLBACK&country=10').respond(VK_API_GET_CITIES);
        var cities = null;
        runs(function() {
            vkApi.cities(10, '1').then(function(_cities) {
                cities = _cities;
            });
            $httpBackend.flush();
        });

        waitsFor(function() {
            return cities != null;
        });

        runs(function() {
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
            expect(cities.length).toEqual(9);

            cities = null;
            vkApi.cities(10).then(function(_cities) {
                cities = _cities;
            });

            rootScope.$digest();

            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
            expect(cities.length).toEqual(9);
        });
 
    }));

    it('shouldn\'t request /method/places.getCities if there are cities for given country', inject(function(vkApi, $httpBackend) {
        var cities = null;

        vkApi.cities(1).then(function(_cities) {
            cities = _cities;
        });

        rootScope.$digest();

        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
        expect(cities.length).toBeGreaterThan(0);
    }));

    it('should request https://api.vk.com/method/users.get', inject(function(vkApi, $httpBackend) {
        $httpBackend.expectJSONP('https://api.vk.com/method/users.get?access_token=1&callback=JSON_CALLBACK&uids=durov').respond({
            response: [
                {uid: 1}
            ]
        });

        var uid;

        vkApi.request('users.get', {uids: 'durov'}, '1').then(function(response) {
            uid = response[0].uid;
        });

        $httpBackend.flush();
        rootScope.$digest();

        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
        expect(uid).toEqual(1);
    }));

    it('should handle API errors', inject(function(vkApi, $httpBackend) {
        $httpBackend.expectJSONP('https://api.vk.com/method/users.get?access_token=1&callback=JSON_CALLBACK&uids=durov').respond({
            error: {
                error_msg: 'Revoked token'
            }
        });
        var reason;

        vkApi.request('users.get', {uids: 'durov'}, '1').then(function(response) {
            uid = response[0].uid;
        }, function(_reason) {
            reason = _reason;
        });

        $httpBackend.flush();
        rootScope.$digest();

        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
        expect(reason).toEqual('API Error: Revoked token');
    }));
});
