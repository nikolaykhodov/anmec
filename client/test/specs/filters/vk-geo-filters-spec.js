"use strict";
describe('Global Vk Geo Module Filters', function() {
    beforeEach(module('global'));
    beforeEach(module('config'));

    it('vkGeoCountry', inject(function($filter) {
        var format = $filter('vkGeoCountry');

        expect(format).not.toEqual(null);
        expect(format(1)).toEqual('Россия');
        expect(format(2)).toEqual('Украина');
        expect(format(25)).toEqual('Ангола');
    }));

    it('vkGeoCity', inject(function($filter) {
        var format = $filter('vkGeoCity');

        expect(format).not.toEqual(null);

        expect(format(1)).toEqual("Москва");
        expect(format(610)).toEqual("Пинск");
        expect(format(1710648)).toEqual("Туркменабад");
        expect(format(627)).toEqual("Симферополь");
    }));
});
 
