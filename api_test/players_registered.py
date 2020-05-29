import api_test.database as database
import time
def signIn(user_name,user_Id = 0,total_sessions=0,total_expenses = 0,total_revenue=0,net_income=0,active_status="活跃",user_leve = 1):
    """
    # 表结构：用户iD  用户名、 游戏场次、总计支出、总计收入、净收入、活跃状态、用户级别、注册时间
    :param user_name:
    :param user_Id:
    :param total_sessions:
    :param total_expenses:
    :param total_revenue:
    :param net_income:
    :param active_status:
    :param user_leve:
    :return:
    """

    # TODO 写入用户注册表
    sign = {
        'user_name':user_name,
        'total_sessions':total_sessions,
        'user_Id':user_Id,
        'total_expenses': total_expenses,
        'total_revenue': total_revenue,
        'net_income': net_income,
        'active_status': active_status,
        'user_leve': user_leve,
        'registration_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    }

    database.Insert().basic_user_information(sign)


if __name__ == '__main__':
    pass
    # # 初始化数据库
    database.MainInit()
    # # 初始化用户
    signIn("惊雷",user_Id=1, total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=2)
    signIn("紫电",user_Id=2,total_sessions=0, total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=1)
    signIn("享自由",user_Id=3, total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=0)
    signIn("屠呦呦", user_Id=4,total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=0)
