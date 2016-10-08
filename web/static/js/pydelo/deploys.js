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
            }
            tr.append($("<td></td>").text(n["user"]["name"]));
            tr.append($("<td></td>").text(n["created_at"]));
            tr.append($("<td></td>").text(n["updated_at"]));

            var actionHtml = '';
            if (n[keyStatus] == 1) {
                actionHtml += "<a href=\"javascript:void(0)\" deploy_id=" + n["id"].toString() + " class=\"rollback\">回滚</a>&nbsp;";
            } else if (n[keyStatus] == 0) {
                actionHtml += "<a href=\"javascript:void(0)\" deploy_id=" + n["id"].toString() + " class=\"publish\">发布</a>&nbsp;";
            }
            if (n[keyStatus] != 99) {
                actionHtml += "<a href=\"javascript:void(0)\" deploy_id=" + n["id"].toString() + " class=\"cancel\">删除</a>&nbsp;";
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

$(document).ready(function () {
    $("table tbody").empty();
    var vars = getVars();
    get_deploys(getListCallback, vars["offset"], vars["limit"]);

    $("tbody").delegate(".rollback", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        update_deploy_by_id(
            deploy_id,
            {"action": "rollback"},
            function (data) {
                check_return(data, function () {
                    $('#totalMessage').text(data['msg']);
                });
            });
    }).delegate(".publish", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        update_deploy_by_id(
            deploy_id,
            {"action": "publish"},
            function (data) {
                check_return(data, function () {
                    $('#totalMessage').text(data['msg']);
                });
            });
    }).delegate(".cancel", "click", function () {
        var deploy_id = $(this).attr("deploy_id");
        update_deploy_by_id(
            deploy_id,
            {"action": "cancel"},
            function (data) {
                check_return(data, function () {
                    self.location.reload();
                });
            });
    });
});
