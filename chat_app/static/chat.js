$(function () {
    scrollToBottom();

    $("#chat-form textarea").keypress(function(e) {
        var $form = $(this).closest("form");
        var $textArea = $(this);
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == '13'){
            $form.submit();
            $textArea.val("");
            return false;
        }
    });

    $("#chat-form").submit(function(e) {
        e.preventDefault();
        var $form = $(this);
        var $textArea = $(this).find("textarea");

        if ($form.find("textarea").val() !== "") {
            $.ajax({
                type: "POST",
                url: $form.attr("action"),
                data: $form.serialize(),
                dataType: "html",
            }).done(function(data) {
                $("#messages").html(data);
                scrollToBottom();
                $textArea.val("").focus();
            });
        }
    });

    function scrollToBottom() {
        $("#messages").scrollTop($("#messages")[0].scrollHeight);
    }
});