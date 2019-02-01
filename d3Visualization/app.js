width = 964
height = width
outerRadius = Math.min(width, height) * 0.5
innerRadius = outerRadius - 124
// d3 = require("d3@5")

chord = d3.chord()
.padAngle(.04)
.sortSubgroups(d3.descending)
.sortChords(d3.descending)

arc = d3.arc()
.innerRadius(innerRadius)
.outerRadius(innerRadius + 20)

ribbon = d3.ribbon()
.radius(innerRadius)

color = d3.scaleOrdinal(d3.schemeCategory10)




data = function() {
    const imports = d3.json("https://gist.githubusercontent.com"
        + "/mbostock/1044242"
        + "/raw/3ebc0fde3887e288b4a9979dad446eb434c54d08"
        + "/flare.json");
  
    const indexByName = new Map;
    const nameByIndex = new Map;
    const matrix = [];
    let n = 0;
  
    // Returns the Flare package name for the given class name.
    function name(name) {
      return name.substring(0, name.lastIndexOf(".")).substring(6);
    }
  
    // Compute a unique index for each package name.
    imports.forEach(d => {
      if (!indexByName.has(d = name(d.name))) {
        nameByIndex.set(n, d);
        indexByName.set(d, n++);
      }
    });
  
    // Construct a square matrix counting package imports.
    imports.forEach(d => {
      const source = indexByName.get(name(d.name));
      let row = matrix[source];
      if (!row) row = matrix[source] = Array.from({length: n}).fill(0);
      d.imports.forEach(d => row[indexByName.get(name(d))]++);
    });
  
    return {
      matrix,
      indexByName,
      nameByIndex
    };
  }


chart = function() {
    const svg = d3.select("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height])
        .attr("font-size", 10)
        .attr("font-family", "sans-serif")
        .style("width", "100%")
        .style("height", "auto");
  
    const chords = chord(data.matrix);
  
    const group = svg.append("g")
      .selectAll("g")
      .data(chords.groups)
      .enter().append("g");
  
    group.append("path")
        .attr("fill", d => color(d.index))
        .attr("stroke", d => color(d.index))
        .attr("d", arc);
  
    group.append("text")
        .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
        .attr("dy", ".35em")
        .attr("transform", d => `
          rotate(${(d.angle * 180 / Math.PI - 90)})
          translate(${innerRadius + 26})
          ${d.angle > Math.PI ? "rotate(180)" : ""}
        `)
        .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
        .text(d => data.nameByIndex.get(d.index));
  
    svg.append("g")
        .attr("fill-opacity", 0.67)
      .selectAll("path")
      .data(chords)
      .enter().append("path")
        .attr("stroke", d => d3.rgb(color(d.source.index)).darker())
        .attr("fill", d => color(d.source.index))
        .attr("d", ribbon);
  
    return svg.node();
  }

chart()