function clearFields() {
    data = document.querySelectorAll('.inp')
    data.forEach(element => {
        element.value = ''
    });
}


function toggleBlockIcon(block, icon) {
    elm = document.getElementById(block).style
    if (elm.display == "none") {
        document.getElementById(block).style.display = "block"
        document.getElementById(icon).classList.remove('bi-caret-right');
        document.getElementById(icon).classList.add('bi-caret-down');
    }
    else {
        document.getElementById(block).style.display = "none"
        document.getElementById(icon).classList.remove('bi-caret-down');
        document.getElementById(icon).classList.add('bi-caret-right');
    }
}


//Ajax - update email
$("#update_email_btn").click(function(){
    let email = $("input[name=email_email]").val();   // another way to get custom named variables from jinja
    let pass = $("input[name=password_email]").val();
    $.ajax({
        url: '../accounts/update_email/',
        type: 'post',
        data: {
            email: email,
            pass: pass,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
            $("#update-email-message").show().text("Email updated");
            // Timeout to hide success message after pop up message from adding to cart
            setTimeout(function(){
                $("#update-email-message").fadeOut(500);
            }, 2000);
        },
        error: function(response) {
            $("#update-email-message").show().text("Incorrect Password");
            setTimeout(function(){
                $("#update-email-message").fadeOut(1000);
            }, 2000);
        }
    });
});

//Ajax - update password
$("#update_password_btn").click(function(){
    let pass = $("input[name=password]").val();
    let pass_new = $("input[name=new_password]").val();
    let pass_new_confirm = $("input[name=new_password_confirm]").val();

    if (pass.length == 0 || pass_new.length == 0 || pass_new_confirm.length == 0) {
        $("#update-password-message").show().text("Missing Fields");
            // Timeout to hide success message after pop up message from adding to cart
            setTimeout(function(){
                $("#update-password-message").fadeOut(500);
            }, 2000);
        return
    }


    $.ajax({
        url: '../accounts/update_password/',
        type: 'post',
        data: {
            pass: pass,
            pass_new: pass_new,
            pass_new_confirm: pass_new_confirm,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
            $("#update-password-message").show().text("Password updated");
            // Timeout to hide success message after pop up message from adding to cart
            setTimeout(function(){
                $("#update-password-message").fadeOut(500);
            }, 2000);
        },
        error: function(response) {
            if (response.responseJSON.message == 'failed') {
                $("#update-password-message").show().text("Incorrect Password");
                setTimeout(function(){
                    $("#update-password-message").fadeOut(1000);
                }, 2000);
            }
            else if (response.responseJSON.messagee == "not match") {
                $("#update-password-message").show().text("Password confirm does not match");
                setTimeout(function(){
                    $("#update-password-message").fadeOut(1000);
                }, 2000);
            }
            else if (response.responseJSON.message == "too short") {
                $("#update-password-message").show().text("New Password is less than 8 characters");
                setTimeout(function(){
                    $("#update-password-message").fadeOut(1000);
                }, 2000);
            }
        }
    });
});