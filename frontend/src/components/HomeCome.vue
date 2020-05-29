<template>
<div class="home">
<el-row display="margin-top:10px">

<el-input v-model="input.join" placeholder="参与玩家" style="display:inline-table; width: 20%; margin: 8px 10px; float:left"></el-input>
<el-input v-model="input.pick" placeholder="获取空投玩家" style="display:inline-table; width: 10%; margin: 8px 2px; float:left"></el-input>
<el-button type="primary" @click="addBook()" style="float:left; margin: 8px 2px;">新建场次</el-button>

<el-button type="primary" @click="addBook()" style="float:left; margin: 8px 2px 8px 20px;">结算</el-button>
</el-row>

<div class="table">
<el-row>
<el-table :data="bookList" style="width: 100%"  :row-style="{height:'20px'}" :cell-style="{padding:'10px'}" style="font-size: 14px" size="small" border>

    <el-table-column prop="sessions" label="场次" min-width="60" align="center" header-align="center" max-height= "10">
    <template slot-scope="scope"> {{ scope.row.sessions }} </template>
    </el-table-column>

    <el-table-column prop="user_Id" label="玩家昵称" min-width="60" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope" > {{ scope.row.user_name}} </template>
    </el-table-column>

    <el-table-column prop="expenditure" label="支出" min-width="60" align="center" header-align="center"  max-height= "20">
    <template slot-scope="scope"> {{ scope.row.expenditure }} </template>
    </el-table-column>

    <el-table-column prop="revenue" label="收入" min-width="60" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope"> {{ scope.row.revenue }} </template>
    </el-table-column>

    <el-table-column prop="surplus" label="净收入" min-width="60" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope"> {{ scope.row.surplus }} </template>
    </el-table-column>

    <el-table-column prop="settlement_status" label="结算状态" min-width="60" align="center" header-align="center" max-height= "20" >
    <template slot-scope="scope"> {{ scope.row.settlement_status }} </template>
    </el-table-column>

    <el-table-column prop="creation_time" label="游戏时间" min-width="80" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope"> {{ scope.row.creation_time }} </template>
    </el-table-column>

    <el-table-column prop="creation_time" label="操作" min-width="100" align="center" header-align="center" max-height= "20">
        <template slot-scope="scope"
          <el-button type="primary" icon="el-icon-edit" size= "mini" @click="addBook(scope.row)"></el-button>
          <el-button type="primary" icon="el-icon-share" size= "mini" @click="addBook(scope.row)"></el-button>
          <el-button type="primary" icon="el-icon-delete" size= "mini" @click="addBook(scope.row)"></el-button>

        </template>

    </el-table-column>

</el-table>

</el-row>
</div>

</div>

</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: {join: '', pick: ''},
      bookList: []
    }
  },
  mounted: function () {
    this.select_personal_bills()
  },
  methods: {
    addBook () {
      this.$http.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          if (res.error_num === 0) {
            this.showBooks()
          } else {
            this.$message.error('新增书籍失败，请重试')
            console.log(res['msg'])
          }
        })
    },
    select_personal_bills () {
      this.$http.get('http://127.0.0.1:8000/api/select_personal_bills')
        .then((response) => {
          var res = JSON.parse(response.bodyText)
          console.log(res)
          if (res.error_num === 0) {
            this.bookList = res['list']
          } else {
            this.$message.error('查询书籍失败')
            console.log(res['msg'])
          }
        })
    }
  }
}
</script>

}
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
