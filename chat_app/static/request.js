$(function () {
    $(".cancel").click(function() {
        if (confirm("Are you sure you want to cancel this chat request?")) {
            $.ajax({
                type: "DELETE",
                url: "/request/" + $(this).val(),
            }).done(function(data) {
                if (xhr.status === 200) {
                    window.location.href="/";
                }
            })
        }
    });
});