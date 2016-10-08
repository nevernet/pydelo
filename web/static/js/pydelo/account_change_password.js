$(document).ready(function () {
    $("#submit").click(function () {
        account_change_password(
            {"password": $("#password").val()},
            function (data) {
                check_return(data, function () {
                    window.location.assign('/')
                });
            }
        );
    });
});
