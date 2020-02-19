$(document).ready(()=>{
	$('#calculate').click(()=>{
		console.log('Cal Click');
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
			data[dArray.splice(0,1)] = dArray;
		}
		// Shift
		for(var i = 2; i < rows.length; i++){
			var elements = $(rows[i]).find('input')
			var name = $($(rows[i]).find('div')[0]).text();
			dArray = [];
			for(var j = 0; j < elements.length; j++){
				dArray.push($(elements[j]).val());
			}
			data[name] = dArray;
		}
		console.log(data);
		$.ajax({
			type:"POST",
			url:window.location.origin + '/postshift/',
			data:JSON.stringify(data),
			async:false,
			dataType:"json",
			contentType: "application/json;charset=utf-8",
			success:(res)=>{
				console.log(res);
			}
		})
	})
})
