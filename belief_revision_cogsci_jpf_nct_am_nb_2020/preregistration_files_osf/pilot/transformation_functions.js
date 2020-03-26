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


// transforming the confidence value scale into log space. the fact that the maxv is larger than the 
// value scale maxv (i.e. 1000 vs 120) prevents that participants can respond with too high confidence values.
// note that values around 150 on the value scale usually result in a and b parameters of > 500 which will produce NaN values in later computations (too small numbers)
var log_slider = function(slid_val){
    var slid_val = 1000 - slid_val;
    var minp = 0;
    var maxp = 1000;
    var minv = Math.log(0.00000000000000001);
    var maxv = Math.log(0.08333333333333333); // variance for b(1,1) is our upper bound for variance 
    var scale_adjust = (maxv-minv) / (maxp-minp);
    var variance = Math.exp(minv + scale_adjust*(slid_val-minp));
    return variance;
};


// transforming the variance back into the confidence slider value 
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


//  function showing how variance for beta pdf is computed (just as reminder)
var var_beta = function(a, b){
    return (a * b)/((a + b)**2 * (a+b+1))
};

// estimating alpha and beta parameters based on mu and variance 
var est_beta_par = function (mu, variance) {
  var alpha = mu * (mu * (1 - mu) / variance - 1);
  var beta = alpha * (1 - mu) / mu; 
  // setting minimum parameter values to 1 
  alpha = Math.max(alpha, 1);
  beta = Math.max(beta, 1);
  return [alpha, beta] 
};