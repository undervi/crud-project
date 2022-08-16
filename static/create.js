// 글 작성 함수
$(document).on('click', '#create_btn', function(e) {
    console.log('글 작성 버튼 동작!')

    const newPost = new FormData();
    newPost.append('title', $('#title').val().trim());
    newPost.append('writer', $('#writer').val().trim());
    newPost.append('restaurant_name', $('#restaurant_name').val().trim());
    newPost.append('content', $('#content').val().trim());
    newPost.append('img', $("#img")[0].files[0]);

    if (newPost.get('title') === '') {
        alert('제목을 입력해주세요.');
        return;
    }
    if (newPost.get('writer') === '') {
        alert('작성자명을 입력해주세요.');
        return;
    }
    if (newPost.get('restaurant_name') === '') {
        alert('식당명을 입력해주세요.');
        return;
    }
    if (newPost.get('content') === '') {
        alert('글 내용을 입력해주세요.');
        return;
    }

    $.ajax({
        url: '/create/',
        type: 'post',
        headers: {
           'X-CSRFTOKEN' : '{{ csrf_token }}'
        },
        processData: false,
        contentType: false,
        data: newPost,
        async: true,
        success:function(json){
            console.log("data pass success", json)
            if (json['result'] == '1') {
                alert('글이 작성 되었습니다.')
                const url = '/read?id=' + json['id'] + '&order=date_desc&page=1';
                window.location.href = url;
            }
            else {
                alert('글 작성에 실패했습니다.')
            }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
        }
    })
});