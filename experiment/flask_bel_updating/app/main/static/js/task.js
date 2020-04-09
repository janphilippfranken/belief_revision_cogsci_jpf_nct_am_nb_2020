
////////////////////////////////////////
// Main task js
// //////////////////////////////////////


// Definition of variables 
//////////////////////////
var conditions = [];         // to be populated by stim.json
var rand_cond_order = [];    // to be populated by stim.json
var start_time = new Date(); 
var start_task_time;
var end_time;
var case_counter = 0; 
var condition_counter = 0;   // counts which condition is currently displayed; random order for each participant 
var trial_counter = 0;		 // counts which trial is shown in the present condition; random order within each condition 
var random_result = [];  	 // random result (i.e. which candidate succeeded on a test); random order of successes but deterministic outcomes 
var random_results = [];     // list of all random results
var rand_res_stored = [];    // short version of results written to database later (i.e. coded as 0s and 1s)
var responses = []; 		 // participant responses. Note - these correspond to the values of the sliders, not to the positions displayed to participants. see slider_transformations.js for details on values 


// randomising the position of the candidate that locals support; 0 means left, and 1 means right 
// Note that that parameters of locals are flipped according to the position of the candidate
var random_pos_winner = _.sample([0,1]) 


// variables for drawing the networks on the canvas board 
var nodes = ['node1', 'node2'];
var lines = ['line1', 'line2']; 
var legs = ['legl1', 'legr1', 'legl2', 'legr2'];
var arms = ['arml1', 'armr1', 'arml2', 'armr2'];
var bodies = ['body1', 'body2'];
var arrows = ['arrow1', 'arrow2'];
var vs = ['vs'];


// Token generator and populating variables
///////////////////////////////////////////

// generating toke displayed to participant (stolen from bonan)
var generateToken = function(length) {
    let tokens = '';
    let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    for (let i = 0; i < length; i ++) {
        tokens += chars.charAt(Math.floor(Math.random() * chars.length))
    }
    return tokens;
};

var token_id = generateToken(10);
 

// getting stimuli from stim.json file 
fetch(root_string + "/static/json/stim.json") 
.then(function(response) {
    return response.json();
  })
.then(function(myJson) {
		conditions = _.shuffle(myJson.conditions); // random order of conditions
		var i = 0; 
		while (i < 3) {   // random order of results (i.e. which candidate one a test)
			possible_results = conditions[i][3];
			rand_cond_order.push(conditions[i][8])
			rand_res_stored.push(_.shuffle(conditions[i][9][random_pos_winner]))
			for(var i_2=0; i_2 < 2; i_2++) {
				random_result = possible_results[rand_res_stored[i][i_2]];
				random_results.push(random_result)
			}; 
			i++
		};
	
})
.catch( (error) => console.log(error) );
 


/////////////////////////////////
// INSTRUCTIONS AND COMPREHENSION
/////////////////////////////////

$('#overview_1').scroll(function() {   // button enabler  
    if ($(this)[0].scrollHeight - $(this).scrollTop() <= $(this).outerHeight()) {
       	$('#ins1btn').prop('disabled',false);
    }
}); 


$('#ins1btn').click(function () {
	$('#ins1').hide();
	$('#ins2').show();
	// drawing first instance of example candidates on the canvas board (see draw_network_js)
	generate_network('network_graph1', 675, 75, nodes[0], vs[0], legs[0], legs[1], arms[0], arms[1], bodies[0], lines[0], arrows[0], -1, 'test', 'Taylor');
	generate_network('network_graph1', 125, 75, nodes[1], vs[0], legs[2], legs[3], arms[3], arms[4], bodies[1], lines[1], arrows[1], 1, 'test', 'Morrison');
});


$('#overview_2').scroll(function() {   // button enabler 
    if ($(this)[0].scrollHeight - $(this).scrollTop() <= $(this).outerHeight()) {
       	$('#ins2btn').prop('disabled',false);
    }
});


