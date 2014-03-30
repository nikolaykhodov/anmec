"use strict";

angular.module('global').
filter('vkGeoCountry', function(vkGeo) {
    return function(country) {
        var entry = vkGeo.getCountryById(country);
        return entry ? entry.title : '';
    }
}).filter('vkGeoCity', function(vkGeo) {
    return function(city) {
        var entry = vkGeo.getCityById(city);
        return entry ? entry.title : '';
    }
});
