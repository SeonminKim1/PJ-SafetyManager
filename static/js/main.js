window.onload = function(){
    // result_box, img_box, main_box, loading_box, score_box, btn_box
    $('.result_box').show()     // Safe, Warning Title Box
    $('.img_box').show()        // SafeMake Icon Image
    $('.main_box').hide()       // Upload, Predict Box - img
    $('.main_vid_box').hide()   // Upload, Predict Box - video
    $('.loading_box').hide()    // Loading Bar Box in Predict
    $('.score_box').show()      // Score Box
    $('.btn_box').show()        // Button Box (파일 선택, 업로드, 안전확인)
}

function change_area_css(is_img) {
    $('.img_box').hide()
    if (is_img){
        target = '.main_box'; // target은 img, vid 가 나타나는 box의 tag를 의미함.
        $('.main_vid_box').css({'display':'none'})
    }else{
        target = '.main_vid_box';
        $('.main_box').css({'display':'none'})
    }
    $(target).show()
    $(target).css({
        "display": "flex",
        "height": "500px",
        "width": "100%",
        "padding-bottom": "40px",
        "flex-direction": "row",
        "justify-content": "center",
        "align-items": "center"
    });
}

// Upload UX #1 - Preview (not upload)
function preview() {
    let file = $('#file')[0].files[0]
    let is_img = file.type.match(/image.*/)
    change_area_css(is_img) // div-box : hide and show
    if (is_img) {
        $('#upload_img').show(); $('#predict_img').hide(); 
        $('#upload_vid').hide(); $('#predict_vid').hide(); 
        $('#upload_img').css({
            'height': '400px',
            'width': '400px',
            'margin': '0px 10px 0px 10px'
        });
        $('#upload_img').attr("src", window.URL.createObjectURL(file));

    }else{ // video
        $('#upload_vid').show(); $('#predict_vid').hide();
        $('#upload_img').hide(); $('#predict_img').hide(); 
        $('#upload_vid').css({
            'height': '400px',
            'width': '400px',
            'margin': '0px 10px 0px 10px'
        });
        var video = document.getElementById('upload_vid');
        $("#upload_vid_src").attr("src", window.URL.createObjectURL(file))
        video.load();
    }
}

var upload_path = ''
// Upload UX #2 - Upload to Server
function posting() {
    let file = $('#file')[0].files[0] // 'if you view filename => file['name'] => test3.jpg
    let form_data = new FormData() // FormData 처럼 보내는 방식
    form_data.append("file", file) // console.log(file, typeof (file))
    // check images or video
    if (file.type.match(/image.*/)) {
        $.ajax({ // 비동기 방식
            type: "POST",
            url: "/main/api/img/upload",
            data: form_data,
            contentType: false,
            processData: false,
            success: function (response) {
                alert(response["msg"])
                upload_path = response['upload_path']
            }
        });
    } else {
        $.ajax({
            type: "POST",
            url: "/main/api/video/upload",
            data: form_data,
            contentType: false,
            processData: false,
            success: function (response) {
                alert(response["msg"])
                upload_path = response['upload_path']
            }
        });
    }
}

// Upload UX #3 - Detection in Server
function detecting() {
    let file = $('#file')[0].files[0] // 'if you view filename => file['name'] => test3.jpg
    $('.loading_box').show()
    // check images or video
    if (file.type.match(/image.*/)) {
        $('.main_box').hide()
        $.ajax({ // 비동기 방식
            type: "POST",
            url: "/detect/api/img/inference",
            data: {'upload_path':upload_path},
            success: function (response) {
                alert(response["msg"])
                $('.loading_box').hide()
                $('.main_box').show()
                $('#predict_img').show()
                predict_path = response["predict_path"]
                $('#predict_img').css({
                    'height': '400px',
                    'width': '400px',
                    'margin': '0px 10px 0px 10px'
                });
                $('#predict_img').attr("src", predict_path)

                results = response["results"]
                $('#helmet_value').text(results['helmet'])
                $('#head_value').text(results['head'])
                $('#score_value').text(results['score'])
                $('#isPass_value').text(results['isPass'])
                $('#result_label').text(results['isPass'])
            }
        });
    } else {
        $('.main_vid_box').hide()
        $.ajax({
            type: "POST",
            url: "/detect/api/video/inference",
            data: {'upload_path':upload_path},
            success: function (response) {
                alert(response["msg"])
                $('.loading_box').hide(); 
                $('.main_vid_box').show(); $('#upload_vid').show(); $('#predict_vid').show()
                let predict_src = response['predict_path']
                var video = document.getElementById('predict_vid');
                $("#predict_vid_src").attr("src", predict_src)
                video.load();

                $('#predict_vid').css({
                    'height': '400px',
                    'width': '400px',
                    'margin': '0px 10px 0px 10px'
                });

                results = response["results"]
                $('#helmet_value').text(results['helmet'])
                $('#head_value').text(results['head'])
                $('#score_value').text(results['score'])
                $('#isPass_value').text(results['isPass'])
            }
        })
    }
}