$('#ins2btn').click(function () {
	$('#ins2').hide();
	$('#ins3').show();
	show_success('network_graph1', random_results[case_counter][1][0], 145);
	show_success('network_graph1', random_results[case_counter][1][1], 145);
	//  creating initial bar that can be moved to show how belief is rated 
	var x_1 = create_data(0.5, 0.005)[0];	// see create_beta_plots.js for details about data creation and plot functions
	var y_1 = create_data(0.5, 0.005)[1];
	create_plot_start(x_1, y_1, 0.5, 'ins_bel_plot', 'Morrison', 'Taylor');
	create_plot_start(x, y, 0.5, 'ins_bel_plot', 'Morrison', 'Taylor');
	var $belief=$('#belief_slider_1'); 
	$belief.on('input',function(x_1, y_1){
	    var belief = parseInt($belief.val());
	    create_plot_start(x_1, y_1, belief/100, 'ins_bel_plot', 'Morrison', 'Taylor', ""); 
	});
});


$('#test_performance_btn').click(function () {
	$('#test_performance_btn').hide();
	$('#test_result').show();
	$('#ins3btn').show();
	show_success('network_graph1', 650, 155);
	create_plot_start(x, y, 0.5, 'ins_bel_plot', 'Morrison', 'Taylor');
});

 
$('#ins3btn').click(function () {
		$('#ins4').show();
		$('#ins2').hide();
		$('#ins3').hide(); 
});


// onlys allow to proceed if slider set to requested value 
$('#ins4btn').click(function() {
	var slid = $('#beliefOutputId_1').text();
	if (slid == 66) {
		responses.push($('#belief_slider_1').val());
		$('#ins4').hide();
		$('#ins5').show();
		$('#network_graph1').hide();
		var x = create_data($('#belief_slider_1').val()/100, 0.084)[0]; 
		var y = create_data($('#belief_slider_1').val()/100, 0.084)[1];
		create_plot(x, y, $('#belief_slider_1').val()/100, 'ins_con_plot', 'Morrison', 'Taylor', 550, "", "", '2'); 
		var $confidence=$('#confidence_slider_1');
		$confidence.on('input',function(){
			var variance = log_slider(transform_con_slider_pos(parseInt($confidence.val())));
			var x = create_data($('#belief_slider_1').val()/100, variance)[0];
			var y = create_data($('#belief_slider_1').val()/100, variance)[1];
			create_plot(x, y, $('#belief_slider_1').val()/100, 'ins_con_plot', 'Morrison', 'Taylor', 550, "", "", '2');
		});
	} else {
		alert('You are not using the slider correctly. Try setting your belief to 66!')
	}
});


$('#ins5btn').click(function() {
	var slid = $('#confidenceOutputId_1').text(); 
	if (slid == 10) {
		responses.push(transform_con_slider_pos($('#confidence_slider_1').val())); 
		$('#ins6').show();
		$('#ins5').hide();
		// drawing first instance of example voters on the canvas board (see draw_network_js)
		// generate_network('network_graph2', 675, 75, nodes[0], vs[0], legs[0], legs[1], arms[0], arms[1], bodies[0], lines[0], arrows[0], -1, 'test', 'Bob');
		// generate_network('network_graph2', 125, 75, nodes[1], vs[0], legs[2], legs[3], arms[3], arms[4], bodies[1], lines[1], arrows[1], 1, 'test', 'Alice');

		// TODO : need to make this prettier in a function 
		var alpha_1 = 40;
		var alpha_2 = 45;
		var alpha_3 = 45;

		var beta_1 = 20;
		var beta_2 = 40;
		var beta_3 = 28;


		var mean_1 = jStat.beta.mean(alpha_1, beta_1);
		var mean_2 = jStat.beta.mean(alpha_2, beta_2);
		var mean_3 = jStat.beta.mean(alpha_3, beta_3);
		var variance_1 = jStat.beta.variance(alpha_1, beta_1);
		var variance_2 = jStat.beta.variance(alpha_2, beta_2); 
		var variance_3 = jStat.beta.variance(alpha_3, beta_3); 

		var con_slid_val_1 = inverse_log_slider(variance_1); 
		var con_slid_val_2 = inverse_log_slider(variance_2); 
		var con_slid_val_3 = inverse_log_slider(variance_3); 
		var con_slid_pos_1 = transform_con_slider_val(con_slid_val_1);
		var con_slid_pos_2 = transform_con_slider_val(con_slid_val_2);
		var con_slid_pos_3 = transform_con_slider_val(con_slid_val_3);

		var x_1 = create_arrays(0.01, .99, 1000, alpha_1, beta_1)[0];
		var y_1 = create_arrays(0.01, .99, 1000, alpha_1, beta_1)[1];
		var x_2 = create_arrays(0.01, .99, 1000, alpha_2, beta_2)[0];
		var y_2 = create_arrays(0.01, .99, 1000, alpha_2, beta_2)[1];
		var x_3 = create_arrays(0.01, .99, 1000, alpha_3, beta_3)[0];
		var y_3 = create_arrays(0.01, .99, 1000, alpha_3, beta_3)[1];

		create_plot(x_1, y_1, mean_1.toFixed(2), 'local_1_plot_intro', 'Morrison', 'Taylor', 350, "Alice", (Math.round(con_slid_pos_1)).toString(), '1');
		create_plot(x_2, y_2, mean_2.toFixed(2), 'local_2_plot_intro', 'Morrison', 'Taylor', 350, "Bob", (Math.round(con_slid_pos_2)).toString(), '1');
		create_plot(x_3, y_3, mean_3.toFixed(2), 'local_3_plot_intro', 'Morrison', 'Taylor', 350, "Paul", (Math.round(con_slid_pos_3)).toString(), '1');
	} else {
		alert('You are not using the slider correctly. Try setting certainty to 10')
	}
});


