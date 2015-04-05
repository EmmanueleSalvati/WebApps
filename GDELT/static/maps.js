var margin = {
        top: 50,
        right: 30,
        bottom: 30,
        left: 40
    },
    width = 600 - margin.left - margin.right,
    height = 600 - margin.top;

var svg = d3.select("#area2").append("svg")
    .attr('class', 'map')
    .attr('width', width)
    .attr('height', height);

var color = d3.scale.ordinal()
    .range(colorbrewer.PuRd[4]);

var projection = d3.geo.albers()
    .translate([width / 2, height / 2])
    .scale(400);

var path = d3.geo.path()
    .projection(projection)
    .pointRadius(2);

d3.csv("/static/tot_events_northamerica.csv", function(data) {
    color.domain([
        d3.min(data, function(d) {
            return d.NumEvents;
        }),
        d3.max(data, function(d) {
            return d.NumEvents;
        })
    ]);

    d3.json("/static/northamerica.json", function(error, json) {
        if (error) return console.error(error);

        var numColors = (topojson.feature(json,
            json.objects.northamerica_subunits).features.length);

        color.range(colorbrewer.Accent[numColors]);
        console.log(numColors);

        for (var i = 0; i < data.length; i++) {
            var country = data[i].DomainCountry;
            var numevents = parseFloat(data[i].NumEvents);

            for (var j = 0; j < (topojson.feature(json,
                    json.objects.northamerica_subunits).features.length); j++) {

                var jsonCountry = (topojson.feature(json,
                    json.objects.northamerica_subunits).features[j].properties).name;

                if (country === jsonCountry) {
                    topojson.feature(json,
                        json.objects.northamerica_subunits).features[j].properties.value = numevents;

                    // console.log("Num events:", topojson.feature(json,
                    //     json.objects.northamerica_subunits).features[j].properties.value);

                    break;
                }

            }
        }

        // I have to put the call function here
        svg.selectAll("path")
            .data(topojson.feature(json,
                json.objects.northamerica_subunits).features)
            .enter().append("path")
            .attr('d', path)
            .style("fill", function(d) {
                var value = d.properties.value;

                if (value) {
                    return color(value);
                } else {
                    return "#ccc";
                }
            });


        svg.selectAll(".subunit-label")
            .data(topojson.feature(json,
                json.objects.northamerica_subunits).features)
            .enter().append("text")
            .attr('class', function(d) {
                return "subunit-label " + d.id;
            })
            .attr('transform', function(d) {
                return "translate(" + path.centroid(d) + ")";
            })
            .attr('d', ".35em")
            .text(function(d) {
                return d.properties.name;
            });

        /* Add legend */
        var legendRectSize = 18;
        var legendSpacing = 4;
        var legend = svg.selectAll('.legend')
            .data(color.domain())
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var offset = 5 * numColors;
                var horz = 2 * legendRectSize;
                var vert = height - (i + 1) * offset;
                return 'translate(' + horz + ',' + vert + ')';
            });
        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', color)
            .style('stroke', color);
        legend.append('text')
            .attr('x', legendRectSize + legendSpacing)
            .attr('y', legendRectSize - legendSpacing)
            .text(function(d) {
                num = d.toString();
                return num + ' news events';
            });

        function somethingCool() {
            var mysel = d3.select(this).data();
            $("svg.chart").empty();
            var country = {
                'CAN': '/static/Canada.tsv',
                'MEX': '/static/Mexico.tsv',
                'USB': '/static/UnitedStates.tsv'
            };
            draw_bars(country[mysel[0].id], mysel[0].properties.name);
            // console.log(mysel[0].properties.name);
        }

        d3.selectAll("path")
            .on("mouseover", somethingCool);

    });
});
