import json

from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from crudProject import dictfetchall, file_upload, page_util


def where_check(img, kw):
    if img == 'true' or kw is not None and kw != 'None':
        where = " WHERE "
    else:
        where = ""
    return where


def and_check(img, kw):
    if img == 'true' and kw is not None and kw != 'None':
        many = " AND "
    else:
        many = ""
    return many


def img_check(img):
    if img == 'true':
        img = "img IS NOT NULL"
    else:
        img = ""
    return img


def kw_check(kw):
    if kw is None or kw == 'None':
        kw = ""
    else:
        kw = "title LIKE '%" + kw + "%'"
    return kw


def date_desc(request):
    img = request.GET.get('img')
    kw = request.GET.get('kw')

    try:
        cursor = connection.cursor()
        str_sql = "SELECT title, writer, date, restaurant_name, id FROM board" \
                  + where_check(img, kw) + img_check(img) + and_check(img, kw) + kw_check(kw) + " ORDER BY date DESC"
        print("sql문: " + str_sql)
        cursor.execute(str_sql)
        post_list = dictfetchall(cursor)
        connection.commit()
        connection.close()

        page = request.GET.get('page')
        lists = page_util(post_list, page)

        post_list = Paginator(post_list, 10).get_page(page)

    except:
        connection.rollback()
        print("Failed postList")

    data = {
        'results': lists,
    }
    context = {
        'post_list': post_list,
        'data': data,
        'order_by': 'date_desc',
        'page': page,
        'img': img,
        'kw': kw
    }

    return render(request, 'crudapp/home.html', context=context)


def date_asc(request):
    img = request.GET.get('img')
    kw = request.GET.get('kw')
    try:
        cursor = connection.cursor()
        str_sql = "SELECT title, writer, date, restaurant_name, id FROM board" \
                  + where_check(img, kw) + img_check(img) + and_check(img, kw) + kw_check(kw) + " ORDER BY date ASC"
        print("sql문: " + str_sql)
        cursor.execute(str_sql)
        post_list = dictfetchall(cursor)

        connection.commit()
        connection.close()

        page = request.GET.get('page')
        lists = page_util(post_list, page)

        post_list = Paginator(post_list, 10).get_page(page)

    except:
        connection.rollback()

    data = {
        'results': lists,
    }
    context = {
        'post_list': post_list,
        'data': data,
        'order_by': 'date_asc',
        'page': page,
        'img': img,
        'kw': kw
    }

    return render(request, 'crudapp/home.html', context=context)


def title_asc(request):
    img = request.GET.get('img')
    kw = request.GET.get('kw')
    try:
        cursor = connection.cursor()
        str_sql = "SELECT title, writer, date, restaurant_name, id FROM board" \
                  + where_check(img, kw) + img_check(img) + and_check(img, kw) + kw_check(kw) + " ORDER BY title ASC"
        print("sql문: " + str_sql)
        cursor.execute(str_sql)
        post_list = dictfetchall(cursor)

        connection.commit()
        connection.close()

        page = request.GET.get('page')
        lists = page_util(post_list, page)

        post_list = Paginator(post_list, 10).get_page(page)

    except:
        connection.rollback()
        print("Failed postList")
        print(str_sql)

    data = {
        'results': lists,
    }
    context = {
        'post_list': post_list,
        'data': data,
        'order_by': 'title_asc',
        'page': page,
        'img': img,
        'kw': kw
    }

    return render(request, 'crudapp/home.html', context=context)


def writer_asc(request):
    img = request.GET.get('img')
    kw = request.GET.get('kw')
    try:
        cursor = connection.cursor()
        str_sql = "SELECT title, writer, date, restaurant_name, id FROM board" \
                  + where_check(img, kw) + img_check(img) + and_check(img, kw) + kw_check(kw) + " ORDER BY writer ASC"
        print("sql문: " + str_sql)
        cursor.execute(str_sql)
        post_list = dictfetchall(cursor)

        connection.commit()
        connection.close()

        page = request.GET.get('page')
        lists = page_util(post_list, page)

        post_list = Paginator(post_list, 10).get_page(page)

    except:
        connection.rollback()
        print("Failed postList")

    data = {
        'results': lists,
    }
    context = {
        'post_list': post_list,
        'data': data,
        'order_by': 'writer_asc',
        'page': page,
        'img': img,
        'kw': kw
    }

    return render(request, 'crudapp/home.html', context=context)


def read(request):
    try:
        id_str = request.GET['id']
        order_by = request.GET.get('order')
        page = request.GET.get('page')
        img = request.GET.get('img')

        cursor = connection.cursor()
        str_sql = "SELECT * FROM board WHERE id = %s"
        cursor.execute(str_sql, (id_str,))
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        post = {'id': datas[0][0],
                'writer': datas[0][1],
                'date': datas[0][2],
                'title': datas[0][3],
                'content': datas[0][4],
                'img': datas[0][5],
                'restaurant_name': datas[0][6]
                }

    except:
        connection.rollback()
        print("Failed read")

    return render(request, 'crudapp/read.html', context={'post': post, 'order_by': order_by, 'page': page, 'img': img})