$('#focus_group_info').scroll(function() {
    if ($(this)[0].scrollHeight - $(this).scrollTop() <= $(this).outerHeight()) {
       	$('#ins6btn').prop('disabled',false);
    }
});


$('#ins6btn').click(function() {
	$('#ins6').hide(); 
	$('#ins7').show();
	plot_distributions('belief_slider_2', 'confidence_slider_2', $('#belief_slider_1').val(), transform_con_slider_pos(10), 'ins_full_plot', 'Morrison', 'Taylor', "");

});


// $('#ins7btn').click(function() {
// 	$('#ins7').hide();
// 	$('#ins8').show();
// });


var $confidence=$('#confidence_slider_2');  // only allow to proceed if participants moved the confidence slider to prevent instant pressing of continue
		$confidence.on('change',function(){
		$('#ins8btn').prop('disabled',false);;
		});


$('#ins8btn').click(function() {  
	$('#ins7').hide();
	$('#ins9').show(); 
	responses.push($('#belief_slider_2').val()); 
	responses.push(transform_con_slider_pos($('#confidence_slider_2').val())); 

});


$('#instructions_summary').scroll(function() {   // show instructions  button 1 only if scrolled 
    if ($(this)[0].scrollHeight - $(this).scrollTop() <= $(this).outerHeight()) {
       	$('#ins9btn').prop('disabled',false);
    }
});


$('#ins9btn').click(function() {
	$('#ins9').hide();
	$('#comprehension').show(); 
});


// COMPREHENSION QUIZ
// Check whether all questuions are correct 
var comp_checker = function() {
	$('#done_comp').show();
	//Pull the selected values
	var q1 = $('#comp_q1').val();
	var q2 = $('#comp_q2').val();
	var q3 = $('#comp_q3').val();
	var q4 = $('#comp_q4').val();
	var q5 = $('#comp_q5').val();
	var q6 = $('#comp_q6').val();

   // Add the correct answers here
   answers = ["true", "true", "false", "true", "true", "false"];

   if(q1 == answers[0] && q2 == answers[1] && q3 == answers[2] && q4 == answers[3] && q5 == answers[4] && q6 == answers[5]){
   		// Allow the start
        alert('You got everything correct! Press "Start" to begin the experiment.'); 
        $('#done_comp').show();
        $('#comp_check_btn').hide();
    } else {
    	// Throw them back to the start of the instructions
    	// Remove their answers and have them go through again
		alert('You answered at least one question incorrectly! Please try again.');
 
    	$('#comp_q1').prop('selectedIndex', 0);
    	$('#comp_q2').prop('selectedIndex', 0);
    	$('#comp_q3').prop('selectedIndex', 0);
    	$('#comp_q4').prop('selectedIndex', 0);
    	$('#comp_q5').prop('selectedIndex', 0);
    	$('#comp_q6').prop('selectedIndex', 0);
    	$('#done_comp').hide();
    	$('#comp_check_btn').show(); 
    	$('#ins1').show();
		$('#comprehension').hide();
    };
}


