import os, json
import requests
from datetime import date, datetime, timedelta
from datatransfer import insert_data_to_db

managed_cur = ['EUR', ]

def update_currency_through_api(days):
    """
    For updating EUR currency history at once
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_file = os.path.join(BASE_DIR, 'secrets.json')
    with open(secret_file) as f:
        secrets = json.loads(f.read())

    url = ""
    url_prefix = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey="
    secure_key = secrets['CUR_API_SECURE_KEY']
    datatype = "AP01"

    """
    date.weekday()
    Return the day of the week as an integer, where Monday is 0 and Sunday is 6.
    """

    insert_query = ""
    previous_cur = []

    for i in range(days, -1, -1):
        
        date = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
        url = url_prefix + secure_key + "&" + "searchdate=" + date + "&data=" + datatype
        response  = requests.get(url)
        today_cur = response.json()
        is_holiday = False
        if not bool(today_cur) :
            #print(f'[warning] there is no data on {date}')
            actual_cur = previous_cur
            is_holiday = True
        else:
            actual_cur = today_cur
        
        for each_country in actual_cur:
            if each_country['cur_unit'] in managed_cur:
                print("{} : {} 당시 환율은 1 {} 당 {}원 입니다.".format(date, each_country['cur_nm'], each_country['cur_unit'], each_country['deal_bas_r']))
                insert_query += "INSERT INTO category_currency (date, is_holiday, cur_unit, cur_nm, ttb, tts, deal_bas_r, bkpr, yy_efee_r, ten_dd_efee_r, kftc_deal_bas_r, kftc_bkpr) SELECT '{}', {}, '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {} WHERE NOT EXISTS (SELECT 1 FROM category_currency WHERE date='{}' and cur_unit='{}');\n"\
                    .format(date, is_holiday, each_country['cur_unit'], each_country['cur_nm'],\
                        float(each_country['ttb'].replace(',','')), float(each_country['tts'].replace(',','')),\
                        float(each_country['deal_bas_r'].replace(',','')), float(each_country['bkpr'].replace(',','')),\
                        float(each_country['yy_efee_r'].replace(',','')), float(each_country['ten_dd_efee_r'].replace(',','')),\
                        float(each_country['kftc_deal_bas_r'].replace(',','')), float(each_country['kftc_bkpr'].replace(',','')),\
                        date, each_country['cur_unit'])
        if bool(today_cur):
            previous_cur = today_cur
        
    insert_data_to_db(insert_query, "")

update_currency_through_api(1)
