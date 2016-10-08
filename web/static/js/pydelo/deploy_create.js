function refresh_projects() {
    $("#projects").empty();
    get_projects(function (data) {
        check_return(data, function (data1) {
            var data = data1["data"];
            var projects = [];
            $.each(data["projects"], function () {
                projects.push({"text": this["name"], "value": this["id"]})
            });
            $("#projects").append($("<option></option>").text("请选择..."));
            append_option_to_select(projects, $("#projects"));
        });
    });
}

function refresh_hosts() {
    $("#hosts").empty();
    get_hosts(function (data) {
        check_return(data, function (data1) {
            var data = data1["data"];
            var hosts = [];
            $.each(data["hosts"], function () {
                hosts.push({"text": this["name"], "value": this["id"]})
            });
            $("#hosts").append($("<option></option>").text("请选择..."));
            append_option_to_select(hosts, $("#hosts"));
        });
    });
}

$(document).ready(function () {
    refresh_projects();
    // refresh_hosts();

    $("#submit").click(function () {
        var file = document.getElementById("package").files[0];
        if (file === undefined) {
            alert("请上传文件");
            return;
        }
        var data = new FormData();
        data.append('package', file);

        var projectId = $("#projects").val();
        projectId = isNaN(Number(projectId)) ? 0 : projectId;

        if (projectId < 1) {
            alert("请选择项目");
            return;
        }

        create_deploy(
            projectId,
            // $("#hosts").val(),
            0,
            data,
            function (data) {
                check_return(data, function (data) {
                    // var id = data["data"]["id"];
                    window.location.href = "/deploys";
                });
            }
        );
    });
});
