import pandas as pd
import streamlit as st
import openai
import os

openai.organization = "org-pIQFshReeZ4tEMfF1TiwvWT1"
openai.api_key = os.getenv("OPENAI_API_KEY")





def Ask_ChatGPT(message):
    
    # 応答設定
    completion = openai.ChatCompletion.create(
                 model    = "gpt-3.5-turbo-0301",     # モデルを選択
                 messages = [{
                            "role":"system","content":"Consultants on utility costs",
                            "role":"assistant","content":message,   # メッセージ 

                            }],
    
                 max_tokens  = 1024,             # 生成する文章の最大単語数
                 n           = 1,                # いくつの返答を生成するか
                 stop        = None,             # 指定した単語が出現した場合、文章生成を打ち切る
                 temperature = 0.7,              # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
    )
    
    # 応答
    response = completion.choices[0].message.content
    
    # 応答内容出力
    return response


def find_key_by_name(fuel_data, name):
    for key, value in fuel_data.items():
        if value["name"] == name:
            return key
    return None

    


fuel_data = {
    "propane": {
        "material": "LPガス",
        "name": "プロパン(MJ/kg)",
        "unit": "kg",
        "highHeatValue": 50.3224811545823,
        "lowHeatValue": 46.6489400302978,
        "co2Factor": 0.81712914667223,
        "note": ""
    },
    "propan_low": {
        "material": "LPガス(低圧)",
        "name": "プロパン(MJ/m3)",
        "unit": "m3",
        "highHeatValue": 100.24398636371 * 0.502,
        "lowHeatValue": 92.9261753591589 * 0.502,
        "co2Factor": 1.62774730412795 * 0.502,
        "note": "0.502"
    },
    "butane": {
        "material": "LPガス",
        "name": "ブタン",
        "unit": "kg",
        "highHeatValue": 49.4321011868969,
        "lowHeatValue": 45.8235578002534,
        "co2Factor": 0.826578294369651,
        "note": ""
    },
    "kerosene": {
        "material": "石油",
        "name": "灯油",
        "unit": "L",
        "highHeatValue": 36.4945180652174,
        "lowHeatValue": 34.2683524632391,
        "co2Factor": 0.682672738147564,
        "note": ""
    },
    "lightOil": {
        "material": "石油",
        "name": "軽油",
        "unit": "L",
        "highHeatValue": 38.0418206289855,
        "lowHeatValue": 35.7593113912464,
        "co2Factor": 0.714974013318546,
        "note": ""
    },
    "heavyOilA": {
        "material": "石油",
        "name": "A重油",
        "unit": "L",
        "highHeatValue": 38.9020593739131,
        "lowHeatValue": 36.7235440489739,
        "co2Factor": 0.751705405591391,
        "note": ""
    },
    "cityGas": {
        "material": "LNG",
        "name": "都市ガス (13A)",
        "unit": "m3",
        "highHeatValue": 39.9641433589486,
        "lowHeatValue": 36.4872628867201,
        "co2Factor": 0.557671135633351,
        "note": ""
    },
    "electricity": {
        "material": "電力",
        "name": "電力(家庭用)",
        "unit": "kwh",
        "highHeatValue": 3.6,
        "lowHeatValue": 3.6,
        "co2Factor": 0.130555555555556,
        "note": ""
    }
}


st.title('熱量比較アプリ')

fuel_names = [v["name"] for v in fuel_data.values()]


st.write('条件を入力してください')
selected_fuel = st.selectbox(
'現在ご利用中のエネルギーを選択してください',
options=fuel_names)

st.write("""
        選択したエネルギーのご使用量、単価をご入力ください
        """)

month = '月間使用量で入力'
year = '年間使用量で入力'
volume_unit = ""
selected_key = find_key_by_name(fuel_data, selected_fuel)
selected_material = fuel_data[selected_key]["material"]
selected_unit = fuel_data[selected_key]["unit"]


    
month_year = st.radio("", [month, year], label_visibility="collapsed")
quantity = st.number_input(
'使用量',
step=(1)
)
if selected_material == "石油":
    volume_unit = st.selectbox("単位", options=["L", "kL"])
    if volume_unit == "kL":
                quantity = quantity * 1000
                selected_unit = "kL"

price = st.number_input('単価',
            step=(1))



st.write(f'''
    計算条件
''')



st.write(f'''
    エネルギー: {selected_fuel}
''')

st.write(f'''
    使用量: {quantity} {selected_unit}
''')

st.write(f'''
    単　価: {price} 円/{selected_unit}
''')


calory_high = fuel_data[selected_key]["highHeatValue"]*quantity
calory_low = fuel_data[selected_key]["lowHeatValue"]*quantity
co2 = fuel_data[selected_key]["co2Factor"]*quantity