// Checks whether all questions were answered
var 
comp_change_checker = function() {
	var q1 = $('#comp_q1').val();
	var q2 = $('#comp_q2').val();
	var q3 = $('#comp_q3').val();
	var q4 = $('#comp_q4').val();
	var q5 = $('#comp_q5').val();
	var q6 = $('#comp_q6').val();

	//Make sure start button is disabled because the answers haven't been checked
	$('#done_comp').hide();

 	//Only release the check button if there is a response on all questions
	if (q1 === 'noresp' || q2 === 'noresp' || q3 === 'noresp' || q4 === 'noresp' || q5 == 'noresp' || q6 == 'noresp')
	{
		$('#comp_check_btn').hide();
	} else {
		$('#comp_check_btn').show();
	}
};


// Start the main task function (just causes a refresh)
$('#done_comp').click(function () {
	console.log('STARTING TASK');
	goto_task();
});


// Listen for actions on radio buttons for when all questions answered
$('.comp_questions').change(function() {
	comp_change_checker();
});


// Answer checker function
$('#comp_check_btn').click(function () { 
	comp_checker();
});



////////////
// MAIN TASK
////////////

// brief reminder and start of task
$('#main_task_intro_btn').click(function() {
	$('#main_task').show();
	$('#main_task_intro').hide();
	$('#instructions').hide();
	start_task_time = new Date();
	show_success('network_graph3', random_results[case_counter][1][0], 145);
	show_success('network_graph3', random_results[case_counter][1][1], 145);

	// successSign.strokeStyle="#000000";
	// successSign.beginPath(); 
	// successSign.setLineDash([0]);
	// successSign.arc(x + 35 * shift, 155, 15, 0, 2 * Math.PI);
	// successSign.font = "60px Comic Sans MS";
	// successSign.fillStyle = "green";
	// successSign.textAlign = "center";
	// successSign.closePath();
	// successSign.fill();
});


// Conditions
///////////////

// 1) Tests phase and initial assessment
///////////////////////////////////////

// first test
$('#scenario_1_case_1_btn').click(function() { 
	$('#scenario_1_case_1_results').show();
	show_success('network_graph3', random_results[case_counter][1][2], 155);
	$('#scenario_1_case_1').hide();
});


$('#scenario_1_case_1_res_btn').click(function() {
	$('#scenario_1_case_1_results').hide();
	// clear_success('network_graph3', random_results[case_counter][1][random_pos_winner], 225);
	$('#scenario_1_case_2').show();
});


// second test 
$('#scenario_1_case_2_btn').click(function() {
	$('#scenario_1_case_2_results').show();
	show_success('network_graph3', random_results[case_counter][1][3], 155);
	$('#scenario_1_case_2').hide();
});

$('#scenario_1_case_2_res_btn').click(function() {
	$('#scenario_1_case_2_results').hide();
	// clear_success('network_graph3', random_results[case_counter + 1][1][random_pos_winner], 225);
	// $('#network_graph3').hide();
	var bel_slider_pos = transform_bel_slider_pos(50);
	var con_slider_pos = transform_con_slider_pos(1);
	name_1 = conditions[condition_counter][3][0][0];
	name_2 = conditions[condition_counter][3][1][0];
	plot_distributions('belief_slider_3', 'confidence_slider_3', bel_slider_pos, con_slider_pos, 'post_1_plot', name_1, name_2);
	$('#post_1_plot_wrapper').show();
	// $('#scenario_1_1').hide(); 
	$('#scenario_1_1_background').hide();
	$('#scenario_1_1_head').hide();
	$('#initial_recommendation_head').show();
	$('#initial_recommendation_instruct').show();
	$('#scenario_1_2_btn').show();
}); 


