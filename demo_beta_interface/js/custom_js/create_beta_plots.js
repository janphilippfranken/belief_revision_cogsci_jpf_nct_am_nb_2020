// ########################################################################
// # FUNCTIONS FOR CREATING BETA PDF PLOTS
// ########################################################################

// estimating alpha and beta parameters based on mu and variance 
var est_beta_par = function (mu, variance) {
  var alpha = mu * (mu * (1 - mu) / variance - 1);
  var beta = alpha * (1 - mu) / mu; 
  // setting minimum parameter values to 1 
  alpha = Math.max(alpha, 1);
  beta = Math.max(beta, 1);
  return [alpha, beta] 
};

//  creating two data arrays where y corresponds to the output of the beta density (similar to the idea dnorm in r)
var create_arrays = function(start_val, stop_val, cardinality, alpha, beta) {
  var x_arr = [];
  var y_arr = [];
  var step = (stop_val - start_val) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
    x = start_val + (step * i);
    y = jStat.beta.pdf(x, alpha, beta); // round here
    x_arr.push(x);
    y_arr.push(y);
  };
  return [x_arr, y_arr];
};

//  creating specific data and parameters 
var create_data = function(mu, variance){
  var x = create_arrays(0.01, .99, 1000, 10, 10)[0]
  var alpha = est_beta_par(mu, variance)[0];
  var beta = est_beta_par(mu, variance)[1];
  var y = create_arrays(0.01, .99, 1000, alpha, beta)[1];
  return [x, y];
};

// get index of minimum of list 
function indexOfMin(arr) {
    if (arr.length === 0) {
        return -1;
    };
    var min = arr[0];
    var minIndex = 0;
    for (var i = 1; i < arr.length; i++) {
        if (arr[i] < min) {
            minIndex = i;
            min = arr[i];
        };
    };
    return minIndex;
};

// creating the beta pdf plot shown in the demo
var create_plot = function(x, y, belief_mu, plot_div, name_1, name_2, size, confidence) {
  var arr_diff = [];
  var text_name = ''; // can be amended to include annotations 
  var arrow = false; // can be set to true to include an arrow pointing to any arbitrary position on the plot 
  var scale_height = 1.6; // ratio between height and width 



  //  these for loops determine the upper and lower bound of the colored area. The values can be changed if one wishes to color the whole are vs. only a subpart of it 
  for (var i = 0; i < x.length; i++) {
    var x_val = x[i];
    arr_diff.push(Math.abs(belief_mu - x_val)); 
  };

  var closest_x = x.reduce(function(prev, curr) {
    return (Math.abs(curr - belief_mu) < Math.abs(prev - belief_mu) ? curr : prev);
  });
  
  var closest_x_small = x.reduce(function(prev, curr) {
    return (Math.abs(curr - 0.05) < Math.abs(prev - 0.05) ? curr : prev);
  });

 var closest_x_large = x.reduce(function(prev, curr) {
    return (Math.abs(curr - 0.95) < Math.abs(prev - 0.95) ? curr : prev);
  });

  var min_diff_index = indexOfMin(arr_diff); 

  var mode = x[y.indexOf(Math.max(...y))];

  var trace_1 = {
    x: x.slice(x.indexOf(closest_x_small), 500),
    y: y.slice(x.indexOf(closest_x_small), 500),
    type: 'scatter',
    fill: 'tozeroy',
    mode: 'lines',
    line:{color:'orange'}
  };

  var trace_2 = {
    x: x.slice(500, x.indexOf(closest_x_large)),
    y: y.slice(500, x.indexOf(closest_x_large)),
    type: 'scatter',
    fill: 'tozeroy',
    mode: 'lines',
    line:{color:'orange'}
  };

  var data = [ trace_1, trace_2 ];

  var layout = {
    hovermode: false,
    yaxis: {
      //range: [0, 13],
      fixedrange: false,
      showgrid: false,
      showaxis: false, 
      showticks: false,
      zeroline: false, 
      showticklabels: false},
      xaxis: {
        font:{size:15},
        fixedrange: true,
        showgrid: false,
        zeroline: false, 
        tickvals: [.01, .5, .99],
        ticktext: ["   " + name_1, '0.50', name_2 + "   "], 
        range: [0,1]},

    // shapes: [{type: 'line', x0: belief_mu, x1: belief_mu, y0:0, y1:y[min_diff_index],
       //                        line: {color:'black', width : 3}
         //                      }],
    autosize:false,
    width: size,
    height: size/scale_height,     
    title: { 
      text: "P(H)",
      font: {size: 22}},
    showlegend: false,
    annotations: [
    {
      x: belief_mu,
      y: 3, // y[x.indexOf(belief_mu)]
      font: {size:15},
      xref: 'x',
      yref: 'y', 
      text: text_name,
      showarrow: arrow,   
      arrowhead: 2,
      ax: 0,
      ay: -45,
    }]
  };
  Plotly.newPlot(plot_div, data, layout, {displayModeBar: false}, {staticPlot: true});
};


var create_plot_start = function(x, y, belief_mu, plot_div, name_1, name_2, title_name) {
  var arr_diff = [];
  for (var i = 0; i < x.length; i++) {
    var x_val = x[i];
    arr_diff.push(Math.abs(belief_mu - x_val));
  };
  var min_diff_index = indexOfMin(arr_diff);
  // var trace_1 = {
  //   x: x,
  //   y: y,
  // };

 //  var closest_x = x.reduce(function(prev, curr) {
 //    return (Math.abs(curr - belief_mu) < Math.abs(prev - belief_mu) ? curr : prev);
 //  });
  
 //  var closest_x_small = x.reduce(function(prev, curr) {
 //    return (Math.abs(curr - 0.05) < Math.abs(prev - 0.05) ? curr : prev);
 //  });

 // var closest_x_large = x.reduce(function(prev, curr) {
 //    return (Math.abs(curr - 0.95) < Math.abs(prev - 0.95) ? curr : prev);
 //  });

  var trace_1 = {
    x: x,
    y: y,
    type: 'scatter',
    fill: 'tozeroy',
    mode: 'lines'
  };

  var data = [ trace_1 ];
  var layout = {
    hovermode: false,
    yaxis: {
      range: [0, 1],
      fixedrange: true,
      showgrid: false,
      showaxis: false, 
      showticks: false,
      zeroline: false, 
      showticklabels: false},
      xaxis: {
        font:{size:15},
        fixedrange: true,
        showgrid: false,
        zeroline: false, 
        tickvals: [.01, .5, .99],
        ticktext: ["   " + name_1, 'neutral', name_2 + "   "], 
        range: [0,1]},
    autosize:false,
    width: 550, 
    height: 550/1.6,     
    title: title_name,
    showlegend: false,

    shapes: [{type: 'line', x0: belief_mu, x1: belief_mu,
              line: {color:'black', width : 3}}],
  };
  Plotly.newPlot(plot_div, data, layout, {displayModeBar: false}, {staticPlot: true});
};












