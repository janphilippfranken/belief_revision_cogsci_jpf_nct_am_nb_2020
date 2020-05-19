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
  a = Math.min(alpha, 500);
  b = Math.min(beta, 500);
  var step = (stop_val - start_val) / (cardinality - 1);
  for (var i = 0; i < cardinality; i++) {
    x = start_val + (step * i);
    y = jStat.beta.pdf(x, alpha, beta);
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

// creating the beta pdf plot used in the main task
var create_plot = function(x, y, belief_mu, plot_div, name_1, name_2, size, title_name, confidence, plot_type) {
  var arr_diff = [];
  var bel = 'Belief: ';
  var con = 'Certainty: ';
  var text_name = '';
  var arrow = false;
  var scale_height = 1.6;
  if (plot_type == '1') {
    var belief_str = bel.concat(Math.round(transform_bel_slider_val(belief_mu * 100)));
    var con_str = con.concat(confidence);
    arrow = false;
    scale_height = 1.3;
    text_name = "<b>" + title_name + "'s</b> rating:<br>" + belief_str + "<br>" + con_str;
  };
  if (title_name == "Your") {
    belief_str = 'Belief: ' + $('#beliefOutputId_3').text();
    con_str = "Certainty: "+ $('#confidenceOutputId_3').text();
    text_name = "<b>Your initial recommendation</b>:<br>" + belief_str + "<br>" + con_str;
  };

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

  // var trace_1 = {
  //   x: x.slice(x.indexOf(closest_x_small), x.indexOf(closest_x)),
  //   y: y.slice(x.indexOf(closest_x_small), x.indexOf(closest_x)),
  //   type: 'scatter',
  //   fill: 'tozeroy',
  //   mode: 'lines',
  //   line:{color:'orange'}
  // };

  // array1.indexOf(Math.max(...array1))

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
    line:{color:'purple'}
  };

  var data = [ trace_1, trace_2 ];

  var layout = {
    tracetoggle: false,
    hovermode: false,
    yaxis: {
      range: [0, 13],
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
        ticktext: ["   " + "<b>" + name_1 + "</b>", 'neutral', "<b>" + name_2 + "</b>  "], 
        range: [0,1]},

    shapes: [{type: 'line', x0: belief_mu, x1: belief_mu, y0:0, y1:y[min_diff_index],
                               line: {color:'black', width : 3}
                               }],

    // shapes: [{type: 'line', x0: mode, x1: mode, y0:0, y1:y[min_diff_index],
    //                            line: {color:'black', width : 3}
    //                            }],

    autosize:false,
    width: size,
    height: size/scale_height,     
    title: { 
      text: text_name, x:0.2,
      font: {size: 14}},
    showlegend: false
    // annotations: [
    // {
    //   x: 0.5,
    //   y: 11, // y[x.indexOf(belief_mu)]
    //   font: {size:15},
    //   xref: 'x',
    //   yref: 'y', 
    //   text: text_name,
    //   showarrow: arrow,   
    //   arrowhead: 2,
    //   ax: 0,
    //   ay: -45,
    // }]
  };
  Plotly.newPlot(plot_div, data, layout, {displayModeBar: false}, {staticPlot: true});
};


// creating the beta pdf plot used in the beginning
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
        ticktext: ["   " + "<b>" + name_1 + "</b>", 'neutral', "<b>" + name_2 + "</b>  "], 
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







