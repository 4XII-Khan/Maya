import api_test.database as database
from collections import defaultdict
import time
class PersonBill:

    @staticmethod
    def settlement_base_person():
        """
        个人基本账单结构
        :return:
        """
        person =  {"session":'',"user_Id":'', "expenditure":0, "revenue":0, "surplus":0, "msg":""}
        return person


    @staticmethod
    def session_signalgun_settlement(no_settlement_signalgun_activity,session):
        """
        获取 信号枪活动 单场次结算数据
        :param no_settlement_signalgun_activity:
        :return:
        """


        signal_gun_person_bill = defaultdict(list)

        for settlement in no_settlement_signalgun_activity:
            signalgun = PersonBill.settlement_base_person()
            signalgun["session"] = session
            signalgun["msg"] = "信号枪活动"
            signalgun["user_Id"]= settlement["user_Id"]
            signalgun["expenditure"] = settlement["expenditure"]
            signalgun["revenue"] = settlement["revenue"]
            signalgun["surplus"] = settlement["surplus"]
            signal_gun_person_bill[settlement["user_Id"]].append(signalgun)

        return signal_gun_person_bill



    @staticmethod
    def session_five_settlement(no_settlement_five_activity,session):
        """
        五连活动
        :param no_settlement_five_activity:
        :return:
        """

        five_person_bill = defaultdict(list)


        if len(no_settlement_five_activity) == 0:
            return five_person_bill
        else:
            for settlement in no_settlement_five_activity:
                five = PersonBill.settlement_base_person()
                five["session"] = session
                five["msg"] = "五连活动"
                five_person_bill = defaultdict(list)

                five["expenditure"] = 0
                five["revenue"] = settlement["settlement_cost"]
                five["surplus"] = settlement["settlement_cost"]
                five["user_Id"] = settlement["user_Id"]

                five_person_bill[settlement["user_Id"]].append(five)
            return five_person_bill

    @staticmethod
    def session_ten_settlement(no_settlement_ten_activity, session):
        """
        获取 十连活动 单场次结算数据
        :param no_settlement_signalgun_activity:
        :return:
        """
        ten_person_bill = defaultdict(list)

        if len(no_settlement_ten_activity) == 0:
            return ten_person_bill
        else:
            for settlement in no_settlement_ten_activity:
                ten = PersonBill.settlement_base_person()
                ten["session"] = session
                ten["msg"] = "十连活动"
                ten["expenditure"] = settlement["renewal"]
                ten["revenue"] = 0
                ten["surplus"] = 0 - settlement["renewal"]

                ten["user_Id"] = settlement["user_Id"]
                ten_person_bill[settlement["user_Id"]].append(ten)
            return ten_person_bill






