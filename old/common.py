# encoding=utf8

class gameData:
    def __init__(self):    
        self.main = ''     
        self.client = ''  
        self.main_rank = 0  
        self.client_rank = 0  

        #历史战绩
        self.his_2_win = 0
        self.his_2_ping = 0
        self.his_2_lost = 0

        #主队近10场战绩
        self.his_main_all_win = 0
        self.his_main_all_ping = 0
        self.his_main_all_lost = 0
        self.his_main_all_score = 0
        self.his_main_all_score_lost = 0

        #客队近10场战绩
        self.his_client_all_win = 0
        self.his_client_all_ping = 0
        self.his_client_all_lost = 0
        self.his_client_all_score = 0
        self.his_client_all_score_lost = 0

        #主队近10场主场战绩
        self.his_main_1_win = 0
        self.his_main_1_ping = 0
        self.his_main_1_lost = 0
        self.his_main_1_score = 0
        self.his_main_1_score_lost = 0

        #客队近10场客场战绩
        self.his_client_1_win = 0
        self.his_client_1_ping = 0
        self.his_client_1_lost = 0
        self.his_client_1_score = 0
        self.his_client_1_score_lost = 0

        #近10场主队平均球数
        self.his_main_all_mean_score = 0
        self.his_main_main_socre = 0
        self.his_main_client_socre = 0
        self.his_main_all_mean_score_lost = 0
        self.his_main_main_socre_lost = 0
        self.his_main_client_socre_lost = 0

        #近10场客队平均球数
        self.his_client_all_mean_score = 0
        self.his_client_main_socre = 0
        self.his_client_client_socre = 0
        self.his_client_all_mean_score_lost = 0
        self.his_client_main_socre_lost = 0
        self.his_client_client_socre_lost = 0



        self.main_score = 0  
        self.client_score = 0   
        self.type = ''
        self.time = 0