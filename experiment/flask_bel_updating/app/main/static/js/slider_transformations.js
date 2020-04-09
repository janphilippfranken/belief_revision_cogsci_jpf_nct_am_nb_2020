// // used for transforming slider values into the beta statistics and vice versa 

// //  transforming 1-99 confidence scale into 1-80 confidence scale
// var transform_con_slider_pos = function(position){
//     var minp = 1;
//     var maxp = 99;
//     var minv = 0;
//     var maxv = 80;
//     var scale_adjust = (maxv- minv) / (maxp - minp);
//     var slid_val= (minv + scale_adjust * (position - minp));
//     return slid_val;
// };


// //  transforming 1-99 belief scale into 5-95 elief scale
// var transform_bel_slider_pos = function(position){
//     var minp = 1;
//     var maxp = 99;
//     var minv = 5;
//     var maxv = 95;
//     var scale_adjust = (maxv - minv) / (maxp - minp);
//     var slid_val = minv + scale_adjust * (position - minp);
//     return slid_val;
// };


// //  log slider for variance computation based on confidence value
// var log_slider = function(slid_val){
//     var slid_val = 80 - slid_val;
//     var minp = 0;
//     var maxp = 80;
//     var minv = Math.log(0.00000000000000001);
//     var maxv = Math.log(0.08333333333333333);
//     var scale_adjust = (maxv-minv) / (maxp-minp);
//     var variance = Math.exp(minv + scale_adjust*(slid_val-minp));
//     return variance;
// };


// //  function showing how variance for beta pdf is computed (just as reminder)
// var var_beta = function(a, b){
//     return (a * b)/((a + b)**2 * (a+b+1))
// };


// // transforming the var back into the confidence slider value 
// var inverse_log_slider = function(variance){
//     var variance = Math.log(variance); 
//     var minv = Math.log(0.00000000000000001);
//     var maxv = Math.log(0.08333333333333333);
//     var minp = 0;
//     var maxp = 80;     
//     var scale_adjust = (maxp - minp) / (maxv - minv)
//     var slid_val = minp + scale_adjust * (variance - minv);
//     return (80 - slid_val);
// };

    
// // transforming the confidence slider value back into the confidence slider position
// var transform_con_slider_val = function(slid_val){
//     var minv = 0;
//     var maxv = 80;
//     var minp = 1;
//     var maxp = 99;
//     var scale_adjust = (maxp- minp) / (maxv - minv);
//     var position = (minp + scale_adjust * (slid_val - minv));
//     return position;
// };

// // transforming the bel slider value back into the bel slider position
// var transform_bel_slider_val = function(slid_val){ 
//     var minv = 5;
//     var maxv = 95;
//     var minp = 1;
//     var maxp = 99;
//     var scale_adjust = (maxp- minp) / (maxv - minv);
//     var position = (minp + scale_adjust * (slid_val - minv));
//     return position;
// };

// // parameters of agents 
// var agent_parameters = [[3,2],[2,3],[5,3],[4,4],[2,3],
//                         [2,3],[2,6],[3,5],[5,5],[2,3]];

// //  computing mean and variance based on agent parameters 
// var compute_agent_stats = function(agent_parameters){
//     var agent_stats = [];
//     for (var i=0; i < agent_parameters.length; i++){
//         var alpha = agent_parameters[i][0];
//         var beta = agent_parameters[i][1];
//         var mean = jStat.beta.mean(alpha, beta);
//         var variance = jStat.beta.variance(alpha, beta);
//         agent_stats.push([mean, variance]);
//     };
//     return agent_stats;
// };


// used for transforming slider values into the beta statistics and vice versa 

// transforming 1-99 confidence position scale into 1-100 confidence value scale
var transform_con_slider_pos = function(position){
    var minp = 1;
    var maxp = 99;
    var minv = 0;
    var maxv = 120;
    var scale_adjust = (maxv- minv) / (maxp - minp);
    var slid_val= (minv + scale_adjust * (position - minp));
    return slid_val;
};


//  transforming 1-99 belief position scale into 5-95 belief value scale 
var transform_bel_slider_pos = function(position){
    var minp = 1;
    var maxp = 99;
    var minv = 5;
    var maxv = 95;
    var scale_adjust = (maxv - minv) / (maxp - minp);
    var slid_val = minv + scale_adjust * (position - minp);
    return slid_val;
};


//  log slider for variance computation based on confidence value. The fact that the max is larger than the 
// value scale (i.e. 0-850 vs 0-100) prevents that participants can respond with too high confidence values.
// note that values around 150 on the value scale usually result in a and b parameters of > 500 which will produce NaN values in later computations (too small numbers)
var log_slider = function(slid_val){
    var slid_val = 1000 - slid_val;
    var minp = 0;
    var maxp = 1000;
    var minv = Math.log(0.00000000000000001);
    var maxv = Math.log(0.08333333333333333); // variance for b(1,1)
    var scale_adjust = (maxv-minv) / (maxp-minp);
    var variance = Math.exp(minv + scale_adjust*(slid_val-minp));
    return variance;
};


//  function showing how variance for beta pdf is computed (just as reminder)
var var_beta = function(a, b){
    return (a * b)/((a + b)**2 * (a+b+1))
};

// transforming the var back into the confidence slider value 
var inverse_log_slider = function(variance){
    var variance = Math.log(variance); 
    var minv = Math.log(0.00000000000000001);
    var maxv = Math.log(0.08333333333333333);
    var minp = 0;
    var maxp = 1000;     
    var scale_adjust = (maxp - minp) / (maxv - minv)
    var slid_val = minp + scale_adjust * (variance - minv);
    return (1000 - slid_val);
};

    
// transforming the confidence slider value back into the confidence slider position 
var transform_con_slider_val = function(slid_val){
    var minv = 0;
    var maxv = 120;
    var minp = 1;
    var maxp = 99;
    var scale_adjust = (maxp- minp) / (maxv - minv);
    var position = (minp + scale_adjust * (slid_val - minv));
    return position;
};

// transforming the bel slider value back into the bel slider position
var transform_bel_slider_val = function(slid_val){ 
    var minv = 5;
    var maxv = 95;
    var minp = 1;
    var maxp = 99;
    var scale_adjust = (maxp- minp) / (maxv - minv);
    var position = (minp + scale_adjust * (slid_val - minv));
    return position; 
};

// // parameters of agents 
// var agent_parameters = [[3,2],[2,3],[5,3],[4,4],[2,3],
//                         [2,3],[2,6],[3,5],[5,5],[2,3]];
 
// //  computing mean and variance based on agent parameters 
// var compute_agent_stats = function(agent_parameters){
//     var agent_stats = [];
//     for (var i=0; i < agent_parameters.length; i++){
//         var alpha = agent_parameters[i][0];
//         var beta = agent_parameters[i][1];
//         var mean = jStat.beta.mean(alpha, beta);
//         var variance = jStat.beta.variance(alpha, beta);
//         agent_stats.push([mean, variance]);
//     };
//     return agent_stats;
// };