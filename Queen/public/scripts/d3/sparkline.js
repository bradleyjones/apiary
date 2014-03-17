"use strict"

var width = 500
  , height = 100
  , x = d3.scale.linear().range([0, width - 2])
  , y = d3.scale.linear().range([height - 4, 0])
  , parseTime = d3.time.format("%H")
  , line = d3.svg.line()
                    .interpolate("basis")
                    .x(function(d) { return x(d.time) })
                    .y(function(d) { return y(d.count) });

/*
 * Create the sparkline
 *
 * @param divID is the id of the div containing the sparkline
 * @param data is the data to be displayed on the sparkline
 * @param time is the unit of time to calculate the sparkline against
 */
function sparkline(divId, orig_data, time) {
  // Calculate the number of data items in a specific time
  var data = [];
  Object.keys(orig_data).forEach(function(k) {
    var d = {};
    d.time = k;
    d.count = orig_data[k];

    data.push(d);
  });

  console.log(data);

  x.domain(d3.extent(data, function (d) {
    return d.time;
  }));
  y.domain(d3.extent(data, function (d) {
    return d.count;
  }));

  var vis = d3.select(divId).append("svg")
              .attr("width", width)
              .attr("height", height)
              .append("g");

  // The line
  vis.append("path")
     .datum(data)
     .attr("class", "sparkline")
     .attr("d", line);

  // Circle at the end of line
  //vis.append("circle")
     //.attr("class", "sparkcircle")
     //.attr("cx", x(data[0].time))
     //.attr("cy", y(data[0].count))
     //.attr("r", 1.5);
}
