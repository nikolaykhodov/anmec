"use strict";
describe('Utils', function() {
    beforeEach(module('global'));
    beforeEach(module('config'));

    it('throttle: it should allow to call given function certain 3 times a second', inject(function($q, $rootScope, utils) {
        jasmine.Clock.useMock();

        var count = 0;
        var N = 30;
        var requestPerSecond = 6;

        var f = utils.throttle(requestPerSecond, 
            function() {
                var deferred = $q.defer();
                deferred.resolve([{"1": 1}, 0.1]);
                return deferred.promise;
            }
        );

        runs(function() {
            for(var i = 0; i < N; i++) {
                f().then(function(l) {
                    expect(l).toEqual([{"1": 1}, 0.1]);
                    count++;
                });
            }

            jasmine.Clock.tick(N / requestPerSecond * 1000 + 1);
            $rootScope.$digest();
        });

        waitsFor(function() {
            return count >= N;
        }, 500);

        runs(function() {
            expect(count).toEqual(N);
        });
    }));
    
    it('throttle: it should support promise chaining', inject(function($q, $rootScope, utils) {
        jasmine.Clock.useMock();

        var count = 0;
        var N = 30;
        var requestPerSecond = 6;

        function promise1() {
          var deferred = $q.defer();
          deferred.resolve([{"1": 1}, 0.1]);
          return deferred.promise;
        }

        var f = utils.throttle(requestPerSecond, 
            function() {
              return promise1().then(function() {
                var deferred = $q.defer();
                deferred.resolve([{"1": 1}, 0.1]);
                return deferred.promise;
              });
            }
        );

        runs(function() {
            for(var i = 0; i < N; i++) {
                f().then(function(l) {
                    expect(l).toEqual([{"1": 1}, 0.1]);
                    count++;
                });
            }

            jasmine.Clock.tick(N / requestPerSecond * 1000 + 1);
            $rootScope.$digest();
        });

        waitsFor(function() {
            return count >= N;
        }, 500);

        runs(function() {
            expect(count).toEqual(N);
        });
    }));


   it('zfill: should prepend the appropriate number of zero', inject(function(utils) {
       expect(utils.zfill(123, 6)).toEqual('000123');
       expect(utils.zfill(123, 5)).toEqual('00123');
       expect(utils.zfill(123, 3)).toEqual('123');
       expect(utils.zfill(123, 2)).toEqual('123');
       expect(utils.zfill(123, -1)).toEqual('123');
   }));
});
 
