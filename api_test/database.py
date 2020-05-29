#!/usr/bin/env python
# coding: utf-8
# @Time     : 2018/8/28 17:14
# @Author   : 你的名字啊！！！
# @FileName : LocustTestLibrary .py
# @Project  : YJiang

import datetime
import inspect
import sqlite3

import api_test.common as common

from collections import defaultdict

class Search:
    def __init__(self):

        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')

    def user_Id(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id from basic_user_information "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        all_user_Id = []
        for line in result:
            all_user_Id.append(line[0])
        cursor.close()
        connect.close()
        return all_user_Id

    def active_user_Id(self):
        """
        获取活跃用户
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id from basic_user_information where active_status = '活跃' "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        active_user_Id = []
        for line in result:
            active_user_Id.append(line[0])
        cursor.close()
        connect.close()
        return active_user_Id
    def discontinuous_number(self,user_Id):

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select discontinuous_number  from ten_even_activity where user_Id = {0}".format(user_Id)

        select = cursor.execute(search_sql)
        result = select.fetchone()
        if result == None:
            discontinuous_number = 0
        else:
            discontinuous_number = result[0]

        cursor.close()
        connect.close()
        return discontinuous_number

    def last_session(self,user_Id):

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select last_session  from ten_even_activity where user_Id = {0}".format(user_Id)

        select = cursor.execute(search_sql)
        session = select.fetchone()[0]

        cursor.close()
        connect.close()
        return session


    def user_leve(self,user_Id):

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select user_leve  from basic_user_information where user_Id = {0}".format(user_Id)

        select = cursor.execute(search_sql)
        user_leve = select.fetchone()[0]

        cursor.close()
        connect.close()
        return user_leve

    def total_income(self):

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select total_income,total_expenditure,remaining_funds  from financial_accounts order by sessions desc limit 1 "

        select = cursor.execute(search_sql)
        history = select.fetchone()
        if history == None:
            history_total = {"total_income": 0, "total_expenditure":0, "remaining_funds": 0}
        else:
            history_total = {"total_income":history[0],"total_expenditure":history[1],"remaining_funds":history[2]}

        cursor.close()
        connect.close()
        return history_total

    def surplus(self):

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select a.user_Id, b.user_name, sum(a.surplus) from signal_gun_activity as a, basic_user_information as  b where a.settlement_status= '未结算' and a.user_Id = b.user_Id  group by a.user_Id"
        select = cursor.execute(search_sql)
        history_no_settlement = select.fetchall()
        detail = defaultdict(list)
        settlement = defaultdict(int)
        user_id_name = {}
        if history_no_settlement == []:
            pass
        else:
            for no_settlement in  history_no_settlement:
                user_id_name[no_settlement[0]] = no_settlement[1]
                settlement[no_settlement[0]] = no_settlement[2]
                detail[no_settlement[0]].append(list(no_settlement))

        cursor.close()
        connect.close()
        return settlement,user_id_name,detail

    def user_expenses_revenue_income(self):

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()



        search_sql = "select a.user_Id, b.user_name, a.expenditure,a.revenue ,a.surplus from signal_gun_activity as a, basic_user_information as  b where a.settlement_status= '已结算' and a.user_Id = b.user_Id  group by a.user_Id,a.sessions"

        select = cursor.execute(search_sql)
        history_no_settlement = select.fetchall()

        expenditure = defaultdict(list)
        revenue = defaultdict(list)
        surplus = defaultdict(list)

        user_id_name = {}

        if history_no_settlement == []:
            pass
        else:
            for no_settlement in  history_no_settlement:
                user_id_name[no_settlement[0]] = no_settlement[1]
                expenditure[no_settlement[0]].append(no_settlement[2])
                revenue[no_settlement[0]].append(no_settlement[3])
                surplus[no_settlement[0]].append(no_settlement[4])
        cursor.close()
        connect.close()
        return user_id_name,expenditure,revenue,surplus

    def settlement_discontinuous_number(self):
        """
        查询连续超过十次未参加的用户
        :return:
        """

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select user_Id from ten_even_activity where discontinuous_number >= 10"

        select = cursor.execute(search_sql)
        result = select.fetchall()
        discontinuous_user_Id = []
        for line in result:
            discontinuous_user_Id.append(line[0])
        cursor.close()
        connect.close()
        return discontinuous_user_Id

    def end_session(self):
        """
        获取最后的一次场次
        :return:
        """

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select max(end_session) from five_even_activity "

        select = cursor.execute(search_sql)
        end_session = select.fetchone()[0]
        if end_session == None:
            end_session = 0
        cursor.close()
        connect.close()
        return end_session


    def get_session_revenue(self,end_session = 0):
        """
        查询连续五次没有捡到空投
        :return:
        """

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        search_sql = "SELECT sessions, sum(revenue) from signal_gun_activity where sessions > {0}   group by sessions  order by sessions  ".format(end_session)
        select = cursor.execute(search_sql)
        result = select.fetchall()

        sessions_period_expenditure = {}
        for line in result:
            sessions_period_expenditure[line[0]] =line[1]
        cursor.close()
        connect.close()

        # 连续次数
        continuously = 0
        continuously_list = []
        last = True
        if len(result) != 0:
            start_session = result[0][0]
        else:
            return continuously_list
        for sessions, period_expenditure in sessions_period_expenditure.items():
            # 上一个是否是结算场次
            if int(period_expenditure) == 0 and last:
                continuously = continuously +1

            elif int(period_expenditure) == 0 and not last:
                continuously = continuously +1
                start_session = sessions
                last = True
            else:
                continuously = 0
                start_session = sessions

            if continuously == 5:
                continuously_five = {}
                continuously_five["start_session"] = start_session
                continuously_five["end_session"] = sessions

                continuously = 0
                last = False

                continuously_list.append(continuously_five)

        return continuously_list

    def uncleared_continuous_airdrop(self):
        """
        获取未结算的 连续5次未获取空投
        :return:
        """

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "select sum(settlement_cost) from five_even_activity where settlement_status = '未结算';"

        select = cursor.execute(search_sql)
        settlement_cost = select.fetchone()[0]
        if settlement_cost ==None:
            settlement_cost = 0
        cursor.close()
        connect.close()
        return settlement_cost

    def select_signal_gun_activity(self):
        """
        获取未结算的 连续5次未获取空投
        :return:
        """

        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        # search_sql = "select *  from signal_gun_activity order by sessions desc ;"
        search_sql = "select a.user_Id, a.sessions ,a.expenditure, a.revenue ,a.surplus,a.settlement_status,a.creation_time,b.user_name from signal_gun_activity as a, basic_user_information as  b where a.user_Id = b.user_Id  order by a.sessions desc"

        select = cursor.execute(search_sql)
        all_records = select.fetchall()
        all_records_list = []
        for record in all_records:
            records_dict = {}

            records_dict['user_Id'] = record[0]
            records_dict['sessions'] = record[1]
            records_dict['expenditure'] = record[2]
            records_dict['revenue'] = record[3]
            records_dict['surplus'] = record[4]
            records_dict['settlement_status'] = record[5]
            records_dict['creation_time'] = record[6]
            records_dict['user_name'] = record[7]
            print(records_dict)
            all_records_list.append(records_dict)
        cursor.close()
        connect.close()
        return all_records_list

    def get_users_name(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id, user_name from basic_user_information order by user_Id "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        all_user_name = {}
        for line in result:
            all_user_name[line[0]] = line[1]
        cursor.close()
        connect.close()
        return all_user_name

    def get_users(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT * from basic_user_information order by user_Id "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        user_leve = {0:"普通用户",1:"白银会员", 2:"黄金会员", 3:"铂金会员",}
        all_user_Id = []
        for line in result:
            tmp = {}
            tmp["user_Id"] = line[0]
            tmp["user_name"] = line[1]
            tmp["total_sessions"] = line[2]
            tmp["total_expenses"] = line[3]
            tmp["total_revenue"] = line[4]
            tmp["net_income"] = line[5]
            tmp["active_status"] = line[6]
            tmp["user_leve"] = user_leve[line[7]]
            tmp["registration_time"] = line[8]


            all_user_Id.append(tmp)
        cursor.close()
        connect.close()
        return all_user_Id

    def get_financial_accounts(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT * from financial_accounts order by sessions desc "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        financial_accounts = []
        for line in result:
            tmp = {}
            tmp["sessions"] = line[0]
            tmp["total_income"] = line[1]
            tmp["total_expenditure"] = line[2]
            tmp["remaining_funds"] = line[3]
            tmp["current_period_income"] = line[4]
            tmp["period_expenditure"] = line[5]
            tmp["settlement_type"] = line[6]
            tmp["settlement_time"] = line[7]
            financial_accounts.append(tmp)
        cursor.close()
        connect.close()
        return financial_accounts



    def get_five_even_activity(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT * from five_even_activity order by settlement_session desc "

        select = cursor.execute(search_sql)
        result = select.fetchall()
        not_pick = []
        for line in result:
            tmp = {}
            tmp["user_Id"] = line[0]
            tmp["settlement_session"] = line[1]
            tmp["start_session"] = line[2]
            tmp["end_session"] = line[3]
            tmp["settlement_cost"] = line[4]
            tmp["settlement_status"] = line[5]
            tmp["time"] = line[6]
            not_pick.append(tmp)

        cursor.close()
        connect.close()
        return not_pick

    def get_ten_even_activity(self):
        """
        获取人员主题结构并排序,目前现场主题库表结构暂未确定，目前只统计涉及输出的字段。
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT * from ten_even_activity order by last_session desc "
        user_name = Search().get_users_name()
        select = cursor.execute(search_sql)
        result = select.fetchall()
        not_join = []
        for line in result:
            tmp = {}
            tmp["user_name"] = user_name[line[0]]
            tmp["discontinuous_number"] = line[1]
            tmp["renewal"] = line[2]
            tmp["last_session"] = line[3]
            tmp["time"] = line[4]

            not_join.append(tmp)
        cursor.close()
        connect.close()
        return not_join

    def greater_than_settlement_sessions(self, sessions):
        """
        获取未结算的场次
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT distinct sessions from active_record where sessions > {0} order by sessions ".format(sessions)
        no_settlement_sessions = []
        select = cursor.execute(search_sql)
        result = select.fetchall()
        for session in result:
            no_settlement_sessions.append(session[0])
        cursor.close()
        connect.close()
        return no_settlement_sessions

    def get_no_settlement_signalgun_activity(self, session):
        """
        获取未结算的信号枪活动
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id, sessions, expenditure,revenue, surplus from signal_gun_activity where sessions ='{0}' order by sessions ".format(session)

        no_settlement_signalgun_activity = []
        select = cursor.execute(search_sql)
        result = select.fetchall()

        for signalgun_activity in result:
            tmp = {}
            tmp["user_Id"] = signalgun_activity[0]
            tmp["sessions"] = signalgun_activity[1]
            tmp["expenditure"] = signalgun_activity[2]
            tmp["revenue"] = signalgun_activity[3]
            tmp["surplus"] = signalgun_activity[4]

            no_settlement_signalgun_activity.append(tmp)

        cursor.close()
        connect.close()
        return no_settlement_signalgun_activity


    def get_no_settlement_five_activity(self, session):
        """
        获取未结算的五连活动
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id, settlement_session, start_session, end_session,settlement_cost from five_even_activity where settlement_session ='{0}' order by settlement_session ".format(
            session)

        no_settlement_five_activity = []
        select = cursor.execute(search_sql)
        result = select.fetchall()
        for five_activity in result:
            tmp = {}
            tmp["user_Id"] = five_activity[0]
            tmp["settlement_session"] = five_activity[1]
            tmp["start_session"] = five_activity[2]
            tmp["end_session"] = five_activity[3]
            tmp["settlement_cost"] = five_activity[4]

            no_settlement_five_activity.append(tmp)
        cursor.close()
        connect.close()
        return no_settlement_five_activity

    def get_no_settlement_ten_activity(self, ten_sett_list):
        """
        获取未结算的五连活动
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        print(ten_sett_list)
        ten_sett_list = [str(u) for u in ten_sett_list]
        print(','.join(ten_sett_list))
        search_sql = "SELECT user_Id, discontinuous_number, renewal, last_session from ten_even_activity where settlement_status ='未结算' and user_Id in ('{0}') order by last_session ".format(','.join(ten_sett_list))
        print(search_sql)
        no_settlement_ten_activity = []
        select = cursor.execute(search_sql)
        result = select.fetchall()
        for ten_activity in result:
            tmp = {}
            tmp["user_Id"] = ten_activity[0]
            tmp["discontinuous_number"] = ten_activity[1]
            tmp["renewal"] = ten_activity[2]
            tmp["last_session"] = ten_activity[3]

            no_settlement_ten_activity.append(tmp)
        print(no_settlement_ten_activity)
        cursor.close()
        connect.close()
        return no_settlement_ten_activity

    def get_no_settlement_ten_activity_session(self, last_session,ten_sett_list):
        """
        获取未结算的五连活动
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        ten_sett_list = [str(u) for u in ten_sett_list]
        search_sql = "SELECT user_Id, discontinuous_number, renewal, last_session from ten_even_activity where settlement_status ='未结算' and renewal > 0 and last_session = {0}  and user_Id in ('{1}')  order by last_session ".format(last_session,','.join(ten_sett_list))
        no_settlement_ten_activity = []
        select = cursor.execute(search_sql)
        result = select.fetchall()
        for ten_activity in result:
            tmp = {}
            tmp["user_Id"] = ten_activity[0]
            tmp["discontinuous_number"] = ten_activity[1]
            tmp["renewal"] = ten_activity[2]
            tmp["last_session"] = ten_activity[3]

            no_settlement_ten_activity.append(tmp)
        cursor.close()
        connect.close()
        return no_settlement_ten_activity



    def get_no_settlement_ten_activity_user(self):
        """
        获取未结算的十连活动用户
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        search_sql = "SELECT user_Id from ten_even_activity where settlement_status ='未结算' and  renewal > 0 "
        no_settlement_ten_activity_user = []
        select = cursor.execute(search_sql)
        result = select.fetchall()
        for ten_activity in result:
            no_settlement_ten_activity_user.append(ten_activity[0])
        cursor.close()
        connect.close()
        return no_settlement_ten_activity_user

class Create:
    """
    初始化建表
    """

    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')

    def basic_user_information(self):
        """
        基本信息表
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        # 表结构：用户iD  用户名、 游戏场次、总计支出、总计收入、净收入、活跃状态、用户级别、注册时间

        create_sql = 'create table IF NOT EXISTS basic_user_information (user_Id INT PRIMARY KEY , ' \
                     'user_name CHAR(20) NOT NULL , ' \
                     'total_sessions INT NOT NULL, ' \
                     'total_expenses INT NOT NULL ,' \
                     'total_revenue INT NOT NULL, ' \
                     'net_income INT NOT NULL,' \
                     'active_status CHAR(50) NOT NULL, ' \
                     'user_leve INT NOT NULL,' \
                     'registration_time CHAR(50) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()

    def active_record(self):
        """
        活动记录表
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        # 表结构：场次  用户iD  信号  结算状态  时间
        create_sql = 'create table IF NOT EXISTS active_record (sessions INT NOT NULL , ' \
                     'user_Id INT NOT NULL, ' \
                     'flare_gun CHAR(20) NOT NULL, ' \
                     'settlement_status CHAR(20) NOT NULL,' \
                     'join_status CHAR(20) NOT NULL,' \
                     'time CHAR(20) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()


    def ten_even_activity(self):
        """
        间断记录表
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        # 表结构：用户iD  间断次数  续费补交  最后一次参加场次 ，超过十次 活跃状态置为不活跃
        create_sql = 'create table IF NOT EXISTS ten_even_activity (user_Id INT PRIMARY KEY, ' \
                     'discontinuous_number INT NOT NULL, ' \
                     'renewal integer NOT NULL ,' \
                     'last_session INT NOT NULL,' \
                     'settlement_status CHAR(20) NOT NULL, ' \
                     'time CHAR(20) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()



    def signal_gun_activity(self):
        """
        个人账单表
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        # 表结构：场次 用户ID 支出 收入 盈余 结算状态 创建时间

        create_sql = 'create table IF NOT EXISTS signal_gun_activity (user_Id INT NOT NULL , ' \
                     'sessions INT NOT NULL, ' \
                     'expenditure integer NOT NULL ,' \
                     'revenue INT NOT NULL,' \
                     'surplus INT NOT NULL,' \
                     'settlement_status CHAR(20) NOT NULL,' \
                     'creation_time CHAR(20) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()

    def financial_accounts(self):
        """
        财务账目
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        #    # 表结构：场次、盈余资金、结算资金、本期支出，本期收入、结余资金、结算类型（间断补费、活动结算）、时间
#Session, total income, total expenditure, remaining funds, current period expenditure, current period income, settlement type (intermittent premium, activity settlement), settlement time
        create_sql = 'create table IF NOT EXISTS financial_accounts (sessions INT NOT NULL, ' \
                     'total_income INT NOT NULL,'  \
                     'total_expenditure INT NOT NULL,' \
                     'remaining_funds INT NOT NULL, ' \
                     'current_period_income CHAR(20) NOT NULL,' \
                     'period_expenditure CHAR(20) NOT NULL,' \
                     'settlement_type CHAR(20) NOT NULL,' \
                     'settlement_time CHAR(20) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()

    def five_even_activity(self):
        """
        财务账目
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        #    # 表结构：场次、盈余资金、结算资金、本期支出，本期收入、结余资金、结算类型（间断补费、活动结算）、时间
        # cost Session, total income, total expenditure, remaining funds, current period expenditure, current period income, settlement type (intermittent premium, activity settlement), settlement time
        create_sql = 'create table IF NOT EXISTS five_even_activity (user_Id INT NOT NULL,settlement_session INT NOT NULL ,' \
                     'start_session INT NOT NULL,' \
                     'end_session INT NOT NULL,' \
                     'settlement_cost INT NOT NULL,' \
                     'settlement_status CHAR(20) NOT NULL,' \
                     'time CHAR(20) NOT NULL)'

        cursor.execute(create_sql)
        connect.commit()
        cursor.close()
        connect.close()

    def run_all(self):
        """

        :return:
        """
        for func in inspect.getmembers(self, predicate=inspect.ismethod):
            if func[0] not in ['run_all', '__init__']: func[1]()


class Insert:
    """
    1.字典表：初始化字典数据。
    2.结果表：数据插入
    """

    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')

    def basic_user_information(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()
        insert_sql = "insert into basic_user_information (user_Id," \
                             "user_name," \
                             "total_sessions ," \
                             "total_expenses," \
                             "total_revenue," \
                             "net_income," \
                             "active_status," \
                             "user_leve ," \
                             "registration_time) " \
                     "VALUES (:user_Id," \
                             ":user_name," \
                             ":total_sessions ," \
                             ":total_expenses, " \
                             ":total_revenue, " \
                             ":net_income," \
                             ":active_status, " \
                             ":user_leve ," \
                             ":registration_time)"  # REPLACE

        try:
            cursor.execute(insert_sql,
                           result)
        except :
            log = u'ERROR INSERT basic_user_information {0} '.format(result['user_Id'])
            common.Common.incolorprint(log, 'red')

        else:

            log = 'INFO INSERT basic_user_information SUCCESS {0}'.format(result['user_Id'])
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()


    def active_record(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        insert_sql = "insert into active_record (sessions," \
                     "user_Id," \
                     "flare_gun ," \
                     "settlement_status," \
                     "join_status," \
                     "time) " \
                     "VALUES (:sessions," \
                     ":user_Id," \
                     ":flare_gun," \
                     ":settlement_status," \
                     ":join_status," \
                     ":time)"  # REPLACE

        user_Id = result['user_Id']

        try:
            cursor.execute(insert_sql,
                           result)
        except :
            log = u'ERROR INSERT active_record {0}'.format(user_Id)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO INSERT active_record SUCCESS {0}'.format(user_Id)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def ten_even_activity(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        insert_sql = "replace into ten_even_activity (user_Id," \
                 "discontinuous_number," \
                 "renewal ," \
                 "last_session," \
                 "settlement_status," \
                 "time) " \
                 "VALUES (:user_Id," \
                 ":discontinuous_number," \
                 ":renewal," \
                 ":last_session," \
                 ":settlement_status," \
                 ":time)"


        user_Id = result['user_Id']

        cursor.execute(insert_sql,
                       result)
        try:
            cursor.execute(insert_sql,
                           result)
        except :
            log = u'ERROR INSERT RecommendData {0}'.format(user_Id)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO INSERT RecommendData SUCCESS {0}'.format(user_Id)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()


    def signal_gun_activity(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()


        insert_sql = "insert into signal_gun_activity (user_Id," \
                 "sessions," \
                 "expenditure ," \
                 "revenue," \
                 "surplus," \
                 "settlement_status,"\
                 "creation_time) " \
                 "VALUES (:user_Id," \
                 ":sessions," \
                 ":expenditure," \
                 ":revenue," \
                 ":surplus," \
                 ":settlement_status," \
                 ":creation_time)"


        user_Id = result['user_Id']

        try:
            cursor.execute(insert_sql,
                           result)
        except :
            log = u'ERROR INSERT signal_gun_activity {0}'.format(user_Id)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO INSERT signal_gun_activity SUCCESS {0}'.format(user_Id)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def financial_accounts(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        insert_sql = "insert into financial_accounts (sessions," \
                 "total_income," \
                 "total_expenditure ," \
                 "remaining_funds," \
                 "current_period_income,"\
                 "period_expenditure," \
                 "settlement_type," \
                 "settlement_time) " \
                 "VALUES (:sessions," \
                 ":total_income," \
                 ":total_expenditure," \
                 ":remaining_funds," \
                 ":current_period_income,"\
                 ":period_expenditure," \
                 ":settlement_type," \
                 ":settlement_time)"

        sessions = result['sessions']
        try:
            cursor.execute(insert_sql,
                           result)
        except :
            log = u'ERROR INSERT financial_accounts {0}'.format(sessions)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO INSERT financial_accounts SUCCESS {0}'.format(sessions)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()


    def five_even_activity(self, result):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        insert_sql = "insert into five_even_activity (user_Id,settlement_session," \
                     "start_session," \
                     "end_session," \
                     "settlement_cost," \
                     "settlement_status," \
                     "time) " \
                     "VALUES (:user_Id, " \
                     ":settlement_session," \
                     ":start_session," \
                     ":end_session," \
                     ":settlement_cost," \
                     ":settlement_status," \
                     ":time)"

        settlement_session = result['settlement_session']
        try:
            cursor.execute(insert_sql,
                           result)
        except:
            log = u'ERROR INSERT financial_accounts {0}'.format(settlement_session)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO INSERT financial_accounts SUCCESS {0}'.format(settlement_session)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()



class Update:
    """
    1.字典表：初始化字典数据。
    2.结果表：数据插入
    """

    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Happy.db')


    def settlement_signal_gun_activity(self,sessions):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE signal_gun_activity SET settlement_status= '已结算' WHERE sessions= '{0}';".format(sessions)

        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE signal_gun_activity'
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE signal_gun_activity SUCCESS '
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def ten_even_activity(self,renewal, user_Id):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE ten_even_activity SET renewal={0}  WHERE user_Id= {1};".format(renewal,user_Id)
        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE ten_even_activity'
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE ten_even_activity SUCCESS '
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()



    def basic_user_information(self,user_Id,total_sessions,total_expenses,total_revenue,net_income):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE basic_user_information SET total_sessions={0} , total_expenses={1}, total_revenue={2} ,net_income ={3} WHERE user_Id= {4};".format(total_sessions,total_expenses,total_revenue,net_income,user_Id)
        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE basic_user_information ,uesr_id :{0}'.format(user_Id)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE basic_user_information SUCCESS ,uesr_id :{0}'.format(user_Id)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()




    def active_status(self, user_Id,active_status='活跃'):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE basic_user_information SET active_status='{0}' WHERE user_Id= {1};".format(active_status,user_Id)
        try:
            cursor.execute(update_sql)
        except:
            log = u'ERROR UPDATE basic_user_information ,uesr_id :{0}'.format(user_Id)
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE basic_user_information SUCCESS ,uesr_id :{0}'.format(user_Id)
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def settlement_five_even_activity(self,session):
        """
        结算 连续5次未捡到空投
        :param user_Id:
        :param active_status:
        :return:
        """
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE five_even_activity SET settlement_status='已结算' WHERE settlement_session='{0}';".format(session)
        try:
            cursor.execute(update_sql)
        except:
            log = u'ERROR UPDATE five_even_activity '
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE five_even_activity SUCCESS'
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def settlement_ten_even_activity(self,session):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE ten_even_activity SET discontinuous_number=0 ,renewal=0 ,settlement_status='已结算' WHERE last_session= {0};".format(session)

        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE ten_even_activity'
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE ten_even_activity SUCCESS '
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def settlement_ten_even_activity_last_session(self,session,user_Id):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE ten_even_activity SET last_session= {0}  WHERE user_Id= {1};".format(session,user_Id)

        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE ten_even_activity'
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE ten_even_activity SUCCESS '
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()

    def settlement_active_record(self,session):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        update_sql = "UPDATE active_record SET settlement_status='已结算' WHERE sessions= {0};".format(session)

        try:
            cursor.execute(update_sql)
        except :
            log = u'ERROR UPDATE active_record'
            common.Common.incolorprint(log, 'red')

        else:
            pass
            log = 'INFO UPDATE active_record SUCCESS '
            common.Common.incolorprint(log, 'GREEN')
        connect.commit()
        connect.close()


class Delete:
    def __init__(self):
        self._sql_connect = common.Common.abs_path(__file__, 'Locust.db')

    def delete_table(self, tablename):
        connect = sqlite3.connect(self._sql_connect)
        cursor = connect.cursor()

        create_sql = 'delete from {0}'.format(tablename)
        cursor.execute(create_sql)
        log = 'INFO DELETE {0} SUCCESS '.format(tablename)
        common.Common.incolorprint(log, 'GREEN')
        cursor.close()
        connect.commit()
        connect.close()


class MainInit:
    def __init__(self, init=True):
        if init:
            # 初始化建表
            Create().run_all()


if __name__ == "__main__":
    MainInit()
    # Search().financial_accounts()
    all_records_list =  Search().get_session_revenue(202005279)

    print(all_records_list)
    print(common.Common.abs_path(__file__, 'Happy.db'))
