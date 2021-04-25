import numpy as np
import pandas as pd
import os
import pickle
import sklearn

def preprocess(x):
    valid_keys = ['職場の様子', '休日休暇(月曜日)', '大手企業', '交通費別途支給', '残業月20時間以上', 
                  '1日7時間以下勤務OK', '短時間勤務OK(1日4h以内)', '駅から徒歩5分以内', '学校・公的機関（官公庁）', 
                  '土日祝のみ勤務', 'Wordのスキルを活かす', '派遣スタッフ活躍中', '大量募集', 'Accessのスキルを活かす', 
                  '休日休暇(火曜日)', '平日休みあり', 'フラグオプション選択', '期間・時間　勤務期間', '派遣形態', 
                  '週2・3日OK', '勤務先公開', 'Excelのスキルを活かす', '16時前退社OK', '正社員登用あり', 
                  '残業月20時間未満', '英語力不要', '休日休暇(日曜日)', '社員食堂あり', '10時以降出社OK', 
                  '英語以外の語学力を活かす', '休日休暇(祝日)', '外資系企業', '服装自由', 'PowerPointのスキルを活かす', 
                  '休日休暇(土曜日)', '休日休暇(木曜日)', '英語力を活かす', 'PCスキル不要', '車通勤OK', '制服あり', 
                  '休日休暇(水曜日)', '仕事の仕方', '紹介予定派遣', 'シフト勤務', '経験者優遇', '週4日勤務', '未経験OK', 
                  '土日祝休み', '給与/交通費　交通費', '休日休暇(金曜日)', '扶養控除内', '給与/交通費　給与下限', 
                  'オフィスが禁煙・分煙', '残業なし']
    # valid_keysにあるkeyのみを順番通りに
    train_nums = x['お仕事No.']
    new_x = pd.DataFrame()
    x_keys = x.keys()
    for key in valid_keys:
        if key in x_keys:
            new_x[key] = x[key]
    
    return new_x, train_nums

def predict(x, train_nums):
    with open('./RFRModel.pkl', 'rb') as fp:
        rfr = pickle.load(fp)
    predicted = rfr.predict(x)
    y = pd.concat([pd.DataFrame(train_nums), pd.DataFrame(predicted)], axis=1)
    y = y.rename(columns={0: '応募数 合計'})
    
    return y