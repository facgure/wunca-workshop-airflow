import json
import urllib
from datetime import datetime, timedelta

from airflow import DAG
from airflow import Dataset
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python import PythonOperator


def on_failure(context):

    dag_id = context['dag_run'].dag_id

    task_id = context['task_instance'].task_id
    context['task_instance'].xcom_push(key=dag_id, value=True)

    logs_url = "http://localhost:8080/log?dag_id={}&task_id={}&execution_date={}".format(
        dag_id, task_id, context['ts'])

    print(logs_url)


default_args = {
    'owner': 'Facgure',
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
    'on_failure_callback': on_failure
}


def GET_UNIV_FROM_UM(ti=None):
    url = "https://www.umultirank.org/json/exploreUniFinder.json"
    request = urllib.request.urlopen(url)
    html = request.read().decode("utf8")
    data_uni = json.loads(html)
    list_datauni = []
    list_id = []
    # data of university
    for i in data_uni['unis']:
        data = {'uid': i['id'],
                'name': i['name'],
                'slug': i['slug'],
                'url': i['url'],
                'street': i['street'],
                'city': i['city'],
                'country': i['country'],
                'phone': i['tele'],
                'fax': i['fax'],
                'postalCode': i['postalCode'],
                'remark': i['remark'],
                'profile': i['profile']}
        list_datauni.append(tuple(data.values()))
        list_id.append(i['id'])

    ti.xcom_push(key='university', value=list_datauni)
    ti.xcom_push(key='id', value=list_id)


def prepare_data(dt, id, title_table, sub_table, fact_table, subject_ranking, major):
    url = "https://www.umultirank.org/json/uniData.json?id="+str(id)
    request = urllib.request.urlopen(url)
    html = request.read().decode("utf8")
    data_uni = json.loads(html)

    for i in data_uni['institutional']['mainData']:
        # indicator
        title = [i['dimension']['id'],
                 i['dimension']['name'],
                 i['dimension']['colgroup'],
                 i['dimension']['sort']]
        if title[0] != -1:
            title_table.append(title)
        # sub indicator
        for sub in i['rows']:
            sub_dic = sub.pop('indicator')
            sub_title = [sub_dic['dimension'],
                         sub_dic['id'],
                         sub_dic['name'],
                         sub_dic['sort'],
                         sub_dic['min'],
                         sub_dic['max'],
                         sub_dic['valueType'],
                         sub_dic['description'],
                         sub_dic['lowerIsBetter'],
                         sub_dic['decimal']]
            sub_table.append(sub_title)
            # check grade
            if sub['rankGroup']:
                grade = sub['rankGroup']
            else:
                grade = 0
            # rank table
            fact = [id,
                    sub_title[0],
                    sub_title[1],
                    0,  # subject_id
                    0,  # major_id
                    sub['value'],
                    grade,
                    sub['remark'],
                    sub['entity'],
                    sub['valueType'],
                    int(dt.split('-')[0])]  # year of the data
            fact_table.append(fact)
    # ranking by subject
    if data_uni['fields']:
        # main subject
        for i in data_uni['fields']:
            # subject and major
            sub = [i['id'], i['name']]
            major0 = [i['id'], int(str(i['id'])+'000000'),
                      'faculty as a whole (' + i['name']+')']
            major.append(major0)
            subject_ranking.append(sub)
            for j in i['departments'][-1]['programData']:
                major_i = [i['id'], j['program']['id'], j['program']['name']]
                major.append(major_i)
                # indicator / ranking
                for man in j['mainData']:
                    title = [man['dimension']['id'],
                             man['dimension']['name'],
                             man['dimension']['colgroup'],
                             man['dimension']['sort']]
                    if title[0] != -1:
                        title_table.append(title)
                        for sub in man['rows']:
                            sub_dic = sub.pop('indicator')
                            sub_title = [sub_dic['dimension'],
                                         sub_dic['id'],
                                         sub_dic['name'],
                                         sub_dic['sort'],
                                         sub_dic['min'],
                                         sub_dic['max'],
                                         sub_dic['valueType'],
                                         sub_dic['description'],
                                         sub_dic['lowerIsBetter'],
                                         sub_dic['decimal']]
                            sub_table.append(sub_title)
                            # check grade
                            if sub['rankGroup']:
                                grade = sub['rankGroup']
                            else:
                                grade = 0
                            fact = [id,
                                    sub_title[0],
                                    sub_title[1],
                                    major_i[0],
                                    major_i[1],
                                    sub['value'],
                                    grade,
                                    sub['remark'],
                                    sub['entity'],
                                    sub['valueType'],
                                    int(dt.split('-')[0])]
                            fact_table.append(fact)
            # for each major
            for da in i['departments'][-1]['mainData']:
                title = [da['dimension']['id'],
                         da['dimension']['name'],
                         da['dimension']['colgroup'],
                         da['dimension']['sort']]
                if title[0] != -1:
                    title_table.append(title)
                for sub in da['rows']:
                    try:
                        sub_dic = sub.pop('indicator')
                        sub_title = [sub_dic['dimension'],
                                     sub_dic['id'],
                                     sub_dic['name'],
                                     sub_dic['sort'],
                                     sub_dic['min'],
                                     sub_dic['max'],
                                     sub_dic['valueType'],
                                     sub_dic['description'],
                                     sub_dic['lowerIsBetter'],
                                     sub_dic['decimal']]
                        sub_table.append(sub_title)
                        if sub['rankGroup']:
                            grade = sub['rankGroup']
                        else:
                            grade = 0
                        fact = [id,
                                sub_title[0],
                                sub_title[1],
                                major_i[0],
                                major_i[1],
                                sub['value'],
                                grade,
                                sub['remark'],
                                sub['entity'],
                                sub['valueType'],
                                int(dt.split('-')[0])]
                        fact_table.append(fact)
                    except:
                        continue
    return (title_table, sub_table, fact_table, subject_ranking, major)


