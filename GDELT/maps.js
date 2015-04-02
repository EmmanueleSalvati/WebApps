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

var color = d3.scale.linear()
    .range(["rgb(51,0,0)", "rgb(102,0,0)", "rgb(153,0,0)",
        "rgb(204,0,0)", "rgb(255,0,0)", "rgb(255,51,51)",
        "rgb(255,102,102)", "rgb(255, 153,153)",
        "rgb(255,204,204)"
    ]);

var projection = d3.geo.albers()
    .translate([width / 2, height / 2])
    .scale(400);

var path = d3.geo.path()
    .projection(projection)
    .pointRadius(2);

d3.csv("tot_events_northamerica.csv", function(data) {
    color.domain([
        d3.max(data, function(d) {
            return d.NumEvents;
        }),
        d3.min(data, function(d) {
            return d.NumEvents;
        })
    ]);

    d3.json("northamerica.json", function(error, json) {
        if (error) return console.error(error);

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

                    console.log("Num events:", topojson.feature(json,
                        json.objects.northamerica_subunits).features[j].properties.value);

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

        function somethingCool() {
            var mysel = d3.select(this).data();
            $("svg.chart").empty();
            var country = {'CAN': 'canada_20rows.tsv'};
            draw_bars(country[mysel[0].id]);
            // console.log(mysel[0].id);
        }

        d3.selectAll("path")
            .on("mouseover", somethingCool);

    });
});
