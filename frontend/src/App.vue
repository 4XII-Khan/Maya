<template>

  <div id="app">
    <div id="line">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      @open="handleOpen"
      @close="handleClose"
      @select="handleSelect"
      text-color="#3E3E37"
      active-text-color="#ffd452" router>
      <el-menu-item v-for="(item,i) in navList" :key="i" :index="item.name">
        <template slot="title">
          <el-menu-item index="i">{{ item.navItem }}</el-menu-item>
        </template>
      </el-menu-item>
    </div>
    <router-view/>

  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
  		return {
  			navList:[
          {name:'User',navItem:'用户中心'},
          {name:'settlement',navItem:'结算中心'},
          {name:'nopick',navItem:'竞猜中心'},
          {name:'dataView',navItem:'锦鲤中心'},
          {name:'Rule',navItem:'通知中心'},
          {name:'Member',navItem:'会员中心'},

  			] }
  	},
  computed:{
      activeIndex(){
        return this.$route.path.replace('/','')
      }
    },
  methods: {
      handleSelect(key, keyPath) {
      console.log(key, keyPath);
      },
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  margin-top: 0px 30px;
}

#line {
  margin: 0px 0px 90px 0px;
  height: 10px;
  text-align: center;
  color: #fff; /*设置字体颜色*/
  font-weight: bold;
  font-size: 14px;
}


/*选中则发生一些变化*/
.router-link-active{
  background: rgba(255,255,255,0.8);
  color: #444;
}

</style>