def delete(request):
    if request.method == 'POST':
        post_id = request.POST.get('id')
        user_id = str(request.session.get('user_id'))

        try:
            cursor = connection.cursor()
            str_sql = "SELECT user_id FROM board WHERE id = %s"
            cursor.execute(str_sql, (post_id,))
            datas = cursor.fetchall()
            match_user = str(datas[0][0])
            str_sql = "DELETE FROM board WHERE id = %s AND user_id = %s"
            result = cursor.execute(str_sql, (post_id, user_id))
            result_str = str(result)
            connection.commit()
            connection.close()
        except:
            connection.rollback()
            print("Failed delete")

        context = {
            'result': result_str,
            'user_id': user_id,
            'match_user': match_user
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


def create(request):
    if request.method == 'GET':
        return render(request, 'crudapp/create.html')

    elif request.method == 'POST':
        writer = request.POST.get('writer')
        title = request.POST.get('title')
        restaurant_name = request.POST.get('restaurant_name')
        content = request.POST.get('content')
        img_path = None

        if 'img' in request.FILES:
            img_url = request.FILES['img']
            img_path = file_upload(img_url, '/img')

        if request.session.get('user_id') is None:
            try:
                cursor = connection.cursor()
                str_sql = "INSERT INTO board (writer, title, content, restaurant_name) VALUES(%s, %s, %s, %s)"
                result = cursor.execute(str_sql, (writer, title, content, restaurant_name))
                result_str = str(result)
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_insert_id = str(cursor.fetchall()[0][0])
                str_sql = "SELECT user_id from board WHERE id = %s"
                cursor.execute(str_sql, (last_insert_id,))
                request.session['user_id'] = cursor.fetchall()[0][0]
                connection.commit()
                connection.close()
            except:
                connection.rollback()
                print("Failed create (user_id is None)")

        else:
            try:
                cursor = connection.cursor()
                user_id = str(request.session.get('user_id'))
                str_sql = "INSERT INTO board (writer, title, content, restaurant_name, user_id, img) " \
                          "VALUES(%s, %s, %s, %s, %s, %s)"
                result = cursor.execute(str_sql, (writer, title, content, restaurant_name, user_id, img_path))
                result_str = str(result)
                cursor.execute("SELECT LAST_INSERT_ID()")
                last_insert_id = str(cursor.fetchall()[0][0])
                connection.commit()
                connection.close()
            except:
                connection.rollback()
                print("Failed create (user_id is Not None)")
                print(last_insert_id)

        context = {
            'id': last_insert_id,
            'result': result_str
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


def update(request):
    if request.method == 'GET':
        id_str = request.GET['id']
        order_by = request.GET.get('order')
        page = request.GET.get('page')
        img = request.GET.get('img')

        try:
            cursor = connection.cursor()

            str_sql = "SELECT * FROM board WHERE id = %s"
            result = cursor.execute(str_sql, (id_str,))
            datas = cursor.fetchall()

            connection.commit()
            connection.close()

            post = {'id': datas[0][0],
                    'writer': datas[0][1],
                    'date': datas[0][2],
                    'title': datas[0][3],
                    'content': datas[0][4],
                    'img': datas[0][5],
                    'restaurant_name': datas[0][6]
                    }

        except:
            connection.rollback()
            print("Failed upload update page")

        context = {'post': post, 'order_by': order_by, 'page': page, 'img': img}
        return render(request, 'crudapp/update.html', context=context)

    elif request.method == "POST":

        post_id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        user_id = str(request.session.get('user_id'))

        try:
            cursor = connection.cursor()

            if 'img' in request.FILES:
                img_url = request.FILES['img']
                img_path = file_upload(img_url, '/img')
                str_sql = \
                    "UPDATE board SET date = CURDATE(), title = %s, content = %s, img = %s " \
                    "WHERE id = %s AND user_id = %s"
                result = cursor.execute(str_sql, (title, content, img_path, post_id, user_id))

            else:
                str_sql = \
                    "UPDATE board SET date = CURDATE(), title = %s, content = %s " \
                    "WHERE id = %s AND user_id = %s"
                result = cursor.execute(str_sql, (title, content, post_id, user_id))

            result_str = str(result)
            str_sql = "SELECT user_id FROM board WHERE id = %s"
            cursor.execute(str_sql, (post_id,))
            datas = cursor.fetchall()
            match_user = str(datas[0][0])
            connection.commit()
            connection.close()

        except:
            connection.rollback()
            print("Failed update")

        context = {
            'id': post_id,
            'result': result_str,
            'user_id': user_id,
            'match_user': match_user
        }

        return HttpResponse(json.dumps(context), content_type="application/json")

