from flask import Flask, render_template, request, jsonify
import json
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import os


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ワクチンデータをロード
with open(os.path.join(BASE_DIR, 'static', 'DATA.json'), 'r') as f:
    vaccines = json.load(f)

# ルートページ（HTMLフォーム）を表示
@app.route('/')
def index():
    return render_template('index.html', time=time)

### フォームのデータを受け取り、処理 ###
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # JSONデータを取得
    vaccine_date = data.get("vaccination-date")
    birthdate = data.get("birthdate")
    vaccine_data = data.get("vaccine_data")

    if not vaccine_date:
        return jsonify({"error": "接種日を入力してください。"}), 400
    if not birthdate:
        return jsonify({"error": "生年月日を入力してください。"}), 400
    if not vaccine_data:
        return jsonify({"error": "接種ワクチンのデータがありません。"}), 400

    vaccine_date = datetime.strptime(vaccine_date,"%Y-%m-%d")
    birthdate = datetime.strptime(birthdate,"%Y-%m-%d")

    ##データの処理
    check_list, warning_list, attend_dic = make_list(vaccine_date, birthdate, vaccine_data)

    attend_df = pd.DataFrame([(k, v[0], v[1]) for k, v in attend_dic.items()], columns=["ワクチン名", "回数", "接種時期"], index=None)
    attend_json = attend_df.to_dict(orient='records')

    # 結果メッセージの生成
    return jsonify({
        'vaccine_date': vaccine_date,
        'birthdate': birthdate,
        'vaccine_data': vaccine_data,
        "check_list": check_list,
        "warning_list": warning_list,
        "attend_json" : attend_json
        })

