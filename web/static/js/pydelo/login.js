$(document).ready(function () {
    $("#submit").click(function () {
        login(
            {
                "username": $("#username").val(),
                "password": $("#password").val()
            },
            function (result) {
                check_return(result, function () {
                    var data = result["data"];
                    $.cookie('sign', data["sign"], {expires: 1, path: '/'});
                    window.location.assign('/')
                });
            }
        );
    });
});
