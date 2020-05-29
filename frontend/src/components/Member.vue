<template>
<div class="home">

<div class="table">
<el-row>
<el-table :data="bookList" style="width: 100%"  :row-style="{height:'20px'}" :cell-style="{padding:'10px'}"  size="small" border>

    <el-table-column prop="sessions" label="会员权益" min-width="60" align="center" header-align="center" max-height= "10">
    <template slot-scope="scope"> {{ scope.row.equity }} </template>

    </el-table-column>

    <el-table-column prop="user_Id" label="白银会员" min-width="60" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope">{{ scope.row.Silver}} </template>

    </el-table-column>
    <el-table-column prop="expenditure" label="黄金会员" min-width="60" align="center" header-align="center"  max-height= "20">
    <template slot-scope="scope"> {{ scope.row.Gold }} </template>
    </el-table-column>

    <el-table-column prop="revenue" label="铂金会员" min-width="60" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope"> {{ scope.row.Platinum }} </template>
    </el-table-column>

    <el-table-column prop="surplus" label="钻石会员" min-width="60" align="center" header-align="center" max-height= "20">
    <template slot-scope="scope"> {{ scope.row.Diamond }} </template>
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
      bookList: [
      {equity:"会员价值(RMB)/月",Silver:10, Gold:20, Platinum:"敬请期待!", Diamond:"敬请期待!"},
      {equity:"单场投币金额(RMB)",Silver:1, Gold:2, Platinum:"敬请期待!",Diamond:"敬请期待!"},
      {equity:"空投基金分配(百分比)",Silver:55, Gold:60, Platinum:"敬请期待!", Diamond:"敬请期待!"},
      {equity:"轰炸区保险(RMB)",Silver:0, Gold:1, Platinum:"敬请期待!", Diamond:"敬请期待!"},
      {equity:"买就返(RMB)",Silver:0, Gold:0, Platinum:"敬请期待!", Diamond:"敬请期待!"},
      ]
    }
  }
}
</script>
el-table-column {
  height: 10px;
}
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style >

.home {
  margin: 0px 0px 120px 0px;
  height: 10px;
  text-align: center;
  color: #fff; /*设置字体颜色*/
  font-weight: bold;

}
</style>
