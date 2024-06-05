from django.db import connection


def next_order_number() -> int:
    with connection.cursor() as cursor:
        cursor.execute("SELECT nextval('order_number')")
        return cursor.fetchone()[0]
