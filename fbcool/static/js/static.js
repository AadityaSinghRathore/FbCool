
$(document).ready(function () {
        
          $(".create-post-model-popup").on("click", function (e) {
            e.preventDefault();
            
            url = $(this).data('url');
            $.get(url, function(response) {
                $(".admin-model-popup").html(response);

            });
        });

        $(document).on("click", ".delete-post-model-popup", function(e) {
        
            e.preventDefault();
            
            url = $(this).data('url');
            $.get(url, function(response) {
                $(".admin-model-popup").html(response);

            });
        });
        
        
        $("#adminModelPopup").on("submit", ".create_post_form", function() {
                       
            var form = $(this);
            var data1 = new FormData($(".create_post_form").get(0));
            $.ajax({
                url: form.attr("action"),
                data: data1, 
                type: form.attr("method"),
                dataType: 'json',
                contentType: false,
                processData: false,
                success: function(data) {
                    if (data.form_is_valid) {
                        
                        $('#createpost').modal('hide')
                        $(".container1").html(data.html_admin_user_list);
                    } else {
                        $(".create_post_form").html(data.html_form);
                    }
                }
            });
            return false;
        });
  
        
        $(document).on("click", ".comment-post-model-popup", function(e) {

            e.preventDefault(); 
            url = $(this).data('url');
            var post_id=$(this).data('id');

            $.get(url, function(response) {
                console.log('response',response)
                $(".admin-model-popup").html(response);
            });
           
        });

        $("#adminModelPopup").on("submit", ".comment_post_form", function() {
            var form = $(this);
            var data1 = new FormData($(".comment_post_form").get(0));

            $.ajax({
                url: $(this).attr("action"),
                data: data1,  //form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                contentType: false,
                processData: false,
                success: function(data) {
                    if (data.form_is_valid) {
                        debugger
                        $('#createpost').modal('hide')
                        $(".container1").html(data.html_admin_user_list);
                    } else {

                        $(".comment_post_form").html(data.html_form);
                    }
                }
            });
            return false;
        });

     /*   
        $(document).on("click", ".comment-post-model-popup", function(e) {
            debugger
            e.preventDefault();
            url = $(this).data('url');
            $.get(url, function(response) {
                $(".admin-model-popup").html($.parseHTML(response));
            });
        });*/
        
        
}) 