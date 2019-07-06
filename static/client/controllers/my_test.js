controllers.controller("my_test", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", "$stateParams",function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal,$stateParams) {
    id = $stateParams.id
    alert(id)

}]);


