import api_test.database as database
from collections import defaultdict
import time
class FundBill:
    @staticmethod
    def settlement_base():
        """
        基本账单结构
        :return:
        """
        financial = {"session": '', "expenditure": 0, "revenue": 0, "surplus": 0, "msg": ""}
        return  financial

    @staticmethod
    def settlement_base_person():
        """
        个人基本账单结构
        :return:
        """
        person =  {"session":'',"person":'', "expenditure":0, "revenue":0, "surplus":0, "msg":""}
        return person


    @staticmethod
    def session_signalgun_settlement(no_settlement_signalgun_activity,session):
        """
        获取 信号枪活动 单场次结算数据
        :param no_settlement_signalgun_activity:
        :return:
        """
        signalgun = FundBill.settlement_base()
        signalgun["session"] = session
        signalgun["msg"] = "信号枪活动"

        signal_gun = defaultdict(list)
        for settlement in no_settlement_signalgun_activity:
            # 个人收入 == 基金支出
            signal_gun["expenditure"].append(settlement["revenue"])
            signal_gun["revenue"].append(settlement["expenditure"])
            signal_gun["surplus"].append(settlement["expenditure"] - settlement["revenue"] )

        for type, settlements in signal_gun.items():
            signalgun[type] = sum(settlements)

        return signalgun



    @staticmethod
    def session_five_settlement(no_settlement_five_activity,session):
        """
        五连活动
        :param no_settlement_five_activity:
        :return:
        """
        five = FundBill.settlement_base()
        five["session"] = session

        if len(no_settlement_five_activity) == 0:
            return five
        else:
            five["msg"] = "五连活动"
            five["expenditure"] = no_settlement_five_activity[0]["settlement_cost"]
            five["revenue"] = 0
            five["surplus"] = 0 - no_settlement_five_activity[0]["settlement_cost"]
            return five


    @staticmethod
    def session_ten_settlement(no_settlement_ten_activity, session):
        """
        获取 十连活动 单场次结算数据
        :param no_settlement_signalgun_activity:
        :return:
        """
        ten = FundBill.settlement_base()
        ten["session"] = session

        if len(no_settlement_ten_activity) == 0:
            return ten
        else:
            ten_tmp = defaultdict(list)
            ten["msg"] = "十连活动"
            for settlement in no_settlement_ten_activity:
                ten_tmp["revenue"].append(settlement["renewal"])
                ten_tmp["surplus"].append(settlement["renewal"])

            for type, settlements in ten_tmp.items():
                ten[type] = sum(settlements)
            return ten

