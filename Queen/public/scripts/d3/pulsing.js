/*
 * Create in d3js the pulsing animation that can be seen on the agents/Data page
 *
 * __author__ = "Bradley Jones"
 * __credits__ = ["Bradley Jones", "Jack Fletcher", "John Davidge", "Sam Betts"]
 * __license__ = "Apache v2.0"
 * __version__ = "1.0"
 */

// Create svg container
var vis = d3.select(".pulsing").append("svg")
                               .attr("width", 200)
                               .attr("height", 200)
                               .style("margin", "auto")
                               .style("display", "block");

// Draw circle
var radius = 80;
var circle = vis.append("circle")
                .attr("cx", 100)
                .attr("cy", 100)
                .attr("r", radius);

// Animations
function animateFirstStep() {
  circle
    .transition()
    .duration(800)
    .attr("r", radius + 5)
    .style("fill", "black")
    .each("end", function() {
      animateSecondStep();
    });
}

function animateSecondStep() {
  circle
    .transition()
    .duration(800)
    .attr("r", radius)
    .style("fill", "black")
    .each("end", function() {
      animateFirstStep();
    });
}

function animateIncrease() {
  circle
    .transition()
    .duration(1000)
    .attr("r", radius + 20)
    .style("fill", "green")
    .each("end", function() {
      animateSecondStep();
    });
}

function animateDecrease() {
  circle
    .transition()
    .duration(1000)
    .attr("r", radius - 10)
    .style("fill", "red")
    .each("end", function() {
      animateFirstStep();
    });
}

// Begin the animation
animateFirstStep();
