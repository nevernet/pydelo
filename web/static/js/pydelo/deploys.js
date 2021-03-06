function getVars() {
    vars = get_url_vars();
    if (typeof(vars["offset"]) == "undefined") {
        vars["offset"] = 0
    } else {
        vars["offset"] = parseInt(vars["offset"])
    }
    if (typeof(vars["limit"]) == "undefined") {
        vars["limit"] = 10
    } else {
        vars["limit"] = parseInt(vars["limit"])
    }
    return vars;
}

function getListCallback(data1) {
    check_return(data1, function () {
        var data = data1["data"];
        var keyStatus = "deploy_status";
        var isRollbackAdded = false;
        $.each(data["deploys"], function (i, n) {
            var tr = $("<tr></tr>");
            tr.append($("<td></td>").text(n["id"]));
            tr.append($("<td></td>").text(n["project"]["name"]));
            tr.append($("<td></td>").text(n["package_name"]));
            // tr.append($("<td></td>").text(n["branch"]));
            // tr.append($("<td></td>").text(n["version"]));
            if (n[keyStatus] == 1) {
                tr.append($("<td></td>").text("已发布"));
            } else if (n[keyStatus] == 0) {
                tr.append($("<td></td>").text("已上传"));
            } else if (n[keyStatus] == 99) {
                tr.append($("<td></td>").text("已取消"));
            } else if (n[keyStatus] == 2) {
                tr.append($("<td></td>").text("已回滚"));
            }
            tr.append($("<td></td>").text(n["user"]["name"]));
            tr.append($("<td></td>").text(n["created_at"]));
            tr.append($("<td></td>").text(n["updated_at"]));

            var actionHtml = '';
            cls = ' class="btn btn-primary btn-flat btn-sm" ';
            if (n[keyStatus] == 1 && i == 0) {
                cls = ' class="btn btn-danger btn-flat btn-sm rollback" ';
                actionHtml += "<a href=\"javascript:void(0)\" " +cls+" deploy_id=" + n["id"].toString() + ">回滚</a>&nbsp;";
                isRollbackAdded = true;
            } else if (n[keyStatus] == 0 && i == 0) {
                cls = ' class="btn btn-primary btn-flat btn-sm publish" ';
                actionHtml += "<a href=\"javascript:void(0)\" "+cls+" deploy_id=" + n["id"].toString() + ">发布</a>&nbsp;";
            } else if (n[keyStatus] == 2) {

            }

            if (n[keyStatus] != 99) {
                cls = ' class="btn btn-warning btn-flat btn-sm cancel" ';
                actionHtml += "<a href=\"javascript:void(0)\" "+cls+" deploy_id=" + n["id"].toString() + ">删除</a>&nbsp;";
            }

            tr.append($("<td></td>").append(actionHtml));

            $("table tbody").append(tr);
        });


        var vars = getVars();
        $(".pagination").empty();
        for (var i = 1, offset = 0; offset < data["count"]; i++) {
            $(".pagination").append($("<li><a href=\"/deploys?offset=" + offset + "&limit=" + vars["limit"] + "\">" + i.toString() + "</a></li>"));
            offset += vars["limit"];
        }
    });
}

function getList() {
    $("table tbody").empty();
    var vars = getVars();
    get_deploys(getListCallback, vars["offset"], vars["limit"]);
}

$(document).ready(function () {
    getList();

    $("tbody").delegate(".rollback", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        update_deploy_by_id(
            deploy_id,
            {"action": "rollback"},
            function (data) {
                check_return(data, function (data) {
                    $('#totalMessage').text(data['msg']);
                    getList();
                });
            });
    }).delegate(".publish", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        update_deploy_by_id(
            deploy_id,
            {"action": "publish"},
            function (data) {
                check_return(data, function (data) {
                    getList();
                    $('#totalMessage').text(data['msg']);
                });
            });
    }).delegate(".cancel", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        update_deploy_by_id(
            deploy_id,
            {"action": "cancel"},
            function (data) {
                check_return(data, function (data) {
                    getList();
                    // self.location.reload();
                });
            });
    });
});
