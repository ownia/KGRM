$(function () {
    //禁用"确认重新提交表单"
    window.history.replaceState(null, null, window.location.href);
});

/*
$(function () {
    var cy = cytoscape({
        container: document.getElementById('cy'),
        style: [
            {
                selector: 'node[label = "Person"]',
                css: {'background-color': '#6FB1FC', 'content': 'data(name)'}
            },
            {
                selector: 'node[label = "Movie"]',
                css: {'background-color': '#F5A45D', 'content': 'data(title)'}
            },
            {
                selector: 'edge',
                css: {'content': 'data(relationship)', 'target-arrow-shape': 'triangle'}
            }
        ],
        elements: {
            nodes: [
                {data: {id: '172', name: 'Tom Cruise', label: 'Person'}},
                {data: {id: '183', title: 'Top Gun', label: 'Movie'}}
            ],
            edges: [{data: {source: '172', target: '183', relationship: 'Acted_In'}}]
        },
        layout: {name: 'grid'}
    });
});
*/

$(function () {
    $.get('/graph', function (result) {
        var style = [
            {
                selector: 'node',
                css: {'background-color': '#007bff', 'content': 'data(id)'}
            },
            {
                selector: 'edge',
                //css: {'content': 'data(relationship)', 'target-arrow-shape': 'triangle'}
                css: {'target-arrow-shape': 'triangle-backcurve', 'curve-style': 'unbundled-bezier', 'width': 2}
            },
            {
                selector: "node:selected",
                style: {
                    "border-width": "6px",
                    "border-color": "#AAD8FF",
                    "border-opacity": "0.5",
                    "background-color": "#77828C",
                    "text-outline-color": "#77828C"
                }
            },
        ];

        var cy = cytoscape({
            container: document.getElementById('cy'),
            style: style,
            elements: result,
            layout: {name: 'cose', fit: true}
        });


        cy.on('tap', 'node', function (evt) {
            const node = evt.target;
            document.getElementById('node_data').innerHTML = "节点id：" + node.id()
                + "<br>" + "节点类别：" + node.data('label') + "<br>" + "节点名称：" + node.data('title');
        });

        cy.on('tap', 'edge', function (evt) {
            const edge = evt.target;
            console.log(edge.data())
            document.getElementById('node_data').innerHTML = "源id：" + edge.data('source')
                + "<br>" + "目的id：" + edge.data('target') + "<br>" + "关系名称：" + edge.data('relationship');
        });

        cy.panzoom();

    }, 'json');
});

/*
function node_btn() {
    const text = document.getElementById('node_data').innerText;
    console.log(text);
    $.ajax({
        url: 'http://localhost:5000/',
        type: 'GET',
        data: text,
        dataType: 'text',
        success: function (res) {
            console.log(res)
            console.log(0)

        },
        error: function (res) {
            console.log(res);
            console.log(1)
        }
    })
}
*/