// 2) Provide Posterior 
/////////////////////////
$('#scenario_1_2_btn').click(function() {
	if ($('#beliefOutputId_3').text() != 'move slider to rate belief' && $('#confidenceOutputId_3').text() != 'move slider to rate how certain you are about your belief') {
		$('#scenario_1_1_background').show();
		$('#scenario_1_1_head').show();
		$('#initial_recommendation_head').hide();
		$('#initial_recommendation_instruct').hide();
		$('#scenario_1_1').hide();
		$('#scenario_1_3').show(); 
		$('#post_1_plot_wrapper').hide();
		$('#scenario_1_2_btn').hide();
		// update_scenario('network_graph4', condition_counter, trial_counter, 'neighbours');
		store_responses('round_1');	
		$('#focus_group_setup').show();
		$(conditions[condition_counter][0]).show();
		// setting text in html placeholder divs based on results and condition 
		document.getElementById('name_of_local_1_1').innerHTML = conditions[condition_counter][4][0];
		document.getElementById('name_of_local_1_2').innerHTML = conditions[condition_counter][4][0];
		// document.getElementById('name_of_local_1_3').innerHTML = conditions[condition_counter][5][1][random_pos_winner];
		document.getElementById('name_of_local_2_1').innerHTML = conditions[condition_counter][4][1];
		document.getElementById('name_of_local_2_2').innerHTML = conditions[condition_counter][4][1];

		document.getElementById('name_of_local_3_1').innerHTML = conditions[condition_counter][4][2];
		document.getElementById('name_of_local_3_2').innerHTML = conditions[condition_counter][4][2];
		// document.getElementById('name_of_local_2_3').innerHTML = conditions[condition_counter][6][1][random_pos_winner];   
		$("#focus_group_scroll").scrollTop(0);
		$('#focus_group_scroll').scroll(function() {   // show instructions  button 1 only if scrolled 
		    if ($(this)[0].scrollHeight - $(this).scrollTop() <= $(this).outerHeight()) { 
		       	$('#scenario_1_3_1_btn').prop('disabled',false);
		    }
		});
	} else {
		alert('Please make sure that you provide your advice!')
	}; 
});  


