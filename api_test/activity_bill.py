from api_test.activity_utils import *
import math
class Activity:

    @staticmethod
    def activity_entry(join_user_ids ,flare_gun_user_Ids, session):
        """
        活动入口
        :param json_user_Ids: 参赛玩家
        :param flare_gun_user_Ids: 信号枪玩家
        :param session: 场次
        :return:
        """
        # 所有注册用户
        all_user_id = database.Search().user_Id()
        # 未参与用户
        no_join_ids = [id for id in all_user_id if id not in (join_user_ids + flare_gun_user_Ids)]
        # 场次
        if session < 10:
            session = "0{0}".format(session)
        session = "{0}{1}".format(time.strftime('%Y%m%d', time.localtime(time.time())), session)

        return join_user_ids, no_join_ids, flare_gun_user_Ids, session

    @staticmethod
    def signal_gun_activity(json_user_Ids ,no_join_ids,flare_gun_user_Ids, session):
        """
        信号枪活动规则
        :param json_user_Ids:
        :param flare_gun_user_Ids:
        :param session:
        :return:
        """
        # 表结构：场次 用户ID 支出 收入 结算状态 创建时间
        # todo 根据创建时间+结算状态 进行批量结算

        # 参赛时间
        activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        # 本期收入
        current_period_income = 0
        # 本期支出
        period_expenditure = 0

        bills = {"sessions": session,
                 "settlement_status": "未结算",
                 "creation_time": activation_time}

        for json_user_Id in json_user_Ids:
            # 获取信号枪的玩家 后面单独计算
            if json_user_Id not in flare_gun_user_Ids:
                user_leve = database.Search().user_leve(json_user_Id)
                # 投币
                if user_leve == 0:
                    expenditure = 1
                else:
                    expenditure = user_leve
                bills["expenditure"] = expenditure
                bills["user_Id"] = json_user_Id
                bills["revenue"] = 0
                bills["surplus"] = 0 - expenditure

                activation_record(json_user_Id, session)
                # 写入活动记录
                database.Insert().signal_gun_activity(bills)
                # 投币
                current_period_income = current_period_income + expenditure

        for flare_gun_user_Id in flare_gun_user_Ids:
            # 避免重复加钱 兜底
            if flare_gun_user_Id not in json_user_Ids:
                user_leve = database.Search().user_leve(flare_gun_user_Id)
                # 投币
                if user_leve == 0:
                    expenditure = 1
                else:
                    expenditure = user_leve
                # 投币
                current_period_income = current_period_income + expenditure

        # 激励占比，后续表中取
        incentive = {0:0.5, 1:0.55, 2:0.6}

        for flare_gun_user_Id in flare_gun_user_Ids:
            # 获取总收入
            history_total = database.Search().total_income()
            # 结余
            remaining_funds = history_total["remaining_funds"]
            user_leve = database.Search().user_leve(flare_gun_user_Id)
            # 投币
            if user_leve == 0:
                expenditure = 1
            else:
                expenditure = user_leve
            # 激励
            print((remaining_funds + current_period_income ), incentive[user_leve],len(flare_gun_user_Ids))
            revenue = float((remaining_funds + current_period_income ) * incentive[user_leve])/len(flare_gun_user_Ids)
            revenue = int(revenue+0.5)

            bills["expenditure"] = expenditure
            bills["user_Id"] = flare_gun_user_Id
            bills["revenue"] = revenue
            bills["surplus"] = revenue - expenditure
            # period_expenditure = period_expenditure + revenue

            activation_record(flare_gun_user_Id, session,flareGun = "获取空投枪")

            database.Insert().signal_gun_activity(bills)

        # 没有参加的用户
        for user_id in no_join_ids:
            activation_record(user_id, session, "未参赛")

    @staticmethod
    def five_even_activity():
        """
        五连活动
        连续5次没有捡到空投抽取10%
        :return:
        """
        # 获取五连活动最后一场
        end_session = database.Search().end_session()

        # 拉取 signal_gun_activity 每个场次的用户收入情况
        continuously_list = database.Search().get_session_revenue(end_session)

        activation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        history_total = database.Search().total_income()
        # 结余
        remaining_funds = history_total["remaining_funds"]

        for continuously in continuously_list:
            # 此处固定user_Id == 1
            continuously["user_Id"] = 1
            continuously["time"] = activation_time
            continuously["settlement_session"] = continuously["end_session"]
            continuously["settlement_status"] ="未结算"
            continuously["settlement_cost"] = int(remaining_funds * 0.1 + 0.5)
            # 小于 0 没意义
            if int(remaining_funds * 0.1 + 0.5) < 1:
                continuously["settlement_cost"] = 1

            database.Insert().five_even_activity(continuously)

    @staticmethod
    def ten_even_activity(json_user_Ids ,no_join_ids, session):
        """
        十连活动，超过十次不参加，则自动退出，
        # 表结构：用户iD  间断次数  续费补交  最后一次参加场次 ，超过十次 活跃状态置为不活跃

        :param join_status:
        :param uninterrupted:
        :return:
        """
        # todo 每次参加置为 0 ，不参加增加 1 ，超过 10 次 需计算续费补交，未超过补交为0
        uninterrupted = {"renewal": 0,
                         "discontinuous_number": 0,
                         "last_session": session,
                         "settlement_status":"未结算",
                         "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}

        for user_id in no_join_ids:
            uninterrupted["user_Id"] = user_id
            discontinuous_number = database.Search().discontinuous_number(uninterrupted["user_Id"])
            discontinuous_number = discontinuous_number + 1
            uninterrupted["discontinuous_number"] = discontinuous_number

            # discontinuous_number 大于10 用户置为不活跃
            if discontinuous_number >= 10:
                # 更新 会员注册表的会员状态
                database.Update().active_status(uninterrupted["user_Id"],'不活跃')
                history_total = database.Search().total_income()
                # 结余
                remaining_funds = history_total["remaining_funds"]
                # 获取活跃用户
                active_user_ids = database.Search().active_user_Id()
                # 激活费用 当前活跃用户+1
                activation_fee = remaining_funds/(len(active_user_ids) + 1)
                # 向上取整
                activation_fee = int(activation_fee + 0.5)
                # 小于 0 没意义
                if int(remaining_funds * 0.1 + 0.5) < 1:
                    activation_fee = 1

                uninterrupted["renewal"] = activation_fee

            database.Insert().ten_even_activity(uninterrupted)

        for user_id in json_user_Ids:
            no_settlement_ten_activity_user = database.Search().get_no_settlement_ten_activity_user()
            if user_id in  no_settlement_ten_activity_user:
                discontinuous_number = database.Search().discontinuous_number(user_id)
                uninterrupted["discontinuous_number"] = discontinuous_number + 1
                history_total = database.Search().total_income()
                # 结余
                remaining_funds = history_total["remaining_funds"]
                # 获取活跃用户
                active_user_ids = database.Search().active_user_Id()
                # 激活费用 当前活跃用户+1
                activation_fee = remaining_funds / (len(active_user_ids) + 1)
                # 向上取整
                activation_fee = int(activation_fee + 0.5)
                # 小于 0 没意义
                if int(remaining_funds * 0.1 + 0.5) < 1:
                    activation_fee = 1
                uninterrupted["renewal"] = activation_fee
            else:
                uninterrupted["discontinuous_number"] = 0
                uninterrupted["renewal"] = 0
            uninterrupted["user_Id"] = user_id

            database.Insert().ten_even_activity(uninterrupted)
            # discontinuous_number 小于10 用户置为活跃
            database.Update().active_status(uninterrupted["user_Id"])


if __name__ == "__main__":
    pass