ratios = {}
for key, value in fuel_data.items():
    if key != selected_key:
        high_quantity = calory_high / value["highHeatValue"]
        low_quantity = calory_low / value["lowHeatValue"]
        co2_high_ratio = high_quantity * value["co2Factor"]
        co2_low_ratio = low_quantity * value["co2Factor"]
        price_high_ratio = 0 if high_quantity == 0 else quantity / high_quantity * price
        price_low_ratio = 0 if low_quantity == 0 else quantity / low_quantity * price
        co2_diff_high = co2_high_ratio - co2
        co2_diff_low =  co2_low_ratio - co2

        ratios[key] = {
            "high_quantity": high_quantity,
            "low_quantity": low_quantity,
            "co2_high_ratio": co2_high_ratio,
            "co2_low_ratio": co2_low_ratio,
            "price_high_ratio": price_high_ratio,
            "price_low_ratio": price_low_ratio,
            "co2_diff_high": co2_diff_high,
            "co2_diff_low" : co2_diff_low
        }

# 燃料の並び順に従ってratiosを作成
ordered_ratios = {key: ratios[key] for key in fuel_data.keys() if key != selected_key}

# selected_fuelを上書き
selected_fuel = fuel_data[selected_key]["name"]

if st.button('計算する'):
    # 以下の条件を追加
    if price == 0 or quantity == 0:
        st.warning("単価または使用量が0です。正しい値を入力してください。")
    else:
        # 燃料の並び順に従ってratiosを作成
        ordered_ratios = {key: ratios[key] for key in fuel_data.keys() if key != selected_key}
        # 選択された燃料のデータをratiosに追加
        ordered_ratios[selected_key] = {
            "high_quantity": quantity,
            "low_quantity": quantity,
            "co2_high_ratio": co2,
            "co2_low_ratio": co2,
            "price_high_ratio": price,
            "price_low_ratio": price,
            "co2_diff_high": 0,
            "co2_diff_low" : 0
        }

        # ordered_ratiosをデータフレームに変換
        ratios_df = pd.DataFrame(ordered_ratios).T
        if month_year == year:
                ratios_df["high_quantity"] /= 12
                ratios_df["low_quantity"] /= 12

        # 燃料名と単位をデータフレームに追加
        ratios_df['name'] = [fuel_data[key]['name'] for key in ratios_df.index]
        ratios_df['unit'] = [fuel_data[key]['unit'] for key in ratios_df.index]

        # high_ratioとlow_ratioを同じ行で表示し、交互に配置
        high_ratio_df = ratios_df[['name', 'unit','high_quantity', 'price_high_ratio', 'co2_high_ratio','co2_diff_high']].copy()
        high_ratio_df['ratio_label'] = '高位'
        low_ratio_df = ratios_df[['name', 'unit','low_quantity', 'price_low_ratio','co2_low_ratio', 'co2_diff_low']].copy()
        low_ratio_df['ratio_label'] = '低位'

        # 列名を統一
        high_ratio_df.columns = ['燃料名', '単位','月間使用量', '同等単価','CO2量',  '差', 'ratio_label']
        low_ratio_df.columns = ['燃料名', '単位', '月間使用量','同等単価', 'CO2量', '差', 'ratio_label']

        # 両方のデータフレームを結合
        combined_df = pd.concat([high_ratio_df, low_ratio_df]).reset_index(drop=True)

        # 列の順序を調整
        columns_order = ['燃料名', '単位', 'ratio_label',  '月間使用量','同等単価','CO2量',  '差']
        combined_df = combined_df[columns_order]

        # 燃料名に従ってソート
        combined_df['name_order'] = combined_df['燃料名'].apply(lambda x: fuel_names.index(x))
        combined_df.sort_values(by=['name_order', 'ratio_label'], inplace=True)
        combined_df.drop(columns=['name_order'], inplace=True)

        # カラム名が空白のカラムを追加
        combined_df.insert(2, "", combined_df['ratio_label'])

        # ratio_labelカラムを削除
        combined_df.drop(columns=['ratio_label'], inplace=True)

        combined_df[['月間使用量', '同等単価', 'CO2量', '差']] = combined_df[['月間使用量', '同等単価', 'CO2量', '差']].round(0).applymap(int)

        def highlight_selected_fuel(row):
            name = row['燃料名']
            if name == selected_fuel:
                return ['background-color: yellow']*len(row)
            return ['']*len(row)
        combined_df.reset_index(drop=True, inplace=True)
        combined_df_styled = combined_df.style.apply(highlight_selected_fuel, axis=1).format({
            '月間使用量': '{:,}',
            '同等単価': '{:,}',
            'CO2量': '{:,}',
            '差': '{:,}'
        }).hide_index()

        if price == 0 or quantity == 0:
            st.error("単価または使用量が0のため、計算できません。正しい値を入力してください。")
        else:
            
            st.write(combined_df_styled)

    # 燃料の並び順に従ってratiosを作成
        ordered_ratios2 = {key: ratios[key] for key in fuel_data.keys() if key != selected_key}
        # 選択された燃料のデータをratiosに追加
        ordered_ratios2[selected_key] = {
            "high_quantity": quantity,
            "low_quantity": quantity,
            "co2_high_ratio": co2,
            "co2_low_ratio": co2,
            "price_high_ratio": price,
            "price_low_ratio": price,
            "co2_diff_high": 0,
            "co2_diff_low" : 0
        }

        # ordered_ratiosをデータフレームに変換
        ratios_df2 = pd.DataFrame(ordered_ratios2).T
        if month_year == month:
            ratios_df2["high_quantity"] *= 12
            ratios_df2["low_quantity"] *= 12

        # 燃料名と単位をデータフレームに追加
        ratios_df2['name'] = [fuel_data[key]['name'] for key in ratios_df.index]
        ratios_df2['unit'] = [fuel_data[key]['unit'] for key in ratios_df.index]

        # high_ratioとlow_ratioを同じ行で表示し、交互に配置
        high_ratio_df2 = ratios_df2[['name', 'unit','high_quantity', 'price_high_ratio', 'co2_high_ratio','co2_diff_high']].copy()
        high_ratio_df2['ratio_label'] = '高位'
        low_ratio_df2 = ratios_df2[['name', 'unit','low_quantity', 'price_low_ratio','co2_low_ratio', 'co2_diff_low']].copy()
        low_ratio_df2['ratio_label'] = '低位'

        # 列名を統一
        high_ratio_df2.columns = ['燃料名', '単位','年間使用量', '同等単価','CO2量',  '差', 'ratio_label']
        low_ratio_df2.columns = ['燃料名', '単位', '年間使用量','同等単価', 'CO2量', '差', 'ratio_label']

        # 両方のデータフレームを結合
        combined_df2 = pd.concat([high_ratio_df2, low_ratio_df2]).reset_index(drop=True)

        # 列の順序を調整
        columns_order2 = ['燃料名', '単位', 'ratio_label',  '年間使用量','同等単価','CO2量',  '差']
        combined_df2 = combined_df2[columns_order2]

        # 燃料名に従ってソート
        combined_df2['name_order'] = combined_df2['燃料名'].apply(lambda x: fuel_names.index(x))
        combined_df2.sort_values(by=['name_order', 'ratio_label'], inplace=True)
        combined_df2.drop(columns=['name_order'], inplace=True)

        combined_df2.insert(2, "", combined_df2['ratio_label'])

        # ratio_labelカラムを削除
        combined_df2.drop(columns=['ratio_label'], inplace=True)

        combined_df2[['年間使用量', '同等単価', 'CO2量', '差']] = combined_df2[['年間使用量', '同等単価', 'CO2量', '差']].round(0).applymap(int)

        def highlight_selected_fuel(row):
            name = row['燃料名']
            if name == selected_fuel:
                return ['background-color: yellow']*len(row)
            return ['']*len(row)
        
        combined_df2.reset_index(drop=True, inplace=True)

        combined_df_styled2 = combined_df2.style.apply(highlight_selected_fuel, axis=1).format({
            '年間使用量': '{:,}',
            '同等単価': '{:,}',
            'CO2量': '{:,}',
            '差': '{:,}'
        }).hide_index()

    

        with st.expander('年間の場合を見る'):
            st.write(combined_df_styled2)

    # 辞書をデータフレームに変換
    fuel_df = pd.DataFrame(fuel_data).T

    # 'material' をインデックスとして使いたい文字列のリストを作成
    index_list = fuel_df["material"].tolist()

    # インデックスを 'material' に設定
    fuel_df.index = index_list

    # 列名を変更
    fuel_df.columns = ['原料', '燃料名', '単位', '高位発熱量', '低位発熱量', 'CO2係数', '換算値']

    # '原料' の列を削除
    fuel_df.drop(columns=['原料'], inplace=True)

    with st.expander('使用する係数等、計算方法を見る'):
        # 結果を表示
        st.write(fuel_df)
    
with st.expander('AIアッチ君になんでも質問してみよう!!'):
    input_text = st.text_input("質問を入力してください:")
    if st.button("送信"):
        if input_text:
            response = Ask_ChatGPT(input_text)
            st.write("アッチ君がお答えするよ!!:", response)
    else:
        st.write("質問を入力してください。")