// 3) Interview locals
////////////////////////
$('#scenario_1_3_1_btn').click(function() {
	$("#focus_group_scroll").scrollTop(0);
	$('#intro').hide();
	$('#background_info').hide();
	$('#background_info_2').show();
	// $('#network_graph4').hide();
	$('#focus_group_plots').show();
	$('#prior_plot').show();
	$('#interview_head_1').hide();
	$('#interview_head_2').show();
	$('#post_plot_2_wrapper').show();
	$('#scenario_1_3_2_btn').hide();
	$('#scenario_1_3_1_btn').show();
	$('#background_info_2').hide();
	$('#background_info_const').hide();
	$('#final_recommendation').show();
	$(conditions[condition_counter][10]).show();
	$(conditions[condition_counter][0]).hide(); 
	// $('#results').hide();
	var bel_slider_pos = $('#belief_slider_3').val();
	var con_slider_pos = $('#confidence_slider_3').val();
	name_1 = conditions[condition_counter][3][0][0];
	name_2 = conditions[condition_counter][3][1][0];
	document.getElementById('beliefOutputId_4').innerHTML = 'move slider to rate belief';
	document.getElementById('confidenceOutputId_4').innerHTML = 'move slider to rate how certain you are about your belief';
	$('#scenario_1_3_1_btn').prop('disabled',false);	
	// document.getElementById('focus_group_results').innerHTML = conditions[condition_counter][6];

	//  still has to be changed to be more elegant than this just a test if everything works as it should
	var alpha_1 = conditions[condition_counter][5][0][random_pos_winner][0];
	var alpha_2 = conditions[condition_counter][6][0][random_pos_winner][0];
	var alpha_3 = conditions[condition_counter][7][0][random_pos_winner][0];
	var alpha_4 = est_beta_par($('#belief_slider_3').val()/100, log_slider(transform_con_slider_pos($('#confidence_slider_3').val())))[0];	
	var beta_1 = conditions[condition_counter][5][0][random_pos_winner][1];
	var beta_2 = conditions[condition_counter][6][0][random_pos_winner][1];
	var beta_3 = conditions[condition_counter][7][0][random_pos_winner][1];
	var beta_4 = est_beta_par($('#belief_slider_3').val()/100, log_slider(transform_con_slider_pos($('#confidence_slider_3').val())))[1];


	var x_1 = create_arrays(0.01, .99, 1000, alpha_1, beta_1)[0];
	var y_1 = create_arrays(0.01, .99, 1000, alpha_1, beta_1)[1];
	var x_2 = create_arrays(0.01, .99, 1000, alpha_2, beta_2)[0];
	var y_2 = create_arrays(0.01, .99, 1000, alpha_2, beta_2)[1];
	var x_3 = create_arrays(0.01, .99, 1000, alpha_3, beta_3)[0];
	var y_3 = create_arrays(0.01, .99, 1000, alpha_3, beta_3)[1];
	var x_4 = create_arrays(0.01, .99, 1000, alpha_4, beta_4)[0];
	var y_4 = create_arrays(0.01, .99, 1000, alpha_4, beta_4)[1];


	var mean_1 = jStat.beta.mean(alpha_1, beta_1);
	var mean_2 = jStat.beta.mean(alpha_2, beta_2);
	var mean_3 = jStat.beta.mean(alpha_3, beta_3);
	var mean_4 = jStat.beta.mean(alpha_4, beta_4);
	var variance_1 = jStat.beta.variance(alpha_1, beta_1);
	var variance_2 = jStat.beta.variance(alpha_2, beta_2); 
	var variance_3 = jStat.beta.variance(alpha_3, beta_3); 
	var variance_4 = jStat.beta.variance(alpha_4, beta_4); 

	var con_slid_val_1 = inverse_log_slider(variance_1); 
	var con_slid_val_2 = inverse_log_slider(variance_2); 
	var con_slid_val_3 = inverse_log_slider(variance_3); 
	var con_slid_val_4 = inverse_log_slider(variance_4); 
	var con_slid_pos_1 = transform_con_slider_val(con_slid_val_1);
	var con_slid_pos_2 = transform_con_slider_val(con_slid_val_2);
	var con_slid_pos_3 = transform_con_slider_val(con_slid_val_3); 
	var con_slid_pos_4 = transform_con_slider_val(con_slid_val_4); 
 
	create_plot(x_1, y_1, mean_1.toFixed(2),'local_1_plot', conditions[condition_counter][3][0][0], conditions[condition_counter][3][1][0], 350, conditions[condition_counter][4][0], (Math.round(con_slid_pos_1)).toString(), '1');
	create_plot(x_3, y_3, mean_3.toFixed(2),'local_2_plot', conditions[condition_counter][3][0][0], conditions[condition_counter][3][1][0], 350, conditions[condition_counter][4][2], (Math.round(con_slid_pos_3)).toString(), '1');
	create_plot(x_2, y_2, mean_2.toFixed(2), 'local_3_plot', conditions[condition_counter][3][0][0], conditions[condition_counter][3][1][0], 350, conditions[condition_counter][4][1], (Math.round(con_slid_pos_2)).toString(), '1');
	create_plot(x_4, y_4, mean_4.toFixed(2), 'prior_plot_1', conditions[condition_counter][3][0][0], conditions[condition_counter][3][1][0], 350, "Your", (Math.round(con_slid_pos_4)).toString(), '1');
	
    var bel_slider_pos = transform_bel_slider_pos(50);
	var con_slider_pos = transform_con_slider_pos(1);
	plot_distributions('belief_slider_4', 'confidence_slider_4', bel_slider_pos, con_slider_pos, 'post_2_plot', name_1, name_2);
	draw_network_plotly('illustration_graph_1', 'placeholder_name_1', 'placeholder_name_2','placeholder_name_3', conditions[condition_counter][8])


	$('#scenario_1_4_btn').show();
	$('#scenario_1_3_1_btn').hide(); 
	// $('#results').show();
	$('#focus_group_scroll').scroll(function() {   // show instructions  button 1 only if scrolled 
		    if ($(this)[0].scrollHeight - $(this).scrollTop() <= $(this).outerHeight()) {
		       	$('#scenario_1_3_2_btn').prop('disabled',false);
		    }
		});
});


$('#scenario_1_3_2_btn').click(function() {
	// $('#scenario_1_3_2_btn').hide();
	// $('#scenario_1_3_1_btn').show();
	// $(conditions[condition_counter][0]).hide();
	// $('#intro').show(); 
	// $('#results').hide();
	// $('#network_graph4').show();
	// $('#scenario_1_3').hide();
	// var bel_slider_pos = $('#belief_slider_3').val();
	// var con_slider_pos = $('#confidence_slider_3').val();
	// name_1 = conditions[condition_counter][3][0][0];
	// name_2 = conditions[condition_counter][3][1][0];
	// plot_distributions('belief_slider_4', 'confidence_slider_4', bel_slider_pos, con_slider_pos, 'post_2_plot', name_1, name_2);
	// document.getElementById('beliefOutputId_4').innerHTML = $('#beliefOutputId_3').text();
	// document.getElementById('confidenceOutputId_4').innerHTML = $('#confidenceOutputId_3').text();
	// $('#scenario_1_3_1_btn').prop('disabled',true);	
});


