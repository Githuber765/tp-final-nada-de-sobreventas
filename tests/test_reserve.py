import time
from concurrent.futures import ThreadPoolExecutor

import pymysql
import requests


BASE_URL = "http://localhost:8001"


def get_mysql_connection():
    return pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="marketplace",
        cursorclass=pymysql.cursors.DictCursor
    )


def set_stock(product_id: int, stock: int):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE productos SET stock = %s WHERE id = %s",
                (stock, product_id)
            )
        connection.commit()
    finally:
        connection.close()


def get_stock(product_id: int) -> int:
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT stock FROM productos WHERE id = %s",
                (product_id,)
            )
            row = cursor.fetchone()
            return row["stock"]
    finally:
        connection.close()


def reserve(product_id: int, quantity: int):
    return requests.post(
        f"{BASE_URL}/reserve",
        json={
            "product_id": product_id,
            "quantity": quantity
        },
        timeout=10
    )


def test_dos_usuarios_mismo_producto_stock_uno():
    product_id = 1
    set_stock(product_id, 1)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(reserve, product_id, 1),
            executor.submit(reserve, product_id, 1)
        ]

    responses = [future.result() for future in futures]
    status_codes = [response.status_code for response in responses]

    successful_reservations = status_codes.count(200)
    failed_reservations = len(status_codes) - successful_reservations
    final_stock = get_stock(product_id)

    assert successful_reservations == 1
    assert failed_reservations == 1
    assert final_stock == 0
    assert final_stock >= 0


def test_cincuenta_usuarios_diez_productos():
    product_id = 3
    set_stock(product_id, 10)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [
            executor.submit(reserve, product_id, 1)
            for _ in range(50)
        ]

    responses = [future.result() for future in futures]
    status_codes = [response.status_code for response in responses]

    successful_reservations = status_codes.count(200)
    failed_reservations = len(status_codes) - successful_reservations
    final_stock = get_stock(product_id)

    assert successful_reservations == 10
    assert failed_reservations == 40
    assert final_stock == 0
    assert final_stock >= 0


def test_endpoint_responde_rapido():
    product_id = 2
    set_stock(product_id, 1)

    start = time.time()
    response = reserve(product_id, 1)
    duration = time.time() - start

    assert duration < 5
    assert response.status_code in [200, 400, 503]