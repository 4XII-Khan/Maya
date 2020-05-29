import api_test.database as database
from collections import defaultdict
from api_test.fund_bills import FundBill
from api_test.person_bills import *
from api_test.common import *

import time
class Settlement:

    @staticmethod
    def fund_settlement_pre(only_session ,ten_sett_list = ''):
        """
        入账
        :return:
        """
        no_settlement_sessions = []
        if ten_sett_list == '':
            ten_sett_list = []
        else:
            ten_sett_list = ten_sett_list.split(',')

        if len(only_session) != 0:
            no_settlement_sessions.append(only_session)

        # 结算时间
        activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        for session in no_settlement_sessions:
            # 获取最近一次
            history_total = database.Search().total_income()
            # 总收入
            total_income = history_total["total_income"]
            # 总支出
            total_expenditure = history_total["total_expenditure"]
            # 结余
            remaining_funds = history_total["remaining_funds"]

            # 获取信号枪活动未结算的信息
            no_settlement_signalgun_activity = database.Search().get_no_settlement_signalgun_activity(session)
            signalgun = FundBill.session_signalgun_settlement(no_settlement_signalgun_activity, session)
            # 获取五连活动未结算的信息
            no_settlement_five_activity = database.Search().get_no_settlement_five_activity(session)
            five = FundBill.session_five_settlement(no_settlement_five_activity, session)

            if len(ten_sett_list) != 0:
                # 获取十连连活动未结算的信息 获取未结算的
                no_settlement_ten_activity = database.Search().get_no_settlement_ten_activity(ten_sett_list)
                ten = FundBill.session_ten_settlement(no_settlement_ten_activity, session)
                for user in ten_sett_list:
                    # 设置结算场次，根据这个场次来判断 该部门划入那个场次结算。
                    database.Update().settlement_ten_even_activity_last_session(session, user)


            else:
                ten = FundBill.settlement_base()

            period_income = signalgun["revenue"] + five["revenue"] + ten["revenue"]
            period_expenditure =  signalgun["expenditure"] + five["expenditure"] + ten["expenditure"]
            settlement_type = "{0},{1},{2}".format(signalgun["msg"], ten["msg"],five["msg"]).strip(',')

            settlement_account = {"sessions": session,
                                 "total_income": total_income + period_income,
                                 "total_expenditure": total_expenditure + period_expenditure,
                                 "remaining_funds": remaining_funds + period_income - period_expenditure,
                                 "current_period_income": period_income,
                                 "period_expenditure": period_expenditure,
                                 "settlement_type": settlement_type,
                                 "settlement_time": activation_time
                                 }


            database.Insert().financial_accounts(settlement_account)

    @staticmethod
    def fund_settlement(start_session = 0,ten_sett_list = ''):
        """
        入账
        :return:
        """
        if ten_sett_list == '':
            ten_sett_list = []
        else:
            ten_sett_list = ten_sett_list.split(',')

        if start_session == 0 :
            start_session = "{0}{1}".format(time.strftime('%Y%m%d', time.localtime(time.time())), 0)

        # 范围的场次
        no_settlement_sessions =  database.Search().greater_than_settlement_sessions(start_session)

        # 结算时间
        person_bill = defaultdict(list)
        for session in no_settlement_sessions:

            # 获取信号枪活动未结算的信息
            no_settlement_signalgun_activity = database.Search().get_no_settlement_signalgun_activity(session)
            signalgun_person = PersonBill.session_signalgun_settlement(no_settlement_signalgun_activity, session)
            for person, _signalgun in signalgun_person.items():
                for _ in _signalgun:
                    person_bill[person].append(_)

            # 获取五连活动未结算的信息
            no_settlement_five_activity = database.Search().get_no_settlement_five_activity(session)
            five_person = PersonBill.session_five_settlement(no_settlement_five_activity, session)
            for person, _five in five_person.items():
                for _ in _five:
                    person_bill[person].append(_)

            # 获取十连连活动未结算的信息
            if len(ten_sett_list) != 0 :
                # 获取十连连活动未结算的信息
                print(ten_sett_list,),len(ten_sett_list)
                no_settlement_ten_activity = database.Search().get_no_settlement_ten_activity_session(session,ten_sett_list)
                ten_person = PersonBill.session_ten_settlement(no_settlement_ten_activity, session)

                for person, _ten in ten_person.items():
                    for _ in _ten:
                        person_bill[person].append(_)

            # 更新五连活动 结算状态
            database.Update().settlement_five_even_activity(session)
            # 更新信号枪活动 结算状态
            database.Update().settlement_signal_gun_activity(session)
            # 更新十连活动 结算状态
            if len(ten_sett_list) != 0:
                database.Update().settlement_ten_even_activity(session)
            # 更新活动记录 结算状态
            database.Update().settlement_active_record(session)

        all_user_name = database.Search().get_users_name()
        for person, bill in person_bill.items():
            expenditure = sum([b['expenditure'] for b in bill ])
            revenue = sum([b['revenue'] for b in bill ])
            surplus = sum([b['surplus'] for b in bill ])
            print("玩家昵称：{0} ,本次结算总支出:{1} ,本次结算总收入:{2},本次结算净收入:{3}".format(all_user_name[person],expenditure,revenue,surplus))
            print("    【详情】:")
            for _ in  bill :

                log = "     活动名称:【{0}】, 场次:{1}, 本场支出{2}, 本场收入{3}, 本场净收入{4}".format(
                    _['msg'],_['session'],_['expenditure'],_['revenue'],_['surplus']
                )

                if _['surplus'] < 0 :
                    Common.incolorprint(log, 'yellow')
                if _['surplus'] > 0 :
                    Common.incolorprint(log, 'green')