def del_duplicate_list(list_i):
    new_list = []
    for x in range(len(list_i)):
        if list_i[x] not in new_list:
            new_list.append(list_i[x])
    return new_list


def GET_INDICATOR_FROM_UM(EXEC_DATE, ti=None):
    dt = EXEC_DATE
    university_id = ti.xcom_pull(task_ids='GET_UNIV_FROM_UM', key='id')
    title_table = []
    sub_table = []
    fact_table = []
    subject_ranking = [(0, "University as a whole")]
    major = [(0, 0, "University as a whole")]
    for id in university_id:
        print(id)
        title_table, sub_table, fact_table, subject_ranking, major = prepare_data(
            dt, id, title_table, sub_table, fact_table, subject_ranking, major)
    title_table = del_duplicate_list(title_table)
    sub_table = del_duplicate_list(sub_table)
    subject_ranking = del_duplicate_list(subject_ranking)
    major = del_duplicate_list(major)
    indicators = {"title": title_table, "sub": sub_table,
                  "fact": fact_table, "subject": subject_ranking, "major": major}
    ti.xcom_push(key='indicators', value=indicators)


def INSERT_UM_UNIVERSTY(ti):
    mysql_hook = MySqlHook(mysql_conn_id='U_MULTIRANK_RANKING')
    mysql_conn = mysql_hook.get_conn()
    mysql_cursor = mysql_conn.cursor()
    Metadata = ti.xcom_pull(task_ids='GET_UNIV_FROM_UM', key='university')
    for i in range(0, len(Metadata), 1000):
        query = """
            INSERT INTO UM_UNIVERSITY (
                UID,
                NAME,
                SLUG,
                URL,
                STREET,
                CITY,
                COUNTRY,
                PHONE,
                FAX,
                POSTALCODE,
                REMARK,
                PROFILE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                NAME = VALUES(NAME),
                SLUG = VALUES(SLUG),
                URL = VALUES(URL),
                STREET = VALUES(STREET),
                CITY = VALUES(CITY),
                COUNTRY = VALUES(COUNTRY),
                PHONE = VALUES(PHONE),
                FAX = VALUES(FAX),
                POSTALCODE = VALUES(POSTALCODE),
                REMARK = VALUES(REMARK),
                PROFILE = VALUES(PROFILE);
        """
        mysql_cursor.executemany(query, Metadata[i:i+1000])
        mysql_conn.commit()


