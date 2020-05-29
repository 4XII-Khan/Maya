<template>
    <el-tabs v-model="activeName" @tab-click="handleClick" type="border-card">

      <el-tab-pane label="个人账单" name="personB" style="height:600px;overflow-y:auto;overflow-x:hidden;">
      <person ></person>
      </el-tab-pane>

      <el-tab-pane label="基金账单" name="financialA" style="height:600px;overflow-y:auto;overflow-x:hidden;">
      <financial ></financial>
      </el-tab-pane>

      <el-tab-pane label="五连账单" name="noPick" style="height:600px;overflow-y:auto;overflow-x:hidden;">
      <nopick ></nopick>
      </el-tab-pane>

      <el-tab-pane label="十连账单" name="continue" style="height:600px;overflow-y:auto;overflow-x:hidden;">
      <nojoin></nojoin>
      </el-tab-pane>

      <el-tab-pane label="基金大盘" name="third" style="height:600px;overflow-y:auto;overflow-x:hidden;">
      <dataView></dataView>
      </el-tab-pane>

    </el-tabs>

</template>

<script>
import financial from '@/components/financial'
import person from '@/components/person'
import nopick from '@/components/nopick'
import nojoin from '@/components/nojoin'
import dataView from '@/components/dataView'

export default {
  data () {
    return {
      activeName: 'second',
      stretch: true
    }
  },
  components: {
    person,
    financial,
    nopick,
    nojoin,
    dataView
  },
  methods: {
    handleClick (tab, event) {
      console.log(tab, event)
    }
  }
}
</script>

<style scoped>
.el-tab-pane {
    padding: 12px 10px;
    margin: 10px;

}
</style>
