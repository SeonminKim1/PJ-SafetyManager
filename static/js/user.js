// Join
function join() {
    // 입력값 변수에 저장 후 보냄
    let id = $('#id').val()
    let name = $('#name').val()
    let company = $('#company').val()
    let pwd = $('#pwd').val()
    $.ajax({
        type: "POST",
        url: "/user/api/join",
        data: {'id_give': id, 'name_give': name, 'company_give': company, 'pwd_give': pwd},
        success: function (response) {
            alert(response["msg"])
            window.location.href = '/user/login'
        }
    })
}


// Login
function login() {
    let id = $('#id').val()
    let pwd = $('#pwd').val()

    $.ajax({
        type: "POST",
        url: "/user/api/login",
        data: {'id_give': id, 'pwd_give': pwd},
        success: function (response) {
            alert(response['msg'])
            if (response['result'] == 'success') {
                // 토큰이 정상적으로 발급되면, 'token' 토큰을 받아 쿠키에 저장
                // 토큰 최상위 경로에 쿠키 저장
                document.cookie = 'mytoken=' + response['token'] + ';path=/'
                window.location.replace('/')
            } else {
                // 로그인 실패 시
                window.location.replace('/user/login')
            }
        }
    })
}


// Logout
function logout() {
    $.ajax({
        type: "GET",
        url: '/user/logout',
        data: {},
        success: function (response) {
            $.removeCookie('mytoken');
            window.location.href = '/user/login'
        }
    })
}

