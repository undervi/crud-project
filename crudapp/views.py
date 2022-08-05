from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from crudProject import dictfetchall


def post_list(request):
    try:
        cursor = connection.cursor()

        str_sql = "SELECT title, writer, date, restaurant_name, id FROM board ORDER BY id DESC"
        cursor.execute(str_sql)
        post_list = dictfetchall(cursor)

        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed postList")

    return render(request, 'crudapp/home.html', context={'post_list': post_list})


def read(request):
    id_str = request.GET['id'][:-1]

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
        print("Failed read")

    return render(request, 'crudapp/read.html', context={'post': post})


def delete(request):
    id_str = request.GET['id'][:-1]

    try:
        cursor = connection.cursor()

        str_sql = "DELETE FROM board WHERE id = %s"
        cursor.execute(str_sql, (id_str,))
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed delete")

    return redirect('/crud/')


def create(request):
    if request.method == 'GET':
        return render(request, 'crudapp/create.html')
    elif request.method == 'POST':
        writer = request.POST['writer']
        title = request.POST['title']
        restaurant_name = request.POST['restaurant_name']
        content = request.POST['content']

        try:
            cursor = connection.cursor()
            str_sql = "INSERT INTO board (writer, title, content, restaurant_name) VALUES(%s, %s, %s, %s)"
            cursor.execute(str_sql, (writer, title, content, restaurant_name))
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_insert_id = str(cursor.fetchall()[0][0])
            connection.commit()
            connection.close()

        except:
            connection.rollback()
            print("Failed create")

        return redirect('/crud/read?id=' + last_insert_id + '/')


def update(request):
    if request.method == 'GET':
        id_str = request.GET['id'][:-1]

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

        return render(request, 'crudapp/update.html', context={'post': post})

    elif request.method == "POST":
        post_id = request.POST['id']
        title = request.POST['title']
        content = request.POST['content']

        try:
            cursor = connection.cursor()
            strSql = "UPDATE board SET date = CURDATE(), title = %s, content = %s WHERE id = %s"
            cursor.execute(strSql, (title, content, post_id))
            connection.commit()
            connection.close()

        except:
            connection.rollback()
            print("Failed create")

        return redirect('/crud/read?id=' + post_id + '/')

