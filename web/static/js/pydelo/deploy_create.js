function refresh_projects() {
    $("#projects").empty();
    get_projects(function (data) {
        check_return(data);
        var data = data["data"];
        var projects = [];
        $.each(data["projects"], function () {
            projects.push({"text": this["name"], "value": this["id"]})
        });
        $("#projects").append($("<option></option>").text("请选择..."));
        append_option_to_select(projects, $("#projects"));
    });
}

function refresh_hosts() {
    $("#hosts").empty();
    get_hosts(function (data) {
        check_return(data);
        var data = data["data"];
        var hosts = [];
        $.each(data["hosts"], function () {
            hosts.push({"text": this["name"], "value": this["id"]})
        });
        $("#hosts").append($("<option></option>").text("请选择..."));
        append_option_to_select(hosts, $("#hosts"));
    });
}

function refresh_branches() {
    $("#branches").empty();
    $("#commits").empty();
    get_branches_by_id($("#projects").val(), function (data) {
        check_return(data);
        var data = data["data"];
        var branches = [];
        $.each(data, function () {
            branches.push({"text": this, "value": this});
        });
        $("#branches").append($("<option></option>").text("请选择..."));
        append_option_to_select(branches, $("#branches"));
    });
}

function refresh_commits() {
    $("#commits").empty();
    get_commits_by_id($("#projects").val(), $("#branches option:selected").text(), function (data) {
        check_return(data);
        var data = data["data"];
        var commits = [];
        $.each(data, function () {
            commits.push({
                "value": this["abbreviated_commit"],
                "text": this["abbreviated_commit"] + " - " + this["author_name"] + " - " + this["subject"]
            });
        });
        $("#commits").append($("<option></option>").text("请选择..."));
        append_option_to_select(commits, $("#commits"));
    });
}

function refresh_tags() {
    $("#tags").empty();
    get_tags_by_id($("#projects").val(), function (data) {
        check_return(data);
        var data = data["data"];
        var tags = [];
        $.each(data, function () {
            tags.push({"value": this, "text": this});
        });
        $("#tags").append($("<option></option>").text("请选择..."));
        append_option_to_select(tags, $("#tags"));
    });
}

$(document).ready(function () {
    refresh_projects();
    refresh_hosts();
    // $("#projects").change(function(){
    //     var deploy_mode = $("input[name='deploy_mode']:checked").val();
    //     if(deploy_mode == 0){
    //         refresh_branches();
    //     }else{
    //         refresh_tags();
    //     }
    // });
    // $("#branches").change(refresh_commits);

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

        if(projectId < 1) {
            alert("请选择项目");
            return;
        }

        // return;
        // var deploy_mode = $("input[name='deploy_mode']:checked").val();
        // var data = {};
        // if (deploy_mode == 0) {
        //     data = {
        //         "mode": 0,
        //         "branch": $("#branches").val(),
        //         "commit": $("#commits").val()
        //     };
        // } else {
        //     data = {
        //         "mode": 1,
        //         "tag": $("#tags").val()
        //     };
        // }
        // alert("running");
        // console.log(data);
        create_deploy(
            projectId,
            // $("#hosts").val(),
            0,
            data,
            function (data) {
                check_return(data);
                var id = data["data"]["id"];
                window.location.href = "/deploys";
                // window.location.assign('/deploys/' + id.toString() + '/progress')
            }
        );
    });


    // $("input[name='deploy_mode']").click(function () {
    //     var deploy_mode = $("input[name='deploy_mode']:checked").val();
    //     if (deploy_mode == 0) {
    //         $(".deploy_branch_mode").show();
    //         $(".deploy_tag_mode").hide();
    //         refresh_branches();
    //     } else {
    //         $(".deploy_branch_mode").hide();
    //         $(".deploy_tag_mode").show();
    //         refresh_tags();
    //     }
    // });
});
