controllers.controller("test", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal) {
    $scope.get_count_obj = function () {
        loading.open();
        sysService.get_count_obj({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.data_list = res.data

            } else {
                errorModal.open(res.message);
            }
        });
    };
    $scope.get_count_obj();


    // 饼图
    $scope.mysql_pie = {
        data: "data_list",
        title: {text: 'MySQL版本占比', enabled: true},
        unit: "",
        size: "200px"
    };

}]);


