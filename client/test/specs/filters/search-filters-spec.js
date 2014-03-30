"use strict";
describe('Search Module Filters', function() {
    beforeEach(module('global'));
    beforeEach(module('config'));
    beforeEach(module('search'));

    it('should be defined', inject(function($filter) {
        var groupType = $filter('groupType');
        var groupPrivacy = $filter('groupPrivacy');

        expect(groupPrivacy).not.toEqual(null);
        expect(groupType).not.toEqual(null);
    }));
});

