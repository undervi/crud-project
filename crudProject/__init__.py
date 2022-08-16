import datetime
import os.path

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection

import pymysql
from django.http import HttpResponse

pymysql.install_as_MySQLdb()


def db_select(request, str_sql, params=None):
    try:
        cursor = connection.cursor()
        if params is None:
            cursor.execute(str_sql)
        elif params is not None:
            cursor.execute(str_sql, params)
        results = dictfetchall(cursor)
        connection.close()
        return results
    except Exception as e:
        connection.rollback()
        return HttpResponse(e.message)


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# 파일 업로드 관련 함수 1
def file_upload(file, path):
    f_name = file.name  # 파일명
    file_name = f_name.split('.')
    n_file_name, n_file_ext = os.path.splitext(file.name)
    # db_path = handle_uploaded_file(file, file_name[0], file_name[1], path)    # 파일, 파일명, 파일확장자, 패스
    db_path = handle_uploaded_file(file, n_file_name, n_file_ext.strip("."), path)  # 파일, 파일명, 파일확장자, 패스
    return db_path


# 파일 업로드 관련 함수 2
def handle_uploaded_file(f, f_name, fext, path):
    date_path = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_name = settings.MEDIA_ROOT + path + '/' + f_name + date_path + "." + fext   # 실 저장 위치
    db_path = 'static' + path + '/' + f_name + date_path + "." + fext   # DB 저장 위치

    destination = open(new_name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return db_path


# 페이징 함수
def page_util(lists, page):
    row_per_page = 10   # 한 페이지에 노출될 목록 수
    page_window = 5     # 화면에 표시될 페이지 개수 (예 1~5/6~10/11~15 ...)
    page = page         # 아마도 현재 페이지
    paginator = Paginator(lists, row_per_page)
    total_page_cnt = paginator.num_pages
    try:
        req_list = paginator.page(page)
    except PageNotAnInteger:    # page에 int가 아닌 값이 들어오면
        page = 1
        req_list = paginator.page(page)
    except EmptyPage:   # 페이지가 범위를 벗어나면 (없는 페이지)
        page = total_page_cnt
        req_list = paginator.page(page)

    page = int(page)
    page_window = int(page_window)
    start_page_num = 1 + int((page - 1) / page_window) * page_window   # page는 int인 점 유의 / 현재 page가 1~5면 1, 6~10이면 6, 11~15면 11 ...
    end_page_num = start_page_num + page_window - 1
    if total_page_cnt < end_page_num:   # end_page_num이 총 페이지 수보다 클 경우
        end_page_num = total_page_cnt   # end_page_num은 총 페이지 수 (12페이지까지 있을 경우는 11~15가 아닌 11~12 표시)

    bottom_pages = range(int(start_page_num), int(end_page_num + 1))    # range(MIN, MAX) => MIN <= x < MAX
    before_window = start_page_num - 1  # 이전 페이지 (<): 현재 start_page_num의 바로 전 페이지로 감! 6~10일 경우 5로!
    next_window = end_page_num + 1  # 다음 페이지 (>): 현재 end_page_num의 바로 다음 페이지로 감! 6~10일 경우 11로!

    return {
        'paginator': paginator,
        'req_list': req_list,
        'page': page,
        # 'end_page_num': page_window,
        'bottom_pages': bottom_pages,
        'total_page_cnt': total_page_cnt,
        'start_page_num': start_page_num,
        'end_page_num': end_page_num,
        'before_window': before_window,
        'next_window': next_window,
        'pages': range(1, total_page_cnt + 1),
        'prev_page': page - 1,
        'next_page': page + 1
    }


# 여기서 부터 sql 쿼리문에 쓰는 함수
def where_check(img, kw, my_post, start_date, end_date):
    if img == 'true' or (kw is not None and kw != 'None') or my_post == 'true' \
            or ((start_date is not None and start_date != 'None') and (end_date is not None and end_date != 'None')):
        where = " WHERE "
    else:
        where = ""
    return where


def img_check(img):
    if img == 'true':
        img = "img IS NOT NULL"
    else:
        img = ""
    return img


def and_check(img, kw):
    if img == 'true' and (kw is not None and kw != 'None'):
        many = " AND "
    else:
        many = ""
    return many


def topic_check(topic):
    if topic is None or topic == 'None':
        topic = ""
    else:
        topic = topic
    return topic


def kw_check(kw):
    if kw is None or kw == 'None':
        kw = ""
    else:
        kw = " LIKE '%" + kw + "%'"
    return kw


def and2_check(img, kw, my_post):
    if (img == 'true' or (kw is not None and kw != 'None')) and my_post == 'true':
        many = " AND "
    else:
        many = ""
    return many


def my_post_check(my_post, user_id):
    if my_post == 'true':
        if user_id is None or user_id == 'None':
            my_post = "user_id = 'None'"
        else:
            my_post = "user_id = " + user_id
    else:
        my_post = ""
    return my_post


def and3_check(img, kw, my_post, start_date, end_date):
    if (img == 'true' or (kw is not None and kw != 'None') or my_post == 'true') \
            and ((start_date is not None and start_date != 'None') and (end_date is not None and end_date != 'None')):
        many = " AND "
    else:
        many = ""
    return many


def date_check(start_date, end_date):
    if (start_date is not None and start_date != 'None') and (end_date is not None and end_date != 'None'):
        date = "date BETWEEN '" + start_date + "' AND '" + end_date + "'"
    else:
        date = ""
    return date


def order_check(order):
    if order == 'date_asc':
        order = 'date ASC'
    elif order == 'title_asc':
        order = 'title ASC'
    elif order == 'writer_asc':
        order = 'writer ASC'
    else:
        order = 'date DESC'
    return order






