describe('Feed VK Wall Controller', function() {

    beforeEach(module('feed'));
    beforeEach(module('config'));

    var scope, rootScope, controller, httpBackend, ctrl;

    beforeEach(inject(function($rootScope, $controller, $httpBackend) {
        scope = $rootScope.$new();
        rootScope = $rootScope;
        controller = $controller;
        httpBackend = $httpBackend;
        ctrl = controller('feedVkWallController', {$scope: scope, $routeParams: {query: '{+}'}, $rootScope: rootScope});
    }));

    it('should be initialized', function() {
        expect(ctrl).toBeDefined();

    });

    it('should remove one entity', function() {
        scope.entities = [{mid: 1}, {mid: 2}, {mid: 3}];
        scope.removeEntity(1);

        expect(scope.entities.length).toEqual(2);
    });
});

