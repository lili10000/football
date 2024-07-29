import json
import fileUtil
import os




class dataItem:
    def __init__(self, homeScore=None, awayScore=None, o_home=None, o_stand=None, o_guest=None, y_goal=None, y_up=None, y_down=None, score_goal=None, score_upOdds=None, score_downOdds=None) -> None:
        self.homeScore = homeScore
        self.awayScore = awayScore
        self.o_home = o_home
        self.o_stand = o_stand
        self.o_guest = o_guest
        self.y_goal = y_goal
        self.y_up = y_up
        self.y_down = y_down
        self.score_goal = score_goal
        self.score_upOdds = score_upOdds
        self.score_downOdds = score_downOdds
    

def saveData(id):

    files = fileUtil.getFileList(id)
    itemList = []
    for file in files:
        with open(file, 'r',encoding='utf-8') as f:
            data = f.read()
            result=json.loads(data)
            dataList = result["data"]["list"]

            for data in dataList:
                item = dataItem()
                item.homeScore = data['homeScore']
                item.awayScore = data['awayScore']
                item.o_home = data["o_odds"]['o_home']
                item.o_stand = data["o_odds"]['o_stand']
                item.o_guest = data["o_odds"]['o_guest']
                item.y_goal = data["y_odds"]['y_goal']
                item.y_up = data["y_odds"]['y_up']
                item.y_down = data["y_odds"]['y_down']
                item.score_goal = data["total_score_odds"]['total_score_goal_r']
                item.score_upOdds = data["total_score_odds"]['total_score_upOdds_r']
                item.score_downOdds = data["total_score_odds"]['total_score_downOdds_r']
                itemList.append(item)


    path = os.path.dirname(__file__)
    file = "{}\\data\\{}.json".format(path, id)
    with open(file, 'w',encoding='utf-8') as f:
        str_data = json.dumps(itemList,ensure_ascii=False,default=lambda obj:obj.__dict__)
        f.write(str_data)
        print("write ", file, " ok")


if __name__ == "__main__":
    # saveData("36") # 英超
    saveData("2") # 阿甲
