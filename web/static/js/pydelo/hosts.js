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
    get_hosts(function (data) {
        check_return(data);
        var data = data["data"];
        $.each(data["hosts"], function (i, n) {
            var tr = $("<tr></tr>");
            tr.append($("<td></td>").text(n["name"]));
            tr.append($("<td></td>").text(n["ssh_host"]));
            //tr.append($("<td></td>").append($("<a href=\"/hosts/"+n["id"].toString()+"\">detail</a>&nbsp;&nbsp;<a href=\"group\">group</a>")));
            tr.append($("<td></td>").append($("<a href=\"/hosts/" + n["id"].toString() + "\">detail</a>")));
            $("table tbody").append(tr);
        });
        $(".pagination").empty();
        for (var i = 1, offset = 0; offset < data["count"]; i++) {
            $(".pagination").append($("<li><a href=\"/hosts?offset=" + offset + "&limit=" + vars["limit"] + "\">" + i.toString() + "</a></li>"));
            offset += vars["limit"];
        }
    }, vars["offset"], vars["limit"]);
});
