<template>
<div class="home" id="person">

  <el-table
    :data="bookList.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100% " size="small">
    <el-table-column
      label="游戏场次"
      prop="sessions">
    </el-table-column>
    <el-table-column
      label="玩家昵称"
      prop="user_name">
    </el-table-column>

    <el-table-column
      label="本场支出"
      prop="expenditure">
    </el-table-column>

    <el-table-column
      label="本场收入"
      prop="revenue">
    </el-table-column>

    <el-table-column
      label="净收入"
      prop="surplus">
    </el-table-column>

    <el-table-column
      label="结算状态"
      prop="settlement_status">
    </el-table-column>

    <el-table-column
      label="游戏时间"
      prop="creation_time">
    </el-table-column>

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
        bookList: [],
        search: ''
      }
    },
    mounted: function () {
    this.select_personal_bills()
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
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
    },
  }
</script>
<style >

</style>
