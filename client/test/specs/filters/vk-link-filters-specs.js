"use strict";
describe('Vk Link Filters', function() {
    beforeEach(module('global'));
    beforeEach(module('config'));
    beforeEach(module('vk'));

    it('vkGeoCountry', inject(function($filter) {
        var format = $filter('vkLinkByMid');

        expect(format).not.toEqual(null);
        expect(format(1)).toEqual('Россия');
        expect(format(2)).toEqual('Украина');
        expect(format(25)).toEqual('Ангола');
    }));
});
 