def make_list(vaccine_date, birthdate, vaccine_data):
    #定義→想定されるワクチン名を変数定義する
    hepatitis_b = "B型肝炎"
    rotavirus_mono = "ロタウイルス(1価)"
    rotavirus_penta = "ロタウイルス(5価)"
    pediatric_pneumococcus = "小児用肺炎球菌"
    pentavalent_vaccine = "五種混合"
    bcg_vaccine = "BCG"
    measles_rubella = "MR(麻疹風疹混合)"
    varicella_vaccine = "水痘(みずぼうそう)"
    mumpsVirus = "おたふくかぜ"
    
    #制限確認に必要な日付を入手
    date_6_days_ago = vaccine_date - timedelta(days=6+1) 
    date_27_days_ago = vaccine_date - timedelta(days=27+1)
    date_60_days_ago = vaccine_date - timedelta(days=60+1)
    date_139_days_ago = vaccine_date - timedelta(days=139+1)
    date_3_weeks_ago = vaccine_date - timedelta(weeks=3)
    date_4_weeks_ago = vaccine_date - timedelta(weeks=4)
    date_8_weeks_ago = vaccine_date - timedelta(weeks=8)
    date_3_months_ago = vaccine_date - relativedelta(months=3)
    date_5_months_ago = vaccine_date - relativedelta(months=5)
    date_6_months_ago = vaccine_date - relativedelta(months=6)
    date_18_months_ago = vaccine_date - relativedelta(months=18)
    # 誕生日からの期間に対応する日付を計算し、年月日形式に変換
    birth_14_weeks_6_days = birthdate + timedelta(weeks=14, days=6)
    birth_24_weeks = birthdate + timedelta(weeks=24)
    birth_32_weeks = birthdate + timedelta(weeks=32)
    birth_2_months = birthdate + relativedelta(months=2)
    birth_5_months = birthdate + relativedelta(months=5)
    birth_7_months = birthdate + relativedelta(months=7)
    birth_8_months = birthdate + relativedelta(months=8)
    birth_12_months = birthdate + relativedelta(months=12)
    birth_15_months = birthdate + relativedelta(months=15)
    
    # 計算された日付をY/M/D形式に変換
    formatted_date_6_days_ago = date_6_days_ago.strftime("%Y/%m/%d")
    formatted_date_27_days_ago = date_27_days_ago.strftime("%Y/%m/%d")
    formatted_date_60_days_ago = date_60_days_ago.strftime("%Y/%m/%d")
    formatted_date_139_days_ago = date_139_days_ago.strftime("%Y/%m/%d")
    formatted_date_3_weeks_ago = date_3_weeks_ago.strftime("%Y/%m/%d")
    formatted_date_4_weeks_ago = date_4_weeks_ago.strftime("%Y/%m/%d")
    formatted_date_8_weeks_ago = date_8_weeks_ago.strftime("%Y/%m/%d")
    formatted_date_3_months_ago = date_3_months_ago.strftime("%Y/%m/%d")
    formatted_date_5_months_ago = date_5_months_ago.strftime("%Y/%m/%d")
    formatted_date_6_months_ago = date_6_months_ago.strftime("%Y/%m/%d")
    formatted_date_18_months_ago = date_18_months_ago.strftime("%Y/%m/%d")
    
    # 誕生日からの期間に対応する日付をY/M/D形式に変換
    formatted_birth_14_weeks_6_days = birth_14_weeks_6_days.strftime("%Y/%m/%d")
    formatted_birth_24_weeks = birth_24_weeks.strftime("%Y/%m/%d")
    formatted_birth_32_weeks = birth_32_weeks.strftime("%Y/%m/%d")
    formatted_birth_2_months = birth_2_months.strftime("%Y/%m/%d")
    formatted_birth_5_months = birth_5_months.strftime("%Y/%m/%d")
    formatted_birth_7_months = birth_7_months.strftime("%Y/%m/%d")
    formatted_birth_8_months = birth_8_months.strftime("%Y/%m/%d")
    formatted_birth_12_months = birth_12_months.strftime("%Y/%m/%d")
    formatted_birth_15_months = birth_15_months.strftime("%Y/%m/%d")
    
    #次回接種アテンドに必要な日付を入手
    formatted_date_6_days_later = (vaccine_date + timedelta(days=6+1)).strftime("%Y/%m/%d")
    formatted_date_27_days_later = (vaccine_date + timedelta(days=27+1)).strftime("%Y/%m/%d")
    formatted_date_60_days_later = (vaccine_date + timedelta(days=60+1)).strftime("%Y/%m/%d")
    formatted_date_139_days_later = (vaccine_date + timedelta(days=139+1)).strftime("%Y/%m/%d")
    formatted_date_3_weeks_later = (vaccine_date + timedelta(weeks=3)).strftime("%Y/%m/%d")
    formatted_date_4_weeks_later = (vaccine_date + timedelta(weeks=4)).strftime("%Y/%m/%d")
    formatted_date_8_weeks_later = (vaccine_date + timedelta(weeks=8)).strftime("%Y/%m/%d")
    formatted_date_3_months_later = (vaccine_date + relativedelta(months=3)).strftime("%Y/%m/%d")
    formatted_date_4_months_later = (vaccine_date + relativedelta(months=4)).strftime("%Y/%m/%d")
    formatted_date_5_months_later = (vaccine_date + relativedelta(months=5)).strftime("%Y/%m/%d")
    formatted_date_6_months_later = (vaccine_date + relativedelta(months=6)).strftime("%Y/%m/%d")
    formatted_date_12_months_later = (vaccine_date + relativedelta(months=12)).strftime("%Y/%m/%d")
    formatted_date_18_months_later = (vaccine_date + relativedelta(months=18)).strftime("%Y/%m/%d")


    #確認メッセージを作成
    check_list = []
    warning_list = []

    
    #生ワクチンを含むか否か
    live_vaccine = False
    for v in vaccine_data.keys():
        if vaccines[v]["vaccine-type"] == "live":
            live_vaccine = True
            break
    if live_vaccine:
        check_list.append(f"過去4週間({formatted_date_4_weeks_ago}以降)に注射生ワクチンを接種していない。（ロタウイルスは対象外）")


    #各ワクチンが含まれていた時の処理(チェックボックスと警告メッセージ)
    if hepatitis_b in vaccine_data.keys():
        if vaccine_data[hepatitis_b] == "1":
            if vaccine_date < birth_2_months:
                warning_list.append(f"{hepatitis_b}の1回目は生後2ヶ月以降での接種が推奨されています。（{formatted_birth_2_months}以降）")
        elif vaccine_data[hepatitis_b] == "2":
            check_list.append(f"{hepatitis_b}の1回目接種から27日以上経過している。（1回目接種：{formatted_date_27_days_ago} 以前）")
        elif vaccine_data[hepatitis_b] == "3":
            check_list.append(f"{hepatitis_b}の1回目接種から139日以上経過している。（1回目接種：{formatted_date_139_days_ago} 以前）")
            check_list.append(f"{hepatitis_b}の2回目接種から6日以上経過している。(2回目接種：{formatted_date_6_days_ago} 以前)")
            warning_list.append(f"{hepatitis_b}の3回目接種は2回目から4-5ヶ月の間隔を空けることが標準的です。")

    if rotavirus_mono in vaccine_data.keys():
        if vaccine_data[rotavirus_mono] == "1":
            if vaccine_date > birth_14_weeks_6_days:
                warning_list.append(f"生後15週0日以降の{rotavirus_mono}の初回接種は推奨されていません。")
        elif vaccine_data[rotavirus_mono] == "2":
            if vaccine_date > birth_24_weeks:
                warning_list.append(f"生後24週以降の{rotavirus_mono}の接種は認められていません。")
            else:
                check_list.append(f"{rotavirus_mono}の1回目接種から4週間以上経過している。（1回目接種：{formatted_date_4_weeks_ago} 以前）")

    if rotavirus_penta in vaccine_data.keys():
        if vaccine_data[rotavirus_penta] == "1":
            if vaccine_date > birth_14_weeks_6_days:
                warning_list.append(f"生後15週0日以降の{rotavirus_penta}の初回接種は推奨されていません。")
        elif vaccine_data[rotavirus_penta] in ["2", "3"]:
            if vaccine_data[rotavirus_penta] == "3" and vaccine_date > birth_32_weeks:
                warning_list.append(f"生後32週以降の{rotavirus_penta}の接種は認められていません。")
            else:
                check_list.append(f"{rotavirus_penta}の前回接種から4週間以上経過している。（前回接種：{formatted_date_4_weeks_ago} 以前）")

    if pediatric_pneumococcus in vaccine_data.keys():
        check_list.append(f"{pediatric_pneumococcus}の接種スケジュールは初回1回目接種日により変動します。別途確認してください。")

    if pentavalent_vaccine in vaccine_data.keys():
        if vaccine_data[pentavalent_vaccine] == "1":
            if vaccine_date < birth_2_months or vaccine_date > birth_7_months:
                warning_list.append(f"{pentavalent_vaccine}の初回接種推奨期間は生後2-7ヶ月\
                                    （{formatted_birth_2_months} 〜 {formatted_birth_7_months}）です。")
        elif vaccine_data[pentavalent_vaccine] in ["2", "3"]:
            check_list.append(f"{pentavalent_vaccine}の前回接種から3週間以上8週間未満経過している。\
                            (前回接種：{formatted_date_8_weeks_ago} 〜 {formatted_date_3_weeks_ago}）")
        elif vaccine_data[pentavalent_vaccine] == "4":
            check_list.append(f"{pentavalent_vaccine}の前回接種から6ヶ月以上18ヶ月未満経過している。\
                            (3回目接種：{formatted_date_18_months_ago} 〜 {formatted_date_6_months_ago}）")

    if bcg_vaccine in vaccine_data.keys():
        if vaccine_date < birth_5_months or vaccine_date > birth_8_months:
            warning_list.append(f"{bcg_vaccine}は副作用の観点から生後5-8ヶ月\
                            ({formatted_birth_5_months} 〜 {formatted_birth_8_months})での接種が推奨されています。")

    if measles_rubella in vaccine_data.keys():
        pass
    
    if varicella_vaccine in vaccine_data.keys():
        if vaccine_data[varicella_vaccine] == "2":
            check_list.append(f"{varicella_vaccine}の1回目接種から3ヶ月以上経過している。（1回目接種：{formatted_date_3_months_ago} 以前）")

    if mumpsVirus in vaccine_data.keys():
        if vaccine_date < birth_12_months:
            warning_list.append(f"{mumpsVirus}は1歳から接種可能です。")



