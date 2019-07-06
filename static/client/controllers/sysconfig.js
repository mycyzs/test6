controllers.controller("zhu_test", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal) {


      $scope.get_count_zhu = function () {
        loading.open();
        sysService.get_count_zhu({}, {}, function (res) {
            loading.close();
            if (res.result) {
                $scope.test_column = res.data

            }else {
                errorModal.open(res.message);
            }
        });
    };

      $scope.get_count_zhu();


    $scope.test_chart = {
        //柱状图标题
        title: {text: '服务器', enabled: false},
        //y轴
        yAxis: {
            title: {text: '数目'}, //y轴标题
            lineWidth: 2, //基线宽度1
            //tickPositions: [0, 1, 2, 3, 4]
        },
        //提示框位置和显示内容
        tooltip: {
            headerFormat: '<table\>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f} 台</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true,
            positioner: function () {
                return {x: 80, y: 80}
            }
        },
        data: "test_column"
    };


}]);


