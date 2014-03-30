describe('Search Controller', function() {

    beforeEach(module('search'));
    beforeEach(module('config'));

    var scope, rootScope, controller, httpBackend;

    beforeEach(inject(function($rootScope, $controller, $httpBackend) {
        scope = $rootScope.$new();
        rootScope = $rootScope;
        controller = $controller;
        httpBackend = $httpBackend;
    }));

    afterEach(function() {
    });

    it('should handle incorrect "query" param properly', inject(function() {
        var ctrl = controller('searchVkGroupsController', {$scope: scope, $routeParams: {query: '{+}'}, $rootScope: rootScope});

        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
        expect(ctrl).toBeDefined();
        expect(scope.query).toEqual({});
    }));

    it('should request /findGroups/ once', inject(function(config) {
        httpBackend.expectPOST(config.API_ROOT + '/findGroups/').respond({});
        var ctrl = controller('searchVkGroupsController', {$scope: scope, $routeParams: {query: '{"page":1}'}, $rootScope: rootScope});

        httpBackend.flush();
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    }));
});
