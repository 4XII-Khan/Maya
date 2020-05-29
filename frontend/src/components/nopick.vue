<template>
<div class="home" id="pick">
  <el-table
    :data="results.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100% " size="small">
    <el-table-column
      label="起始场次"
      prop="start_session">
    </el-table-column>

    <el-table-column
      label="结束场次"
      prop="end_session">
    </el-table-column>

    <el-table-column
      label="结算费用"
      prop="settlement_cost">
    </el-table-column>
    <el-table-column
      label="结算场次"
      prop="settlement_session">
    </el-table-column>


    <el-table-column
      label="结算状态"
      prop="settlement_status">
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
    this.get_continuously_not_pick()
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      },
      get_continuously_not_pick () {
        this.$http.get('http://127.0.0.1:8000/api/get_continuously_not_pick')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (res.error_num === 0) {
              this.results = res['list']
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
