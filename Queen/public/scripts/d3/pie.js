/*
 * Create a new d3js pie chart with animation
 *
 * __author__ = "Bradley Jones, Jack Fletcher"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

var width = 960,
    height = 450,
    radius = Math.min(width, height) / 2;

  var pie = d3.layout.pie()
.sort(null)
  .value(function(d) {
    return d.value;
  });

  var arc = d3.svg.arc()
.outerRadius(radius * 0.8)
  .innerRadius(radius * 0.4);

  var outerArc = d3.svg.arc()
.innerRadius(radius * 0.9)
  .outerRadius(radius * 0.9);

  var color;

  var key = function(d){ return d.data.label; };

/*
 * Create the pie chart
 * @param divID is the id of the div containing the pie
 * @param data, list of fields with Label and value (count)
 * [ { label: label, value: value } ]
 */
function pieChart(divID, data){
  //create pie chart!
  console.log(data);

  //Put labels in domain
  color = d3.scale.category20()
    .domain(data.map(function(item){
      return item.label;
    }));

        var svg = d3.select(divID)
        .append("svg")
          .attr("width", width)
          .attr("height", height)
        .append("g")

        svg.append("g")
        .attr("class", "slices");

        svg.append("g")
        .attr("class", "labels");

        svg.append("g")
        .attr("class", "lines");

        svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        pieChange(divID, data);

}

function pieChange(divID, data) {

  var svg = d3.select(divID);
  console.log("Creating Pie");

    /* ------- PIE SLICES -------*/
    var slice = svg.select(".slices").selectAll("path.slice")
    .data(pie(data), key);

  slice.enter()
    .insert("path")
    .style("fill", function(d) { return color(d.data.label); })
    .attr("class", "slice");

  slice
    .transition().duration(1000)
    .attrTween("d", function(d) {
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        return arc(interpolate(t));
      };
    })

  slice.exit()
    .remove();

  /* ------- TEXT LABELS -------*/

  var text = svg.select(".labels").selectAll("text")
    .data(pie(data), key);

  text.enter()
    .append("text")
    .attr("dy", ".35em")
    .text(function(d) {
      return d.data.label;
    });

  function midAngle(d){
    return d.startAngle + (d.endAngle - d.startAngle)/2;
  }

  text.transition().duration(1000)
    .attrTween("transform", function(d) {
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        var d2 = interpolate(t);
        var pos = outerArc.centroid(d2);
        pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
        return "translate("+ pos +")";
      };
    })
  .styleTween("text-anchor", function(d){
    this._current = this._current || d;
    var interpolate = d3.interpolate(this._current, d);
    this._current = interpolate(0);
    return function(t) {
      var d2 = interpolate(t);
      return midAngle(d2) < Math.PI ? "start":"end";
    };
  });

  text.exit()
    .remove();

  /* ------- SLICE TO TEXT POLYLINES -------*/

  var polyline = svg.select(".lines").selectAll("polyline")
    .data(pie(data), key);

  polyline.enter()
    .append("polyline");

  polyline.transition().duration(1000)
    .attrTween("points", function(d){
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        var d2 = interpolate(t);
        var pos = outerArc.centroid(d2);
        pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
        return [arc.centroid(d2), outerArc.centroid(d2), pos];
      };
    });

  polyline.exit()
    .remove();
};
