angular.module('global').service('modal', function($q, $modal) {
  var holderScope = null;
  var modalPromise = null;

  // created to unify handling of modal dialogs

  function configure(scope, template) {
    template = template || 'partials/global/modal.html';

    holderScope = scope;
    modalPromise = $modal({
      template: template, // partial contains templates for all modals
                 persist: true, show: false,
                 backdrop: 'static', scope: scope,
                 backdropClick: false, keyboard: false
    });
  }

  function showModal(scope) {
    $q.when(modalPromise).then(function(modalEl) {

      // open modal dialog
      holderScope.scope = scope;
      modalEl.modal('show');
    });
  };

  function alertDialog(scope, title, message) {
    configure(scope);

    scope.modalTitle = title;
    scope.modalBody = message;

    showModal(scope);
  }

  return {
    configure: configure,
    showModal: showModal,
    alertDialog: alertDialog
  }
});
