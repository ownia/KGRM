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
                css: {'target-arrow-shape': 'triangle'}
            }
        ];

        var cy = cytoscape({
            container: document.getElementById('cy'),
            style: style,
            elements: result,
            layout: {name: 'cose', fit: true}
        });

    }, 'json');
});

var content = document.getElementById("content");
var contents = content.innerHTML;
var text = document.getElementById("text");
var value = text.value;
var values = contents.split(value);
content.innerHTML = values.join('<span style="background:red;">' + value + '</span>');
