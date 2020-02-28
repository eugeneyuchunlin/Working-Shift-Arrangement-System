
class Username extends React.Component{
    render(){
        return (
            <div id="username-form" className="form">
                <div id="username-text">Username</div>
                <input type="text" id="username"/>
            </div>
        );
    }
}

class Password extends React.Component{
    render(){
        return (
            <div id="password-form" className="form">
                <div id="password-text">Password</div>
                <input type="password" id="password"/>
            </div>
        );
    }
}

class LoginButton extends React.Component{

	constructor(props){
		super(props)
		this.state = {alreadyAlert : false};
	}

    handleClick(){
        var username = $('#username').val();
        var password = $('#password').val();
		var data = {"username" : username, "password" : password};
        // send jqAJAX
        console.log(username);
        console.log(password);
		var response;
		$.ajax({
			type:"POST",
			async:false,
			dataType:"json",
			contentType:"application/json;charset=utf-8",
			url : window.location.origin + '/login/',
			data:JSON.stringify(data),
			success:(res)=>{
				response = res;
				console.log(res);
			},
			error:(res, exception)=>{
				response = res;
				console.log(res);
			}
		});
		if(response.responseText == 'Ok'){
			window.location.href = window.location.origin + '/overview/?year=2018'
		}else{
			var alreadyAlert = this.state.alreadyAlert;
			console.log(alreadyAlert);
			if(!alreadyAlert){
        		$('.alert').transition('fade down');
				alreadyAlert = true;
				this.setState({alreadyAlert : alreadyAlert});
			}
			console.log(this.state.alreadyAlert);
        	$('#username').addClass('wrong');
			$('#password').addClass('wrong');
		}
    }

    render(){
        return (
            <div id="login-button" onClick={()=>this.handleClick()}>
                Login
            </div>
        );
    }
}

class Login extends React.Component{
    render(){
        return (
            <div>
                <div id="alert">
                    <div className="alert alert-danger" role="alert">
                        Wrong Password or Username
                    </div>
                </div>
                <div id="login-text">
                    Login to Continue
                </div>
                <div id="login-form">
                    <Username />
                    <Password />
                    <LoginButton />
                </div>
            </div>
        );
    }
}

ReactDOM.render(
    <Login />,
    document.getElementById('login')
)
