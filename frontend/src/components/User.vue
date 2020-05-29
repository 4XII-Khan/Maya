<template>
<div class="home" >

  <el-table
    :data="alluser.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%" size="small" >
    <el-table-column label="玩家头像" align="center" header-align="center" >
    <div>
      <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" size="medium" fit="scale-down"></el-avatar>
    </div>

    </el-table-column>

    <el-table-column label="玩家昵称" align="center" header-align="center" prop="user_name"></el-table-column>

    <el-table-column label="会员等级" align="center" header-align="center">
      <template slot-scope="scope">
          <div slot="reference" class="name-wrapper">
            <el-tag size="small" type="info" color="#FFFFFF" v-if="scope.row.user_leve == '普通用户'"> {{ scope.row.user_leve }}</el-tag>
            <el-tag size="small" type="info"  color="#EDEBEB" v-else-if="scope.row.user_leve == '白银会员'" > {{ scope.row.user_leve }}</el-tag>
            <el-tag size="small" type="warning" v-else-if="scope.row.user_leve == '黄金会员'" > {{ scope.row.user_leve }}</el-tag>
            <el-tag size="small" type="info"  v-else > {{ scope.row.user_leve }}</el-tag>

          </div>
      </template>
    </el-table-column>

    <el-table-column label="游戏场数" align="center" header-align="center" prop="total_sessions"></el-table-column>

    <el-table-column label="总支出" align="center" header-align="center" prop="total_expenses"> </el-table-column>

    <el-table-column label="总收入" align="center" header-align="center" prop="total_revenue"> </el-table-column>

    <el-table-column label="净收入" align="center" header-align="center" prop="net_income"> </el-table-column>

    <el-table-column label="活跃状态" align="center" header-align="center" >
      <template slot-scope="scope">
        <div slot="reference" class="name-wrapper">
          <el-tag size="small" type="success" v-if="scope.row.active_status == '活跃'"> {{ scope.row.active_status }}</el-tag>
          <el-tag size="small" type="info"  v-else > {{ scope.row.active_status }}</el-tag>
       </div>
      </template>

     </el-table-column>

    <el-table-column label="注册时间" align="center" header-align="center" width="100px" prop="registration_time"> </el-table-column>

    <el-table-column align="right">
      <template slot="header" slot-scope="scope">
        <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/>
      </template>

      <template slot-scope="scope">
        <el-button type="primary" icon="el-icon-edit" size= "mini"  @click="handleEdit(scope.$index, scope.row)"></el-button>
        <el-button type="primary" icon="el-icon-delete" size= "mini" @click="handleDelete(scope.$index, scope.row)"></el-button>

      </template>
    </el-table-column>
  </el-table>

  <el-pagination
    background layout="prev, pager, next"  :total="10">
  </el-pagination>

</div>

</template>

<script>
  export default {
    data() {
      return {
        alluser: [],
        search: ''
      }
    },
    mounted: function () {
    this.get_all_users()
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      },
      get_all_users() {
        this.$http.get('http://127.0.0.1:8000/api/get_all_users')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (res.error_num === 0) {
              this.alluser = res['list']
            } else {
              this.$message.error('查询失败')
              console.log(res['msg'])
            }
          })
    }
    },
  }
</script>
<style scoped>
.el-pagination {
    padding: 12px 0;
    margin: 10px;
}
</style>
