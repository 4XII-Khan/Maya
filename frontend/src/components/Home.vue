<template>
<div class="home">

<el-row display="margin-top:10px">

<el-input v-model="input.join" placeholder="参与玩家" style="display:inline-table; width: 20%; margin: 8px 10px; float:left"></el-input>
<el-input v-model="input.pick" placeholder="获取空投玩家" style="display:inline-table; width: 10%; margin: 8px 2px; float:left"></el-input>
<el-button type="primary" @click="addBook()" style="float:left; margin: 8px 2px;">新建场次</el-button>

<el-button type="primary" @click="addBook()" style="float:left;  margin: 8px 2px 8px 20px; ">结算</el-button>
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
            <template>
              <el-button type="primary" icon="el-icon-edit" size= "mini"  @click="dialogFormVisible = true"></el-button>
              <el-button type="primary" icon="el-icon-delete" size= "mini" @click="dialogFormVisible = true"></el-button>

              <div id="create" >
              <el-dialog title="创建场次" :visible.sync="dialogFormVisible" :destroy-on-close="destroyOnClose" :size="mini">
              <el-form :model="ruleForm" :rules="rules" ref="ruleForm" :label-position="lablePosition" label-width="100px" class="demo-ruleForm"  >
                <el-form-item label="当日场次" prop="name">
                  <el-input v-model="ruleForm.name" style="width:40%;" ></el-input>
                </el-form-item>

                <el-form-item label=" 参与用户" >
                  <el-select v-model="valuejoin" multiple filterable allow-create default-first-option medium placeholder="请选择参与用户" style="width:60%;">
                  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" ></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label=" 幸运用户" >
                  <el-select v-model="valueluck" multiple filterable allow-create default-first-option placeholder="请选择幸运用户" style="width:60%;">
                  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="活动时间" required>
                  <el-col :span="11">
                    <el-form-item prop="date1">
                      <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date1" style="width: 60%;"></el-date-picker>
                    </el-form-item>
                  </el-col>
                </el-form-item>

                <el-form-item label="锦鲤活动" prop="type">
                  <el-checkbox-group v-model="ruleForm.type">
                    <el-checkbox label="会员活动" name="type"></el-checkbox>
                    <el-checkbox label="吃鸡大奖" name="type"></el-checkbox>
                    <el-checkbox label="空投大奖" name="type"></el-checkbox>
                    <el-checkbox label="击杀大奖" name="type"></el-checkbox>
                  </el-checkbox-group>
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
                  <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>

              </el-form>
              </el-dialog>
              </div>
              <div id="delete" >

              <el-dialog title="创建场次" :visible.sync="dialogFormVisible" :destroy-on-close="destroyOnClose" :size="mini">
              <el-form :model="ruleForm" :rules="rules" ref="ruleForm" :label-position="lablePosition" label-width="100px" class="demo-ruleForm"  >
                <el-form-item label="当日场次" prop="name">
                  <el-input v-model="ruleForm.name" style="width:40%;" ></el-input>
                </el-form-item>

                <el-form-item label=" 参与用户"  >
                  <el-select v-model="valuejoin" multiple filterable allow-create default-first-option medium placeholder="请选择参与用户" style="width:60%;">
                  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" ></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label=" 幸运用户" >
                  <el-select v-model="valueluck" multiple filterable allow-create default-first-option placeholder="请选择幸运用户" style="width:60%;">
                  <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="活动时间" required>
                  <el-col :span="11">
                    <el-form-item prop="date1">
                      <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date1" style="width: 60%;"></el-date-picker>
                    </el-form-item>
                  </el-col>
                </el-form-item>

                <el-form-item label="锦鲤活动" prop="type">
                  <el-checkbox-group v-model="ruleForm.type">
                    <el-checkbox label="会员活动" name="type"></el-checkbox>
                    <el-checkbox label="吃鸡大奖" name="type"></el-checkbox>
                    <el-checkbox label="空投大奖" name="type"></el-checkbox>
                    <el-checkbox label="击杀大奖" name="type"></el-checkbox>
                  </el-checkbox-group>
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
                  <el-button @click="resetForm('ruleForm')">重置</el-button>
                </el-form-item>

              </el-form>
              </el-dialog>
              </div>
            </template>
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
      bookList: [],
      ruleForm: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入场次', trigger: 'blur' },
            { min: 1, max: 3, message: '长度在 1 到 3 个字符', trigger: 'blur' }
          ],
          date1: [
            { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
          ],
          type: [
            { type: 'array', required: true, message: '请至少选择一个', trigger: 'change' }
          ]
        },
        options: [{
          value: '惊雷',
          label: '惊雷'
        }, {
          value: '紫电',
          label: '紫电'
        }, {
          value: '享自由',
          label: '享自由'
        }, {
          value: '屠呦呦',
          label: '屠呦呦'
        }],
        valuejoin: [],
        valueluck: [],
        dialogFormVisible: false,
        value: 1,
        lablePosition: 'left',
        destroyOnClose: true,
        mini: 'mini',
        dialogFormVisible: false
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
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('submit!');
        } else {
          console.log('error submit!!');
          return false;
        }
      });
      },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }
}
</script>
el-table-column {
  height: 10px;
}
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#create {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  margin-top: 10px 30px;

}
#delete {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  margin-top: 10px 30px;

}
</style>
