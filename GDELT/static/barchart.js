var margin = {
        top: 20,
        right: 30,
        bottom: 30,
        left: 40
    },
    width = 480 - margin.left - margin.right,
    barHeight = 40;

var x = d3.scale.linear()
    .range([0, width]);

var yAxis = d3.svg.axis()
    .orient('left');

// Chart is the SVG
var chart = d3.select("#area1").append('svg')
    .attr('class', 'chart')
    .attr('width', width + margin.left + margin.right);

var colorbar = d3.scale.linear()
    .range(["red", "white", "green"]);

function draw_bars(country_file, country_name) {
    d3.tsv(country_file, type, function(error, data) {
        x.domain([0, d3.max(data, function(d) {
            return d.value;
        })]);
        colorbar.domain([-10., 0., 10.]);

        var y = d3.scale.linear()
            .range([0, (barHeight * data.length)])
            .domain([0, data.length]);

        yAxis.scale(y)
            .ticks(data.length);

        chart.attr('height', (margin.top + barHeight * data.length + 5));

        chart.append("text")
            .attr("x", (width / 2))
            .attr("y", margin.top * 2 / 3)
            .attr("text-anchor", "middle")
            .style("font-size", "26px")
            .style("text-decoration", "bold")
            .style("text-decoration", "underline")
            .text(country_name);

        var bar = chart.selectAll('g')
            .data(data)
            .enter().append('g')
            .attr('transform', function(d, i) {
                return 'translate(' + margin.left + ',' +
                    (margin.top + i * barHeight) + ')';
            });

        bar.append('rect')
            .attr('width', function(d) {
                return 1.3 * x(d.value);
            })
            .attr('height', barHeight / 2)
            .attr('y', barHeight / 2)
            .style('fill', function(d) {
                return colorbar(d.tone);
            });

        bar.append('text')
            .attr('x', function(d) {
                return 1.05 * x(d.value) - 3;
            })
            .attr('y', barHeight / 2)
            .attr('dy', '.99em')
            .style('text-anchor', 'center')
            .text(function(d) {
                return d.tone;
            });

        bar.append('text')
            .attr('x', margin.left + 1)
            .attr('y', barHeight / 4)
            .attr('dy', '.55em')
            .attr('font', 'sans-serif')
            .attr('font-size', '12px')
            .style('fill', 'black')
            .style('text-anchor', 'start')
            .text(function(d) {
                return d.Event;
            });

        // Now add the last *g*, i.e. the axis
        chart.append('g')
            .attr('class', 'y axis')
            .attr('transform', 'translate(' + margin.left + ',' + (margin.top) + ')')
            .call(yAxis)
            .append("text")
            .attr('transform', 'rotate(-90)')
            .attr('y', -30)
            .attr('x', -20)
            .attr('dy', '.71em')
            .style('text-anchor', 'end')
            .text('Ranking');
    });
};
    function type(d) {
        d.value = +d.value;
        return d;
    }