// 4) Provide new Posterior (now accounting for impact of locals)
////////////////////////////////////////////////////////////////////////
$('#scenario_1_4_btn').click(function() {
	$('#intro').show();
	$('#final_recommendation').hide();
	$(conditions[condition_counter][10]).hide();
	// $('#network_graph4').show();
	$('#scenario_1_3_2_btn').prop('disabled',true);
	$('#focus_group_plots').hide();
	$('#prior_plot').hide();
	$('#background_info_2').hide();
	$('#background_info').show();
	store_responses('round_2');
	advance_trial();	
	$('#scenario_1_3').hide();
	$('#scenario_1_4_btn').hide();
	$('#post_plot_2_wrapper').hide();
	$('#scenario_1_3_1_btn').show();
	$('#scenario_1_5').show();
	$('#scenario_1_1_head').show();
	$('#scenario_1_case_1').show();	 
	$('#interview_head_2').hide();
	$('#interview_head_1').show();
	// $('#results').hide();
	$('#background_info_const').show();
	document.getElementById('beliefOutputId_3').innerHTML = 'move slider to rate belief';
	document.getElementById('confidenceOutputId_3').innerHTML = 'move slider to rate how certain you are about your belief';
});


$('#scenario_1_5_btn').click(function() {
 $('#scenario_1_5').hide();
 $('#scenario_1_1').show();
 $('#scenario_1_4_btn').prop('disabled',true);
});


////////////
// FUNCTIONS
////////////

// A) Generic functions for switching between instructions, task, and debriefing 
//////////////////////////////////////////////////////////////////////////////// 
var advance_trial = function() {
	trial_counter++;
	if (trial_counter<conditions.length)
	{
		condition_counter = condition_counter + 1;
		case_counter = case_counter + 2;
		update_scenario('network_graph3', condition_counter, case_counter, 'not-neighbours');
		show_success('network_graph3', random_results[case_counter][1][0], 145);
		show_success('network_graph3', random_results[case_counter][1][1], 145);
		$('#network_graph3').show();
	} else if (trial_counter==conditions.length) {
		$('#scenario_1_5').hide();
		goto_debrief();
	}
};


var goto_task = function() {
	$('#comprehension').hide();
	$('#main_task_intro').show();
	update_scenario('network_graph3', condition_counter, case_counter, 'not-neighbours');
};


var goto_debrief = function() {
	$('#instructions').hide(); 
	$('#main_task').hide();
	// $('#qual_questions').hide();
	$('#debrief').show();
	$('#completed').hide();
};


var goto_complete = function (code) {
	$('#instructions').hide();
	$('#main_task').hide();
	$('#debrief').hide();
	$('#completed').show();
	$('#completion_code_tb').text(code);
};


// B) Custom functions
//////////////////////

// creating new distribution based on moving sliders 
var plot_distributions = function(bel_slider, con_slider, bel_slider_pos, con_slider_pos, name_1, name_2, plot_division, continue_btn) {
 	$('#scenario_1_4_btn').prop('disabled',true);
	document.getElementById(bel_slider).value = bel_slider_pos;
	document.getElementById(con_slider).value = con_slider_pos;

	var hash = '#'; 
 var bel_slider = hash.concat(bel_slider);
 var con_slider = hash.concat(con_slider);
 

 var belief = bel_slider_pos;
	var variance = log_slider(transform_con_slider_pos(parseInt(con_slider_pos)));
	var x = create_data(belief/100, variance)[0];
	var y = create_data(belief/100, variance)[1];
	create_plot(x, y, belief/100, name_1, name_2, plot_division, 550);

	//  belief
	var $belief=$(bel_slider);
	$belief.on('input',function(){
		if ($('#confidenceOutputId_4').text() != 'move slider to rate how certain you are about your belief' && $('#beliefOutputId_4').text() != 'move slider to rate belief') {
			$('#scenario_1_4_btn').prop('disabled',false);
		};
	 var belief = parseInt($belief.val());
	 var variance = log_slider(transform_con_slider_pos(parseInt($confidence.val()))); 
	 var x = create_data(belief/100, variance)[0];
		var y = create_data(belief/100, variance)[1];
		create_plot(x, y, belief/100, name_1, name_2, plot_division, 550);
	});

	// confidence 
	var $confidence=$(con_slider);
	$confidence.on('input',function(){
		if ($('#confidenceOutputId_4').text() != 'move slider to rate how certain you are about your belief' && $('#beliefOutputId_4').text() != 'move slider to rate belief') {
			$('#scenario_1_4_btn').prop('disabled',false);
		};
		var belief = parseInt($belief.val());
		var variance = log_slider(transform_con_slider_pos(parseInt($confidence.val())));  
		var x = create_data(belief/100, variance)[0];
		var y = create_data(belief/100, variance)[1];
		create_plot(x, y, belief/100, name_1, name_2, plot_division, 550); 
	});
};  


