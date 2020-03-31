// 基于准备好的dom，初始化echarts实例
let myChart = echarts.init(document.getElementById('main'));

// 指定图表的配置项和数据
let option = {
    title: {
        text: 'ECharts'
    },
    tooltip: {},
    legend: {
        data: ['销量']
    },
    xAxis: {
        data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    },
    yAxis: {},
    series: [{
        name: '销量',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
    }]
};
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);

let option1 = {
    title: {
        text: '未来一周气温变化',
        subtext: '纯属虚构'
    },
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            formatter: '{value} °C'
        }
    },
    series: [{
        name: '最高气温', type: 'line', data: [11, 11, 15, 13, 12, 13, 10],
        markPoint: {
            data: [
                {type: 'max', name: '最大值'},
                {type: 'min', name: '最小值'}
            ]
        },
        markLine: {
            data: [
                {type: 'average', name: '平均值'}
            ]
        }
    },
        {
            name: '最低气温',
            type: 'line',
            data: [1, -2, 2, 5, 3, 2, 0],
            markPoint: {
                data: [
                    {name: '周最低', value: -2, xAxis: 1, yAxis: -1.5}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'},
                    [{symbol: 'none', x: '90%', yAxis: 'max'}, {
                        symbol: 'circle',
                        label: {normal: {position: 'start', formatter: '最大值'}},
                        type: 'max',
                        name: '最高点'
                    }]
                ]
            }
        }
    ]
};
let option2 = {
    title: {
        text: '大规模散点图'
    },
    legend: {
        data: ['sin', 'cos']
    },
    xAxis: [{type: 'value', scale: true}],
    yAxis: [{type: 'value', scale: true}],
    series: [{
        name: 'sin', type: 'scatter', large: true, symbolSize: 3, data: (function () {
            let d = [];
            let len = 10000;
            let x = 0;
            while (len--) {
                x = (Math.random() * 10).toFixed(3) - 0;
                d.push([
                    x,
                    //Math.random() * 10
                    (Math.sin(x) - x * (len % 2 ? 0.1 : -0.1) * Math.random()).toFixed(3) - 0
                ]);
            }
            //console.log(d)
            return d;
        })()
    },
        {
            name: 'cos',
            type: 'scatter',
            large: true,
            symbolSize: 2,
            data: (function () {
                let d = [];
                let len = 20000;
                let x = 0;
                while (len--) {
                    x = (Math.random() * 10).toFixed(3) - 0;
                    d.push([
                        x,
                        //Math.random() * 10
                        (Math.cos(x) - x * (len % 2 ? 0.1 : -0.1) * Math.random()).toFixed(3) - 0
                    ]);
                }
                //console.log(d)
                return d;
            })()
        }
    ]
};
let charts = [];
let chart1 = echarts.init(document.getElementById("left1"));
let chart2 = echarts.init(document.getElementById("left2"));
let chart3 = echarts.init(document.getElementById("right11"));
let chart4 = echarts.init(document.getElementById("right12"));
let chart5 = echarts.init(document.getElementById("right21"));
let chart6 = echarts.init(document.getElementById("right22"));
chart1.setOption(option1);
chart2.setOption(option1);
chart3.setOption(option2);
chart4.setOption(option2);
chart5.setOption(option1);
chart6.setOption(option1);
charts.push(chart1);
charts.push(chart2);
charts.push(chart3);
charts.push(chart4);
charts.push(chart5);
charts.push(chart6);
$(window).resize(function () {
    for (let i = 0; i < charts.length; i++) {
        charts[i].resize();
    }
});
$('a[data-toggle="pill"]').on('shown.bs.tab', function (e) {
    for (let i = 0; i < charts.length; i++) {
        charts[i].resize();
    }
});