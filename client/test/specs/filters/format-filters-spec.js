"use strict";
describe('Search Module Filters', function() {
    beforeEach(module('global'));
    beforeEach(module('config'));

    it('formatNumber: should insert spaces after every 3 digits from right to left', inject(function($filter) {
        var format = $filter('formatNumber');

        expect(format).not.toEqual(null);

        expect(format(1)).toEqual('1');
        expect(format(11)).toEqual('11');
        expect(format(111)).toEqual('111');
        expect(format(2111)).toEqual('2 111');
        expect(format(22111)).toEqual('22 111');
        expect(format(222111)).toEqual('222 111');
        expect(format(3222111)).toEqual('3 222 111');
        expect(format(33222111)).toEqual('33 222 111');

        expect(format(1.0)).toEqual('1');
        expect(format(1.1)).toEqual('1.1');
        expect(format(1.12)).toEqual('1.12');
        expect(format(1.123)).toEqual('1.12');
    }));
});
 
