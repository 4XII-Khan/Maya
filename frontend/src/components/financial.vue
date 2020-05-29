<template>
<div class="home" id="financial">

  <el-table
    :data="results.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100% " size="small">
    <el-table-column
      label="游戏场次"
      prop="sessions">
    </el-table-column>

    <el-table-column
      label="基金总收入"
      prop="total_income">
    </el-table-column>


    <el-table-column
      label="基金总支出"
      prop="total_expenditure">
    </el-table-column>

    <el-table-column
      label="基金净收入"
      prop="remaining_funds">
    </el-table-column>

    <el-table-column
      label="本场收入"
      prop="current_period_income">
    </el-table-column>

    <el-table-column
      label="本场支出"
      prop="period_expenditure">
    </el-table-column>

    <el-table-column
      label="结算状态"
      prop="settlement_type">
    </el-table-column>

    <el-table-column
      label="结算时间"
      prop="settlement_time">
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
    this.get_financial_accounts()
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      },
      get_financial_accounts () {
        this.$http.get('http://127.0.0.1:8000/api/get_financial_accounts')
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
