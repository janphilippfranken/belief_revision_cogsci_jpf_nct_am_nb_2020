var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. " + 
"This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";


//Listen for all fields being complete
posttest_button_disabler = function () {
	if($("#feedback").val() === '' || $("#age").val() === '' || $("#sex").val() === 'noresp' || $("#engagement").val() === '--' || $("#difficulty").val() === '--' || $("#pol_orientation").val() === '--' || $("#init_strat").val() === '' || $("#final_strat").val() === '') {
		$('#done_debrief').prop('disabled',true);
	} else{
		$('#done_debrief').prop('disabled',false);
	}
}

prompt_resubmit = function() {
	document.body.innerHTML = error_message;
	$("#resubmit").click(resubmit);
};

//Assign the (dis)abler function to all posttestQ class objects
$(".posttestQ").change(function () {
	posttest_button_disabler();
})


// Block enter in age field
$("#ageinput").keydown(function(event){
	if(event.keyCode == 13) {
		event.preventDefault();
		console.log('blocked enter in age field');
		return false;
	} 
});


 
var save_data = function () {

	console.log('FINISHED TASK');

	var end_time = new Date();

	var data = {
		"subjectwise": {
			date:String(end_time.getFullYear()) + '_' +
				String(end_time.getMonth() + 1).padStart(2, '0') + '_' +
				String(end_time.getDate() + 1).padStart(2, '0'),
			time:String(end_time.getHours()+ 1).padStart(2, '0') + '_' +
				String(end_time.getMinutes() + 1).padStart(2, '0')+ '_' +
				String(end_time.getSeconds() + 1).padStart(2, '0'),
			age:$("#ageinput").val(),
			gender:$("#sex").val(),
			feedback:$('#feedback').val(),
			initial_strategy: $('#init_strat').val(),
			final_strategy: $('#final_strat').val(),
			instructions_duration:start_task_time - start_time,
			task_duration:end_time - start_task_time,
			engaging:$("#engagement").val(),
			difficult:$("#difficulty").val(),
			pol_orient:$("#pol_orientation").val(),
			token: token_id},
		"trialwise":{rand_cond_order, rand_res_stored, responses, random_pos_winner},
		} 

		console.log(data);

		fetch(root_string, {
			method: 'POST',
			body: JSON.stringify(data),
		})
		.then( (response) => {
			console.log(response);
			return response.json()})
		// .then( (json) => goto_complete(json.completed_token) )
		.catch( (error) => console.log(error) );


		goto_complete(token_id);
	};




// When done is clicked, attempt to save all the data
$('#done_debrief').click(save_data);
