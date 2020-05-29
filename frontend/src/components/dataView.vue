<template>
<div class="dataView" >
<dv-decoration-8 style="width:300px;height:50px;" />
<dv-decoration-8 :reverse="true" style="width:300px;height:50px;" />
<dv-decoration-3 style="width:300px; height:30px;" />
<dv-decoration-9 style="width:150px;height:150px; ">100%</dv-decoration-9>

<dv-capsule-chart :config="config" style="width:300px;height:200px" />

</div>

</template>

<script>
export default {
  name: 'home',
  data () {
    return {
      input: {join: '', pick: ''},
      data: [
        {
          name: '南阳',
          value: 167
        },
        {
          name: '周口',
          value: 67
        },
        {
          name: '漯河',
          value: 123
        },
        {
          name: '郑州',
          value: 55
        },
        {
          name: '西峡',
          value: 98
        }
      ]
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
el-table-column {
  height: 10px;
}
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.dataView{
width: 100%;
height: 100%;
position: relative;

}

</style>
