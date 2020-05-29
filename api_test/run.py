
from api_test.activity_bill  import *
from api_test.settlement  import *
from api_test.players_registered import *
def activity_create(join_user_ids ,flare_gun_user_Ids, session,ten_sett_list = ''):
    join_user_ids, no_join_ids, flare_gun_user_Ids, session = Activity.activity_entry(join_user_ids ,flare_gun_user_Ids, session)
    # 信号
    Activity.signal_gun_activity(join_user_ids, no_join_ids, flare_gun_user_Ids, session)
    # 十连
    Activity.ten_even_activity(join_user_ids, no_join_ids, session)
    # 五连
    Activity.five_even_activity()

    # 资金账单
    Settlement.fund_settlement_pre(session, ten_sett_list)

    return session

def settlement():
    Settlement.fund_settlement()

if __name__ == '__main__':

    # # 初始化数据库
    database.MainInit()
    # 初始化用户
    signIn("惊雷",user_Id=1, total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=2)
    signIn("紫电",user_Id=2,total_sessions=0, total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=1)
    signIn("享自由",user_Id=3, total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=0)
    signIn("屠呦呦", user_Id=4,total_sessions=0,total_expenses=0, total_revenue=0, net_income=0, active_status="活跃", user_leve=0)


    for i in  range(1,10):
        print(i)
        join_user_ids = [1,2,3]
        flare_gun_user_Ids = []
        session = i
        format_session = activity_create(join_user_ids ,flare_gun_user_Ids, session)
    activity_create([1, 2, 3],  [1], 10, '4')

    Settlement.fund_settlement(ten_sett_list='4')
