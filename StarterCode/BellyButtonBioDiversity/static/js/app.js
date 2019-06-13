function buildMetadata(sample) {
    var meta_url = `/metadata/${sample}`;
    var meta_data = d3.select('#sample-metadata');
    meta_data.html("");
  
    // @TODO: Complete the following function that builds the metadata panel
    d3.json(meta_url).then(function(data) {
      Object.entries(data).forEach(function(d){
       var row = meta_data.append('p');
       row.text(`${d[0]}:${d[1]}\n`);
      });
      
    });
    
  }
  
  function buildCharts(sample) {
    var data_url = `/samples/${sample}`;
    // @TODO: Use `d3.json` to fetch the sample data for the plots
  
    //Bubble Plot
    d3.json(data_url).then(function(data) {
      var trace = {
        x: data.otu_ids,
        y: data.sample_values,
        text: data.otu_labels,
        mode: 'markers',
        marker: { size: data.sample_values,
                  color: data.otu_ids }
      };
      var bubble_data = [trace];
   
   // UPDATE LAYOUT MAKE IT PRETTY
  
      Plotly.newPlot('bubble', bubble_data);
   
    //Pie Chart  
    var trace1 = {
      values: data.sample_values.slice(0,10), 
      labels: data.otu_ids.slice(0,10),
      type: 'pie'
    };
  
    // UPDATE LAYOUT MAKE IT PRETTY
    var pie_data = [trace1];
  
    Plotly.newPlot('pie', pie_data);
  });
  };
  
  function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
  
    // Use the list of sample names to populate the select options
    d3.json("/names").then((sampleNames) => {
      sampleNames.forEach((sample) => {
        selector
          .append("option")
          .text(sample)
          .property("value", sample);
      });
  
      // Use the first sample from the list to build the initial plots
      const firstSample = sampleNames[0];
      buildCharts(firstSample);
      buildMetadata(firstSample);
    });
  }
  
  function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    buildCharts(newSample);
    buildMetadata(newSample);
  }
  
  // Initialize the dashboard
  init();