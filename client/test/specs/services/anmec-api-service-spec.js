"use strict";
describe('Internal API', function() {
    beforeEach(module('search'));
    beforeEach(module('config'));

    it('should request /findGroups/', inject(function(config, anmecApi, $httpBackend) {
        $httpBackend.expectPOST(config.API_ROOT + '/findGroups/').respond({});
        anmecApi.findGroups({});
        $httpBackend.flush();
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    }));

    it('shoud parse admins in proper manner', inject(function(config, anmecApi, $httpBackend) {
        $httpBackend.expectPOST(
            config.API_ROOT + '/proxy/', 
            '{"2":"http://vk.com/al_page.php?act=a_get_contacts&al=1&oid=-2"}'
        ).respond({
            '2': GET_ADMIN_AL_PAGE_PHP_RESPONSE
        });

        var admins;
        runs(function() { 
            anmecApi.getAdmins([2]).then(function(data) {
                admins = data;
            });

            $httpBackend.flush();
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
        });

        waitsFor(function() {
            return admins !== undefined;
        });

        runs(function() {
            expect(admins['2'].length).toEqual(1);
            expect(admins['2'][0].screen_name).toEqual('4ever_free');
        });
    }));
});
