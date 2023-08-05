import autodynatrace

import cx_Oracle

class A:

    @autodynatrace.trace
    def query(self):

        dsn = cx_Oracle.makedsn("localhost", 1521, service_name="ORCLCDB.localdomain")
        connection: cx_Oracle.Connection = cx_Oracle.connect(user="david", password="password", dsn=dsn)

        cursor: cx_Oracle.Cursor
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT make_me_slow( 0.01 ) FROM dual CONNECT BY level <= 100")
                for i, row in enumerate(cursor):
                    pass
        except Exception as e:
            print(e)

        connection.close()


def main():
    import time

    while True:
        a = A()
        a.query()
        time.sleep(5)


if __name__ == "__main__":
    main()
