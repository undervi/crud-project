import json

from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from crudProject import dictfetchall, file_upload, page_util, where_check, and_check, img_check, kw_check, \
    topic_check, and2_check, my_post_check, date_check, and3_check, order_check, db_select


# HOME (POST LIST)
def home(request):
    order = request.GET.get('order')
    topic = request.GET.get('topic')
    kw = request.GET.get('kw')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    img = request.GET.get('img')
    my_post = request.GET.get('my_post')
    user_id = str(request.session.get('user_id'))
    page = request.GET.get('page')

    try:
        str_sql = "SELECT title, writer, date, restaurant_name, id FROM board" + \
                  where_check(img, kw, my_post, start_date, end_date) + img_check(img) + \
                  and_check(img, kw) + topic_check(topic) + kw_check(kw) + \
                  and2_check(img, kw, my_post) + my_post_check(my_post, user_id) + \
                  and3_check(img, kw, my_post, start_date, end_date) + date_check(start_date, end_date) + \
                  " ORDER BY " + order_check(order)
        print("sql문: " + str_sql)

        post_list = db_select(request, str_sql)
        lists = page_util(post_list, page)
        post_list = Paginator(post_list, 10).get_page(page)

    except:
        print("Failed postList")
        print("sql문: " + str_sql)
        print(post_list)
    data = {
        'results': lists,
    }
    context = {
        'post_list': post_list,
        'data': data,
        'order': order,
        'topic': topic,
        'kw': kw,
        'start_date': start_date,
        'end_date': end_date,
        'page': page,
        'img': img,
        'my_post': my_post
    }

    return render(request, 'crudapp/home.html', context=context)


# READ (POST DETAILS)
def read(request):
    try:
        id_str = request.GET['id']
        order = request.GET.get('order')
        topic = request.GET.get('topic')
        kw = request.GET.get('kw')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        page = request.GET.get('page')
        img = request.GET.get('img')
        my_post = request.GET.get('my_post')

        str_sql = "SELECT id, writer, date, title, content, img, restaurant_name FROM board WHERE id = %s"
        datas = db_select(request, str_sql, (id_str,))

        post = {'id': datas[0]['id'],
                'writer': datas[0]['writer'],
                'date': datas[0]['date'],
                'title': datas[0]['title'],
                'content': datas[0]['content'],
                'img': datas[0]['img'],
                'restaurant_name': datas[0]['restaurant_name']
                }
        context = {
            'post': post,
            'order': order,
            'topic': topic,
            'kw': kw,
            'start_date': start_date,
            'end_date': end_date,
            'page': page,
            'img': img,
            'my_post': my_post
        }

    except:
        connection.rollback()
        print("Failed read")

    return render(request, 'crudapp/read.html', context=context)


# DELETE
def delete(request):
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


# CREATE
class Create(View):
    def get(self, request):
        return render(request, 'crudapp/create.html')

    def post(self, request):
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

        context = {
            'id': last_insert_id,
            'result': result_str
        }

        return HttpResponse(json.dumps(context), content_type="application/json")


# UPDATE
class Update(View):
    def get(self, request):
        id_str = request.GET['id']
        order = request.GET.get('order')
        topic = request.GET.get('topic')
        kw = request.GET.get('kw')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        page = request.GET.get('page')
        img = request.GET.get('img')
        my_post = request.GET.get('my_post')

        try:
            cursor = connection.cursor()

            str_sql = "SELECT id, writer, date, title, content, img, restaurant_name FROM board WHERE id = %s"
            datas = db_select(request, str_sql, (id_str,))

            connection.commit()
            connection.close()

            post = {'id': datas[0]['id'],
                    'writer': datas[0]['writer'],
                    'date': datas[0]['date'],
                    'title': datas[0]['title'],
                    'content': datas[0]['content'],
                    'img': datas[0]['img'],
                    'restaurant_name': datas[0]['restaurant_name']
                    }
            context = {
                'post': post,
                'order': order,
                'topic': topic,
                'kw': kw,
                'start_date': start_date,
                'end_date': end_date,
                'page': page,
                'img': img,
                'my_post': my_post
            }

        except:
            connection.rollback()
            print("Failed upload update page")

        return render(request, 'crudapp/update.html', context=context)

    def post(self, request):
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

