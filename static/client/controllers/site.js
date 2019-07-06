controllers.controller("site", ["$scope",
function ($scope) {
    $scope.menuList = [
        {
            displayName: "首页", iconClass: "fa fa-tachometer fa-lg", url: "#/"
        },
        {displayName: "用户管理", url: "#/test"},
        {displayName: "系统日志", url: "#/syslog"},
        {displayName: "日志管理", url: "#/zhu_test"},
        {displayName: "BODY", url: "#/body"},

    ];
    $scope.menuOption = {
        data: $scope.menuList
    };
}]);