// updating the scenario for each condition (random for each participant)
var update_scenario = function (canvas_no, condition_counter, case_counter, network) {
	
	if (network == 'neighbours'){
		var neighbour_name_1 = conditions[condition_counter][4][0];
		var neighbour_name_2 = conditions[condition_counter][4][1];
	} else if (network == 'not-neighbours') {
		var neighbour_name_1 = conditions[condition_counter][3][0][0];
		var neighbour_name_2 = conditions[condition_counter][3][1][0];
	};

	// getting the network stories and cases from the json files
	var head = conditions[condition_counter][1][0];
	var background = conditions[condition_counter][2];

	// results for each case (stored in the conditions list)
	var possible_results = conditions[condition_counter][3];

	// changing the content of the scenario paragraphs according to the randomly choosen cases, results, and condition
	document.getElementById("scenario_1_1_head").innerHTML = head;
	document.getElementById("scenario_1_1_background").innerHTML = background;
	document.getElementById("case_1_results_text").innerHTML = random_results[case_counter][2][0];
	document.getElementById("case_2_results_text").innerHTML = random_results[case_counter][2][1];
	
	// Drawing the graph displayed in scenario_1_3  
	// graph components  
	// changing the network structure of the graph according to the present condition (see draw_network.js for details)
	generate_network(canvas_no, 675, 75, nodes[0], vs[0], legs[0], legs[1], arms[0], arms[1], bodies[0], lines[0], arrows[0], -1, conditions[condition_counter][0], neighbour_name_2);
	generate_network(canvas_no, 125, 75, nodes[1], vs[0], legs[2], legs[3], arms[3], arms[4], bodies[1], lines[1], arrows[1], 1, conditions[condition_counter][0], neighbour_name_1);
};


// showing plots and storing responses based on condition 
var store_responses = function(round) {
	// determining id of plot and sliders based on condition (random order)
	if (round == 'round_1') {
		var slid_bel = $("#belief_slider_3").val();
		var slid_var = transform_con_slider_pos($("#confidence_slider_3").val());
	} else if (round = 'round_2') {
		var slid_bel = $("#belief_slider_4").val();
		var slid_var = transform_con_slider_pos($("#confidence_slider_4").val());
	};
	// storing responses 
	responses.push(slid_bel); 
	responses.push(slid_var);
}; 


 
 // INITIAL VIEW:
////////////////
// Initially block both the check button and the start button
$('#done_comp').hide();//prop('disabled', true);
$('#comp_check_btn').hide();//prop('disabled', true);
$('#consent').hide(); 
$('#main_task').hide();
// $('#qual_questions').hide(); 
$('#instructions').hide();

if (isMobile() || isMobileOrTablet()) {
	alert('Unfortunately, you need to be on a desktop or laptop computer in order to take part in this experiment. In any case thank you very much for the interest.')
	$('#instructions').hide();	
};

 
if (isChrome == true) {
	$('#instructions').show();	

} else if (isSafari == true || isFirefox == true || isOpera == true || isEdge == true || isIE == true || isBlink == true) {
	alert('Unfortunately, you need to use Google Chrome in order to take part in this experiment. In any case thank you very much for the interest.')
	$('#instructions').hide();	
};




