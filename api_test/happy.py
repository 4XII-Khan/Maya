#!/usr/bin/env python
# coding: utf-8

import api_test.database as database
import time
import math




def activation_record(user_Id, session,join_status = "已参加", flareGun = "未获取空投枪"):
    """
    活动记录
    :param user_Id:
    :param session:
    :param join_status:
    :param flareGun:
    :return:
    """

    # 表结构：场次  用户iD  信号  结算状态  时间
    # TODO 写入记录表 需判断是否需要续费
    sessions = "{0}{1}".format(time.strftime('%Y%m%d', time.localtime(time.time())), session)
    activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    record = {"user_Id":user_Id,
              "sessions":sessions,
              "flare_gun": flareGun,
              "settlement_status": "未结算",
              "time": activation_time,
              "join_status":join_status
              }
    database.Insert().active_record(record)

    uninterrupted = {"user_Id":user_Id,
                     "renewal":0,
                     "last_session":sessions,
                     "time":activation_time}

    uninterrupted_Record(join_status,uninterrupted)



# 间断记录，超过十次不参加，则自动退出，
def uninterrupted_Record(join_status, uninterrupted):
    """
    间断记录，超过十次不参加，则自动退出，
    # 表结构：用户iD  间断次数  续费补交  最后一次参加场次 ，超过十次 活跃状态置为不活跃

    :param join_status:
    :param uninterrupted:
    :return:
    """
    # todo 每次参加置为 0 ，不参加增加 1 ，超过 10 次 需计算续费补交，未超过补交为0
    if join_status == "未参加":
        discontinuous_number = database.Search().discontinuous_number(uninterrupted["user_Id"])
        discontinuous_number = discontinuous_number + 1
        uninterrupted["discontinuous_number"] = discontinuous_number
        # 写入间断次数
        database.Insert().ten_even_activities(uninterrupted)
        # discontinuous_number 大于10 用户置为不活跃
        if discontinuous_number >= 10:
            database.Update().active_status(uninterrupted["user_Id"],'不活跃')


    else:
        uninterrupted["discontinuous_number"] = 0

        database.Insert().ten_even_activities(uninterrupted)
        # discontinuous_number 小于10 用户置为活跃
        database.Update().active_status(uninterrupted["user_Id"])


