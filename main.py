import datetime
import psycopg2
from datetime import timedelta

db_params = {
    "host": "host",
    "database": "database",
    "user": "user",
    "password": "password",
    "port": "port"
}

# переменная для проверки
# today = dt.date.today()


def month_value(today: datetime.date) -> list:
    last_day = today - timedelta(days=1)
    first_day = last_day.replace(day=1)
    time_chain = f"'{first_day}'" + ' AND ' + f"'{last_day}'"

    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        query_1 = ''' SELECT COUNT(pp.problem_id) AS amount
                      FROM 
                           problems_petition AS pp LEFT JOIN problems_problem pp2 
                           ON pp.problem_id = pp2.id
                     WHERE pp.num = 1 
                       AND pp2.reason_id = 250
                       AND pp.moderator_accepted_at::date BETWEEN ''' + time_chain

        cursor.execute(query_1)
        result = cursor.fetchall()

        if today.strftime('%d%m') == '0101':
            first_day = last_day.replace(day=1, month=1)
            time_chain = f"'{first_day}'" + ' AND ' + f"'{last_day}'"
            query_2 = ''' SELECT COUNT(pp.problem_id) AS amount
                      FROM 
                           problems_petition AS pp LEFT JOIN problems_problem pp2 
                           ON pp.problem_id = pp2.id
                     WHERE pp.num = 1 
                       AND pp2.reason_id = 250
                       AND pp.moderator_accepted_at::date BETWEEN ''' + time_chain
            cursor.execute(query_2)
            result = result + cursor.fetchall()

        return result

        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        return "Ошибка при подключении к базе данных: " + str(e)