import api_test.database as database
import time

def activation_record(user_Id, session, join_status = "已参赛", flareGun = "未获取空投枪"):
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
    activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    record = {"user_Id":user_Id,
              "sessions":session,
              "flare_gun": flareGun,
              "settlement_status": "未结算",
              "time": activation_time,
              "join_status":join_status
              }
    database.Insert().active_record(record)


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
