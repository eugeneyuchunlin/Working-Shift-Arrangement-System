$(document).ready(()=>{
	$('#calculate').click(()=>{
		var data = getShift();
		var params = getParameter();
		waitingAnimation(true);
		$.ajax({
			type:"POST",
			url:window.location.origin + '/postshift/' + "?year=" + params['year'] + "&month=" + params['month'] + "&mode=computing",
			data:JSON.stringify(data),
			dataType:"json",
			contentType: "application/json;charset=utf-8",
			success:(res)=>{
				console.log('Success');
				location.reload();
			},
			error:(res)=>{
				console.log('error');
				location.reload();
			}
		})
	})
	$('#save').click(()=>{
		console.log('save shift');
		waitingAnimation(true);
		var data = getShift();	
		var params= getParameter();
		console.log(data)
		console.log(params)
		$.ajax({
			type:"POST",
			url:window.location.origin + '/postshift/' + "?year=" + params['year'] + "&month=" + params['month'] + "&mode=saving",
			data:JSON.stringify(data),
			dataType:"json",
			contentType: "application/json;charset=utf-8",
			success:(res)=>{
				console.log('Success');
				waitingAnimation(false);
			},
			error:(res)=>{
				console.log('error');
				waitingAnimation(false);
			}
		})
	
	})

	$('#clear').click(()=>{
		var params = getParameter();
		$.ajax({
			type:"GET",
			url:window.location.origin + '/postshift/' + '?year=' + params['year'] + '&month=' + params['month'] + '&mode=clear',
			async:false,
			success:(res)=>{
				console.log('success');	
				location.reload();
			},
			error:(res)=>{
				console.log('error');
				location.reload();
			}
			
		})
	})
})

var getParameter = ()=>{
	let locationURL = new URL(window.location.href);
	var searchParams = locationURL.searchParams;
	console.log(searchParams.entries());
	var data = {};
	for(let params of searchParams.entries()){
		data[params[0]] = params[1];
		// console.log(`key : ${params[0]}, value : ${params[1]}`);
	
	}
	return data;
}

var getShift = ()=>{
	var rows = $('.row');
	var data = {};
	var dArray = [];
	// date and day
	for(var i = 0; i < 2; i++){
		var elements = $(rows[i]).find('div')
		dArray = [];
		for(var j = 0; j < elements.length; j++){
			dArray.push($(elements[j]).text());	
		}
		data[dArray[0]] = dArray;
	}
	// Shift
	for(var i = 2; i < rows.length; i++){
		var elements = $(rows[i]).find('input')
		var name = $($(rows[i]).find('div')[0]).text();
		dArray = [];
		dArray.push(name);
		for(var j = 0; j < elements.length; j++){
			dArray.push($(elements[j]).val());
		}
		data[name] = dArray;
	}
	return data;
}

var waitingAnimation = (wait)=>{
	if(wait){
		$('.row').css('filter', 'blur(1px)');
		$('.loader').css('display', 'block');
	}else{
		$('.row').css('filter', 'blur(0px)');
		$('.loader').css('display', 'none');
	}

}
