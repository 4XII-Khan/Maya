<template>
  <div class="visual-chart1" id="myChart1"></div>
</template>

<script>
export default {
  name: 'first',
  props: {
    lineData: {
      type: Object
    }
  },
  data () {
    return {
      faultByHourTime: null
    }
  },
  mounted () {
    this.chartsView()
  },
  methods: {
    chartsView () {
      let myChart = this.$echarts.init(document.getElementById('myChart1'))
      var option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            lineStyle: {
              color: '#57617B'
            }
          }
        },
        legend: {
          itemWidth: 18,
          itemHeight: 10,
          itemGap: 13,
          data: ['学校管理员', '教师', '学员'],
          right: '10px',
          top: '0px',
          textStyle: {
            fontSize: 12,
            color: '#fff'
          }
        },
        grid: {
          left: '8%',
          top: '10%',
          bottom: '10%',
          right: '10%'
        },
        xAxis: [
          {
            type: 'category',
            boundaryGap: false,
            axisLine: {
              lineStyle: {
                color: '#57617B'
              }
            },
            axisLabel: {
              textStyle: {
                color: '#fff'
              }
            },
            data: this.lineData.date
          }
        ],
        yAxis: [
          {
            type: 'value',
            axisTick: {
              show: false
            },
            axisLine: {
              lineStyle: {
                color: '#57617B'
              }
            },
            axisLabel: {
              margin: 10,
              textStyle: {
                fontSize: 14
              },
              textStyle: {
                color: '#fff'
              }
            },
            splitLine: {
              lineStyle: {
                color: '#57617B'
              }
            }
          }
        ],
        series: [
          {
            name: '学校管理员',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: {
              normal: {
                width: 2
              }
            },
            areaStyle: {
              normal: {
                color: new this.$echarts.graphic.LinearGradient(0, 1, 0, 0, [
                  {
                    offset: 0,
                    color: 'rgba(7,46,101,0.2)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0,166,246,0.4)'
                  }
                ]),
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                shadowBlur: 10
              }
            },
            itemStyle: {
              normal: {
                color: '#3A44FB'
              }
            },
            data: this.lineData.sta
          },
          {
            name: '教师',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: {
              normal: {
                width: 2
              }
            },
            areaStyle: {
              normal: {
                color: new this.$echarts.graphic.LinearGradient(0, 1, 0, 0, [
                  {
                    offset: 0,
                    color: 'rgba(7,44,90,0.2)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0,212,199,0.4)'
                  }
                ]),
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                shadowBlur: 10
              }
            },
            itemStyle: {
              normal: {
                color: '#00d4c7'
              }
            },
            data: this.lineData.ta
          },
          {
            name: '学员',
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: {
              normal: {
                width: 2
              }
            },
            areaStyle: {
              normal: {
                color: new this.$echarts.graphic.LinearGradient(0, 1, 0, 0, [
                  {
                    offset: 0,
                    color: 'rgba(7,44,90,0.2)'
                  },
                  {
                    offset: 1,
                    color: 'rgba(0,146,246,0.4)'
                  }
                ]),
                shadowColor: 'rgba(0, 0, 0, 0.1)',
                shadowBlur: 10
              }
            },
            itemStyle: {
              normal: {
                color: '#0092f6'
              }
            },
            data: this.lineData.sa
          }
        ]
      }

      myChart.setOption(option)
      setTimeout(function () {
        window.onresize = function () {
          myChart.resize()
        }
      }, 200)

      // 动态显示tootip
      var faultByHourIndex = 0 // 播放所在下标
      this.faultByHourTime = setInterval(function () {
        // 使得tootip每隔三秒自动显示
        myChart.dispatchAction({
          type: 'showTip', // 根据 tooltip 的配置项显示提示框。
          seriesIndex: 0,
          dataIndex: faultByHourIndex
        })
        faultByHourIndex++
        // faultRateOption.series[0].data.length 是已报名纵坐标数据的长度
        if (faultByHourIndex > option.series[0].data.length) {
          faultByHourIndex = 0
        }
        if (faultByHourIndex > option.series[1].data.length) {
          faultByHourIndex = 0
        }
        if (faultByHourIndex > option.series[2].data.length) {
          faultByHourIndex = 0
        }
      }, 3000)
    }
  },
  beforeDestroy () {
    clearInterval(this.faultByHourTime)
    this.faultByHourTime = null
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.visual-chart1 {
  width: 100%;
  height: 100%;
}
</style>
