// result Modal Func
function result_modal_func(result_num) {
    console.log(result_num, typeof (result_num))
    document.querySelector('.modal_post_' + result_num).style.display = 'flex';
    document.querySelector('.modal_overlay_' + result_num).style.display = 'block';
    document.querySelector('.modal_overlay_' + result_num).style.top = window.pageYOffset + 'px';
    $('body').css("overflow", "hidden");
}

function result_modal_func_off(result_num) {
    console.log(result_num, typeof (result_num))
    document.querySelector('.modal_post_' + result_num).style.display = 'none';
    document.querySelector('.modal_overlay_' + result_num).style.display = 'none';
    document.querySelector('.modal_overlay_' + result_num).style.top = window.pageYOffset + 'px';
    $('body').css("overflow", "scroll");
}