def ten_even_activities(user_Id):
    """
    续费记录 中断后需续费补足奖池 10%金额 方可继续参加
    :param user_Id:
    :return:
    """
    last_session = database.Search().last_session(user_Id)

    uninterrupted = {"user_Id":user_Id,
                     "renewal":0,
                     "discontinuous_number":0,
                     "last_session":last_session,
                     "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}

    database.Insert().ten_even_activities(uninterrupted)

    # todo 间断记录表的间断次数置为 0，补交金额置为 0，用户基本信息中活跃状态置为活跃，财务账目注入资金增加10，视为一次财务结算
    pass

def personalBills(json_user_Ids ,flare_gun_user_Ids, session):
    """
    个人账单
    :param json_user_Ids:
    :param flare_gun_user_Ids:
    :param session:
    :return:
    """
    # 表结构：场次 用户ID 支出 收入 结算状态 创建时间
    # todo 根据创建时间+结算状态 进行批量结算
    history_total = database.Search().total_income()
    all_user_id = database.Search().user_Id()

    sessions = "{0}{1}".format(time.strftime('%Y%m%d', time.localtime(time.time())), session)
    activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 总收入
    total_income = history_total["total_income"]
    # 总支出
    total_expenditure =  history_total["total_expenditure"]
    # 结余
    remaining_funds =  history_total["remaining_funds"]
    # 本期收入
    current_period_income = 0
    # 本期支出
    period_expenditure = 0

    bills = {"sessions": sessions,
             "settlement_status": "未结算",
             "creation_time": activation_time}

    for json_user_Id in json_user_Ids:
        user_leve = database.Search().user_leve(json_user_Id)
        bills["expenditure"] = user_leve
        bills["user_Id"] = json_user_Id
        bills["revenue"] = 0
        bills["surplus"] = 0 - user_leve
        activation_record(json_user_Id, session)
        database.Insert().signal_gun_activity(bills)
        # 投币
        current_period_income = current_period_income + user_leve
        all_user_id.remove(json_user_Id)

    for flare_gun_user_Id in flare_gun_user_Ids:
        # 避免重复加钱 兜底
        if flare_gun_user_Id not in json_user_Ids:
            user_leve = database.Search().user_leve(flare_gun_user_Id)
            # 投币
            current_period_income = current_period_income + user_leve

    for flare_gun_user_Id in flare_gun_user_Ids:
        revenue = (remaining_funds + current_period_income) / (2 * len(flare_gun_user_Ids))
        revenue = math.floor(revenue)
        user_leve = database.Search().user_leve(flare_gun_user_Id)

        bills["expenditure"] = user_leve
        bills["user_Id"] = flare_gun_user_Id
        bills["revenue"] = revenue
        bills["surplus"] = revenue - user_leve
        period_expenditure = period_expenditure + revenue



        activation_record(flare_gun_user_Id, session,flareGun = "获取空投枪")
        if flare_gun_user_Id in all_user_id:
            all_user_id.remove(flare_gun_user_Id)
        print(all_user_id,flare_gun_user_Id)
        database.Insert().signal_gun_activity(bills)

    # 没有参加的用户
    for user_id in all_user_id:
        activation_record(user_id, session, "未参加")

    # 本期后的资金结余
    remaining_funds = remaining_funds + current_period_income - period_expenditure

    financial_account = {"sessions":sessions,
                         "total_income":total_income + current_period_income,
                         "total_expenditure":total_expenditure + period_expenditure,
                         "remaining_funds":remaining_funds,
                         "current_period_income":current_period_income,
                         "period_expenditure":period_expenditure,
                         "settlement_type": "活动结算",
                         "settlement_time": activation_time
                         }
    financialAccount(financial_account)

# 财务账目
def financialAccount(financial_account):
   # 表结构：场次、盈余资金、结算资金、本期支出，本期收入、结余资金、结算类型（间断补费、活动结算）、时间
   # todo 每次结算完计算出当前
   database.Insert().financial_accounts(financial_account)

def user_settlement():
    """
    用户结算，更新用户基本信息表
    :return:
    """
    user_id_name, expenditure, revenue, surplus = database.Search().user_expenses_revenue_income()
    for user_Id,user_expenditure in expenditure.items():
        total_sessions = len(user_expenditure)
        user_revenue = sum(revenue[user_Id])
        user_surplus = sum(surplus[user_Id])

        database.Update().basic_user_information(user_Id, total_sessions, sum(user_expenditure), user_revenue, user_surplus)

def five_even_activity():
    """
    五连活动 连续5次没有捡到空投抽取10%
    :return:
    """
    end_session = database.Search().end_session()
    continuously_list = database.Search().financial_accounts(end_session)
    activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    history_total = database.Search().total_income()
    # 结余
    remaining_funds = history_total["remaining_funds"]

    for continuously in continuously_list:

        continuously["time"] = activation_time
        continuously["settlement_session"] = continuously["end_session"]
        continuously["settlement_status"] ="未结算"
        continuously["settlement_cost"] = remaining_funds* 0.1

        database.Insert().five_even_activity(continuously)

def settlement_five_even_activity(user_Id = 1,settlement_cost = 0):
    """
    结算连续5次未捡到空投
    1.用户信息 +
    3.个人账单
    2.资金账单 -
    4.连续未捡到
    :return:
    """
    #
    # settlement_cost = database.Search().uncleared_continuous_airdrop()

    # 更新 five_even_activity 表
    database.Update().clearing_continuous_airdrop()

    history_total = database.Search().total_income()

    # 总收入
    total_income = history_total["total_income"]
    # 总支出
    total_expenditure = history_total["total_expenditure"]
    # 结余
    remaining_funds = history_total["remaining_funds"]

    sessions = "{0}{1}".format(time.strftime('%Y%m%d', time.localtime(time.time())), 0)
    activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    bills = {"sessions": sessions,
             "settlement_status": "未结算",
             "creation_time": activation_time,
             "expenditure":0,
             "user_Id": user_Id,
             "revenue": settlement_cost,
             "surplus": settlement_cost}
    print( total_expenditure , settlement_cost)
    financial_account = {"sessions": sessions,
                         "total_income": total_income ,
                         "total_expenditure": total_expenditure + settlement_cost,
                         "remaining_funds": remaining_funds - settlement_cost,
                         "current_period_income": 0,
                         "period_expenditure": settlement_cost,
                         "settlement_type": "连续五局未捡空投",
                         "settlement_time": activation_time
                         }
    financialAccount(financial_account)

    database.Insert().signal_gun_activity(bills)

# 结算
def settlement(user_Id = 999, settlement_type = "活动结算",payment_coefficient = 0.1):
    # todo 根据结算类型（间断补费、活动结算）进行结算，输出时间范围内的每个用户的支出和收入总和，进行结算。
    history_total = database.Search().total_income()
    #  连续5次没有捡到空投抽取10%
    five_even_activity()
    settlement_cost = database.Search().uncleared_continuous_airdrop()

    if settlement_cost != 0:
        settlement_five_even_activity(settlement_cost = settlement_cost)

    # 结余
    remaining_funds = history_total["remaining_funds"]
    payment = remaining_funds * payment_coefficient
    if settlement_type == "活动结算":
        settlement, user_id_name, detail = database.Search().surplus()

        for user_id, amount in settlement.items():
            print("用户名:{0}  结算金额:{1}元".format(user_id_name[user_id],amount))
            # for no_settlement in detail[user_id]:
            #     print("   用户名:{0} 场次:{1} 参赛日期:{2} 本场收支:{3}元".format(user_id_name[user_id], no_settlement[3], no_settlement[4], no_settlement[2]))
            # print()
        # 结算
        database.Update().signal_gun_activity()

        discontinuous_user_Id = database.Search().settlement_discontinuous_number()


        for user_id in discontinuous_user_Id:
            database.Update().ten_even_activities(payment, user_id)
            print("用户名:{0}  补缴金额:{1}元".format(user_id_name[user_id],payment))



    elif settlement_type == "间断补费" :
        activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        database.Update().continuous_payment(activation_time, user_Id)
        sessions = "{0}{1}".format(time.strftime('%Y%m%d', time.localtime(time.time())), 0)
        # 总收入
        total_income = history_total["total_income"]
        # 总支出
        total_expenditure = history_total["total_expenditure"]
        # 结余
        remaining_funds = history_total["remaining_funds"]

        financial_account = {"sessions": sessions,
                             "total_income": total_income + payment,
                             "total_expenditure": total_expenditure,
                             "remaining_funds": remaining_funds + payment,
                             "current_period_income": payment,
                             "period_expenditure": 0,
                             "settlement_type": "间断补费",
                             "settlement_time": activation_time
                             }
        financialAccount(financial_account)

        # 补费后 用户置为活跃
        database.Update().active_status(user_Id)

    # 用户结算
    user_settlement()

if __name__ == '__main__':
    pass
    # # 初始化数据库
    # database.MainInit()
    # # 初始化用户
    # signIn("惊雷",user_Id=1, total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=2)
    # signIn("屠呦呦", user_Id=4,total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=1)
    # signIn("享自由",user_Id=3, total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=1)
    # signIn("紫电",user_Id=2,total_sessions=0, total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=1)

    # for i in range(23,30):
    # #
    personalBills([1,2,3], [], 1)
    #
    personalBills([1,2,3], [3], 2)
    #
    personalBills([1,2,3], [2,3], 3)
    #
    # # 结算
    settlement()


    # settlement(user_Id=4, settlement_type="间断补费")

    # renewRecord(4)

