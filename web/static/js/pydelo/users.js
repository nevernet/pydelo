$(document).ready(function () {
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
    $("table tbody").empty();

    get_users(function (data) {
        check_return(data, function (data1) {
            var data = data1["data"];
            $.each(data["users"], function (i, n) {
                var tr = $("<tr></tr>");
                tr.append($("<td></td>").text(n["id"]));
                tr.append($("<td></td>").text(n["name"]));
                var action = $("<td></td>");
                // action.append($("<a href=\"/users/" + n["id"].toString() + "/hosts\">服务器</a>"));
                // action.append($("<span class=\"cut-line\">&nbsp;¦&nbsp;</span>"));
                action.append($("<a href=\"/users/" + n["id"].toString() + "/projects\">项目</a>"));
                if (n["id"] != "1") {
                    action.append($("<span class=\"cut-line\">&nbsp;¦&nbsp;</span>"));
                    action.append($("<a class='delete' href=\"javascript:void(0);\" user_id=\"" + n["id"].toString() + "\">删除</a>"));
                }
                tr.append(action);
                $("table tbody").append(tr);
            });
            $(".pagination").empty();
            for (var i = 1, offset = 0; offset < data["count"]; i++) {
                $(".pagination").append($("<li><a href=\"/users?offset=" + offset + "&limit=" + vars["limit"] + "\">" + i.toString() + "</a></li>"));
                offset += vars["limit"];
            }
        });

    }, vars["offset"], vars["limit"]);

    $("tbody").delegate(".delete", "click", function () {
        var user_id = $(this).attr("user_id");
        delete_user_by_id(
            user_id,
            {},
            function (data) {
                check_return(data, function () {
                    self.location.reload();
                });
            });
    });
});
