"use strict"

var margin {top:20, right: 20, bottom: 30, left: 50} 
  , width = 500 - margin.left - margin.right
  , height = 100 - margin.top - margin.bottom
  , x = d3.scale.linear().range([0, width - 2])
  , y = d3.scale.linear().range([height - 4, 0])
  , parseTime = d3.time.format("%H")
  , line = d3.svg.line()
                    .interpolate("basis")
                    .x(function(d) { return x(d.time) })
                    .y(function(d) { return y(d.count) });

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

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
              .attr("width", width + margin.left + margin.right)
              .attr("height", height + margin.top + margin.bottom)
              .append("g")
              .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // The line
  vis.append("path")
     .datum(data)
     .attr("class", "sparkline")
     .attr("d", line);

  // Circle at the end of line
  vis.append("circle")
     .attr("class", "sparkcircle")
     .attr("cx", x(data[data.length - 1].time))
     .attr("cy", y(data[data.length - 1].count))
     .attr("r", 1.5);

  //Whack x axis on
  vis.append("g")
     .attr("class", "x axis")
     .attr("transform", "translate(0," + height + ")")
     .call(xAxis);

  //Whack y axis on
  vis.append("g")
     .attr("class", "y axis")
     .call(yAxis)
     .append("text")
     .attr("transform", "rotate(-90)")
     .attr("y", 6)
     .attr("dy", ".71em")
     .style("text-anchor", "end")
     .text("Price ($)");
}
