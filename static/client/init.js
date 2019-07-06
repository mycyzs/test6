var app = angular.module("myApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService', 'cwLeftMenu', 'ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider", function ($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
    $urlRouterProvider.otherwise("/home");//默认展示页面
    $stateProvider.state('home', {
        url: "/home",
        controller: "home",
        templateUrl: static_url + "client/views/home.html"
    })
        .state('test', {
            url: "/test",
            controller: "test",
            templateUrl: static_url + "client/views/test.html"
        })
        .state('syslog', {
            url: "/syslog",
            controller: "syslog",
            templateUrl: static_url + "client/views/syslog.html"
        })

        .state('zhu_test', {
            url: "/zhu_test",
            controller: "zhu_test",
            templateUrl: static_url + "client/views/sysconfig.html"
        })

        .state('my_test', {
            url: "/my_test?id",
            controller: "my_test",
            templateUrl: static_url + "client/views/my_test.html"
        })

        .state('body', {
            url: "/body",
            controller: "body",
            templateUrl: static_url + "client/views/body.html"
        })


}]);
