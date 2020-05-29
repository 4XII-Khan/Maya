<template>
  <div id="page" >
    <el-collapse accordion>
    <el-collapse-item>
    <template slot="title">
      投币规则 Rules of the coin <i class="header-icon el-icon-info"></i>
    </template>
          <div>1. 每局游戏，每人次投币一元，主办方投币两元。纳入至活动奖池中，计作 M。</div>
    </el-collapse-item>

    <el-collapse-item>
    <template slot="title" >
      激励规则 Efficiencyy <i class="header-icon el-icon-info"></i>
    </template>
          <div>1.每局游戏中，通过任意方式获取到的有效空投枪（含子弹的空投枪）的人数，计作 N。</div>
          <div>2.获取到有效空投枪的人可平分当前活动奖池的 50% ，作为奖金 W，即可得 W = (M/2N) 元。</div>
    </el-collapse-item>


    <el-collapse-item>
    <template slot="title">
      活跃规则 Active rules <i class="header-icon el-icon-info"></i>
    </template>
          <div>1. 每当连续五局无人获取空投时，主办方获得奖池的10%。</div>
          <div>2. 当活动奖池出现奇数时，由主办方向上取整补齐至偶数。</div>
          <div>3. 当三人及以上参加游戏时，活动自动生效，连续十局不参加活动者，自动退出，永不退票，中途再次加入者需补齐奖池的20%方可加入活动。</div>
  </el-collapse-item>
  </el-collapse>

  </div>
</template>


<style scoped>

</style>
