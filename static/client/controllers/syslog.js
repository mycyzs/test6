controllers.controller("syslog", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal) {


        $scope.dbReports = {
        data: "db_change",
        chart: {type: 'line'},
        title: {text: '每月数据库新增次数统计', enabled: true},
        xAxis: {
            categories: []
        },
        //提示框位置和显示内容
        tooltip: {
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f}</b></td></tr>',
            headerFormat: ""
        }
    };


         //获取mysql、oracle的数量
    $scope.get_count = function () {
        loading.open();
        sysService.get_count({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.db_change = res.data;
                $scope.dbReports.xAxis.categories = res.data.cat;

            }else {
                errorModal.open(res.message);
            }
        });
    };

    $scope.get_count();

}]);


