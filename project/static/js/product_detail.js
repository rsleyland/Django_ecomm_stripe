
//Ajax - add item to cart
$("#add").click(function(){
    let prodName = JSON.parse(document.getElementById('prod_name').textContent);   // another way to get custom named variables from jinja
    let url = JSON.parse(document.getElementById('new_url').textContent);
    let is_auth = JSON.parse(document.getElementById('auth_bool').textContent);
    if (is_auth == false){
        window.location.href = "../../accounts/login"
    }
    $.ajax({
        url: url,
        type: 'get',
        data: {
            // prod_name: $("input[name=product_name]").val(),  //another way to get product name from hidden input field
            prod_name: prodName
        },
        success: function(response) {
            $("#success-message").show().text("Added "+ prodName +" to cart");
            // Timeout to hide success message after pop up message from adding to cart
            setTimeout(function(){
                $("#success-message").fadeOut(500);
            }, 2000);
        }
    });
});

