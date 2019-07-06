controllers.controller("addSys", ["$scope","loading","$modalInstance","msgModal","sysService","errorModal","$filter",function ( $scope,loading,$modalInstance,msgModal,sysService,errorModal,$filter) {
    $scope.title = "添加系统";
    $scope.args = {
        sys_name: "",
        sys_code: "",
        first_owner:"",
        is_control:""
    };
    $scope.userList = [{id:2, text: "dkdkd"}, {id:3, text: "ssssss"}];


    // multiple为true则是多选
    $scope.dbOption1 = {
        data: "userList",
        multiple: false,
        modelData: ""
    };


    // 复选框

    // 判断全选或者全不选
    $scope.check = function(){
        var box = document.getElementById("thead_ck");
        var suns = document.getElementsByName("sun_ck");
        if(box.checked == false){
            for (var i = 0; i < suns.length; i++) {
                   suns[i].checked = false;
                }
        }else {
           for (var i = 0; i < suns.length; i++) {
                   suns[i].checked = true;
                }
        }
    };

    // 每选择一个子节点检查 全选或全不选要不要打勾
    $scope.check_sum = function(){
        var box = document.getElementById("thead_ck");
        var suns = document.getElementsByName("sun_ck");
        var checked_host = [];
        for(var i = 0;i < suns.length; i++){
            if(suns[i].checked == true){
                checked_host.push(suns[i].value)
            }
        }
        if(suns.length == checked_host.length){
            box.checked = true
        }else {
            box.checked = false
        }
    };

    // 获取选择的复选框
     var suns = document.getElementsByName("sun_ck");
        var checked_ip = [];
        for(var i = 0;i < suns.length; i++){
            if(suns[i].checked == true){
                checked_ip.push(suns[i].value)
            }
        }

     // 时间控件
    var dateNow = new Date();
    var effective_time = dateNow.setDate(dateNow.getDate() + 365);
    // 把时间转成普通格式
    $scope.args.start_time = $filter('date')(effective_time, 'yyyy-MM-dd HH:mm')
    $scope.args.end_time = $filter('date')(effective_time, 'yyyy-MM-dd HH:mm')




    $scope.confirm = function () {


        if ($scope.args.sys_name == '') {
            msgModal.open("error", "请输入系统名！");
            return
        }

        //请求后台函数存入数据
        loading.open();
        sysService.add_sys({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "添加系统成功！！");
                $modalInstance.close(res.data);
             }
            else {
                errorModal.open(res.msg);
             }
         })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };


}]);