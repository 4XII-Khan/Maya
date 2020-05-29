<template>
<div class="home" id="nojoin">

  <el-table
    :data="results.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100% " size="small">
    <el-table-column
      label="玩家昵称"
      prop="user_name">
    </el-table-column>

    <el-table-column
      label="连续未参加场数"
      prop="discontinuous_number">
    </el-table-column>

    <el-table-column
      label="激活费用"
      prop="renewal">
    </el-table-column>

    <el-table-column
      label="最后一次参与场次"
      prop="last_session">
    </el-table-column>

    <el-table-column
      label="结算时间"
      prop="time">
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
        results: [],
        search: ''
      }
    },
    mounted: function () {
    this.get_continuously_not_join()
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      },
      get_continuously_not_join () {
        this.$http.get('http://127.0.0.1:8000/api/get_continuously_not_join')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (res.error_num === 0) {
              this.results = res['list']
            } else {
              this.$message.error('查询失败')
              console.log(res['msg'])
            }
          })
    }
    },
  }
</script>
<style >

</style>