def INSERT_UM_INDICATOR(ti):
    mysql_hook = MySqlHook(mysql_conn_id='U_MULTIRANK_RANKING')
    mysql_conn = mysql_hook.get_conn()
    mysql_cursor = mysql_conn.cursor()
    indicators = ti.xcom_pull(
        task_ids='GET_INDICATOR_FROM_UM', key='indicators')
    title = indicators['title']
    sub = indicators['sub']
    subject = indicators['subject']
    major = indicators['major']

    # subject
    for i in range(0, len(subject), 1000):
        query = """
            INSERT INTO UM_SUBJECT (
                SUBJECT_ID,
                NAME)
            VALUES (%s,%s)
            ON DUPLICATE KEY UPDATE
                NAME = VALUES(NAME);
        """
        mysql_cursor.executemany(query, subject[i:i+1000])
        mysql_conn.commit()

    # major
    for i in range(0, len(major), 1000):
        query = """
            INSERT INTO UM_MAJOR (
                SUBJECT_ID,
                MAJOR_ID,
                NAME)
            VALUES (%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                SUBJECT_ID = VALUES(SUBJECT_ID),
                NAME = VALUES(NAME);
        """
        mysql_cursor.executemany(query, major[i:i+1000])
        mysql_conn.commit()

    # indicator
    for i in range(0, len(title), 1000):
        query = """
            INSERT INTO UM_INDICATOR (
                INID,
                NAME,
                COLGROUP,
                SORT)
            VALUES (%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                NAME = VALUES(name),
                COLGROUP = VALUES(COLGROUP),
                SORT = VALUES(SORT);
        """
        mysql_cursor.executemany(query, title[i:i+1000])
        mysql_conn.commit()

    # sub indicator
    for i in range(0, len(sub), 1000):
        query = """
        INSERT INTO UM_SUB_INDICATOR (
            INID,
            SUBINID,
            NAME,
            SORT,
            MIN,
            MAX,
            VALUE_TYPE,
            DESCRIPTION,
            LOWER_IS_BETTER,
            `DECIMAL`)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE
            INID = VALUES(INID),
            NAME = VALUES(NAME),
            SORT = VALUES(SORT),
            MIN = VALUES(MIN),
            MAX = VALUES(MAX),
            VALUE_TYPE = VALUES(VALUE_TYPE),
            DESCRIPTION = VALUES(DESCRIPTION),
            LOWER_IS_BETTER = VALUES(LOWER_IS_BETTER),
            `DECIMAL` = VALUES(`DECIMAL`);
        """
        mysql_cursor.executemany(query, sub[i:i+1000])
        mysql_conn.commit()


def INSERT_UM_RANK(ti):
    mysql_hook = MySqlHook(mysql_conn_id='U_MULTIRANK_RANKING')
    mysql_conn = mysql_hook.get_conn()
    mysql_cursor = mysql_conn.cursor()
    indicators = ti.xcom_pull(
        task_ids='GET_INDICATOR_FROM_UM', key='indicators')
    fact = indicators['fact']
    for i in range(0, len(fact), 10000):
        query = """
            INSERT INTO UM_RANK (
                UID,
                INID,
                SUBINID,
                SUBJECT_ID,
                MAJOR_ID,
                SCORE,
                RANK_GROUP,
                REMARK,
                ENTITY,
                VALUE_TYPE,
                YEAR)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                SCORE = VALUES(SCORE),
                RANK_GROUP = VALUES(RANK_GROUP),
                REMARK = VALUES(REMARK),
                ENTITY = VALUES(ENTITY),
                VALUE_TYPE = VALUES(VALUE_TYPE);
        """
        mysql_cursor.executemany(query, fact[i:i+10000])
        mysql_conn.commit()


with DAG(
    dag_id='U_MULTIRANK',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # '0 10 1 */3 *'
    tags=['umultirank', 'ranking']
) as dag:

    task1 = PythonOperator(
        task_id='GET_UNIV_FROM_UM',
        python_callable=GET_UNIV_FROM_UM,
        inlets={
            "datasets": [
                Dataset("Website", "U-Multirank")
            ]}
    )

    task2 = PythonOperator(
        task_id='GET_INDICATOR_FROM_UM',
        python_callable=GET_INDICATOR_FROM_UM,
        op_kwargs={'EXEC_DATE': '{{ ds }}'},
        inlets={
            "datasets": [
                Dataset("Website", "U-Multirank")
            ]}
    )

    task3 = PythonOperator(
        task_id='INSERT_UM_UNIVERSTY',
        python_callable=INSERT_UM_UNIVERSTY,
        outlets={
            "datasets": [
                Dataset("mysql", "U_MULTIRANK_RANKING.UM_UNIVERSITY"),
            ]}
    )

    task4 = PythonOperator(
        task_id='INSERT_UM_INDICATOR',
        python_callable=INSERT_UM_INDICATOR,
        outlets={
            "datasets": [
                Dataset("mysql", "U_MULTIRANK_RANKING.UM_MAJOR"),
                Dataset("mysql", "U_MULTIRANK_RANKING.UM_SUBJECT"),
                Dataset("mysql", "U_MULTIRANK_RANKING.UM_INDICATOR"),
                Dataset("mysql", "U_MULTIRANK_RANKING.UM_SUB_INDICATOR")
            ]}
    )

    task5 = PythonOperator(
        task_id='INSERT_UM_RANK',
        python_callable=INSERT_UM_RANK,
        outlets={
            "datasets": [
                Dataset("mysql", "U_MULTIRANK_RANKING.UM_RANK")
            ]}
    )

    task1 >> [task2, task3] >> task4 >> task5