##次回接種アテンドを作成
    attend_dic = {}
    if hepatitis_b in vaccine_data.keys():
        if vaccine_data[hepatitis_b] == "1":
            attend_dic[hepatitis_b] = ["2回目", f"{formatted_date_27_days_later} 以降"]
        elif vaccine_data[hepatitis_b] == "2":
            attend_dic[hepatitis_b] = ["3回目", f"{formatted_date_6_days_later}以降(推奨：{formatted_date_4_months_later} 〜 {formatted_date_5_months_later})"]
        elif vaccine_data[hepatitis_b] == "3":
            attend_dic[hepatitis_b] = ["完了","-"]

    if rotavirus_mono in vaccine_data.keys():
        if vaccine_data[rotavirus_mono] == "1":
            attend_dic[rotavirus_mono] = ["2回目", f"{formatted_date_4_weeks_later} 以降"]
        elif vaccine_data[rotavirus_mono] == "2":
            attend_dic[rotavirus_mono] = ["完了","-"]

    if rotavirus_penta in vaccine_data.keys():
        if vaccine_data[rotavirus_penta] == "1":
            attend_dic[rotavirus_penta] = ["2回目", f"{formatted_date_4_weeks_later} 以降"]
        elif vaccine_data[rotavirus_penta] == "2":
            attend_dic[rotavirus_penta] = ["3回目", f"{formatted_date_4_weeks_later} 以降"]
        elif vaccine_data[rotavirus_penta] == "3":
            attend_dic[rotavirus_penta] = ["完了", "-"]

    if pediatric_pneumococcus in vaccine_data.keys():
        attend_dic[pediatric_pneumococcus] = ["要確認", "-"]

    if pentavalent_vaccine in vaccine_data.keys():
        if vaccine_data[pentavalent_vaccine] == "1":
            attend_dic[pentavalent_vaccine] = ["2回目", f"{formatted_date_3_weeks_later} 〜 {formatted_date_8_weeks_later}"]
        elif vaccine_data[pentavalent_vaccine] == "2":
            attend_dic[pentavalent_vaccine] = ["3回目", f"{formatted_date_3_weeks_later} 〜 {formatted_date_8_weeks_later}"]
        elif vaccine_data[pentavalent_vaccine] == "3":
            attend_dic[pentavalent_vaccine] = ["4回目", f"{formatted_date_6_months_later} 以降(推奨：{formatted_date_6_months_later} 〜 {formatted_date_18_months_later} かつ 1歳以上)"]
        elif vaccine_data[pentavalent_vaccine] == "4":
            attend_dic[pentavalent_vaccine] = ["完了", "-"]

    if bcg_vaccine in vaccine_data.keys():
        attend_dic[bcg_vaccine] = ["完了", "-"]

    if measles_rubella in vaccine_data.keys():
        attend_dic[measles_rubella] = ["2回目", "小学校就学前の1年間"]
        
    if varicella_vaccine in vaccine_data.keys():
        if vaccine_data[varicella_vaccine] == "1":
            attend_dic[varicella_vaccine] = ["2回目", f"{formatted_date_3_months_later}以降(推奨：{formatted_date_6_months_later} 〜 {formatted_date_12_months_later})"]
        elif vaccine_data[varicella_vaccine] == "2":
            attend_dic[varicella_vaccine] = ["完了", "-"]

    if mumpsVirus in vaccine_data.keys():
        if vaccine_data[mumpsVirus] == "1":
            attend_dic[mumpsVirus] = ["2回目", "2 〜 6年後"]
        elif vaccine_data[mumpsVirus] == "2":
            attend_dic[mumpsVirus] = ["完了", "-"]

    return check_list, warning_list, attend_dic

if __name__ == '__main__':
    app.run(debug=True)
