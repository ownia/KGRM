$(function () {
    $.get('/graph', function (result) {
        var style = [
            {selector: 'node[label = "class"]', css: {'background-color': '#6FB1FC'}},
            {selector: 'node[label = "newNode"]', css: {'background-color': '#F5A45D'}}
        ];

        var cy = cytoscape({
            container: document.getElementById('cy'),
            style: style,
            layout: {name: 'cose', fit: false},
            elements: result.elements
        });
    }, 'json');
});