var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Username = function (_React$Component) {
    _inherits(Username, _React$Component);

    function Username() {
        _classCallCheck(this, Username);

        return _possibleConstructorReturn(this, (Username.__proto__ || Object.getPrototypeOf(Username)).apply(this, arguments));
    }

    _createClass(Username, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { id: "username-form", className: "form" },
                React.createElement(
                    "div",
                    { id: "username-text" },
                    "Username"
                ),
                React.createElement("input", { type: "text", id: "username" })
            );
        }
    }]);

    return Username;
}(React.Component);

var Password = function (_React$Component2) {
    _inherits(Password, _React$Component2);

    function Password() {
        _classCallCheck(this, Password);

        return _possibleConstructorReturn(this, (Password.__proto__ || Object.getPrototypeOf(Password)).apply(this, arguments));
    }

    _createClass(Password, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                { id: "password-form", className: "form" },
                React.createElement(
                    "div",
                    { id: "password-text" },
                    "Password"
                ),
                React.createElement("input", { type: "password", id: "password" })
            );
        }
    }]);

    return Password;
}(React.Component);

var LoginButton = function (_React$Component3) {
    _inherits(LoginButton, _React$Component3);

    function LoginButton(props) {
        _classCallCheck(this, LoginButton);

        var _this3 = _possibleConstructorReturn(this, (LoginButton.__proto__ || Object.getPrototypeOf(LoginButton)).call(this, props));

        _this3.state = { alreadyAlert: false };
        return _this3;
    }

    _createClass(LoginButton, [{
        key: "handleClick",
        value: function handleClick() {
            var username = $('#username').val();
            var password = $('#password').val();
            var data = { "username": username, "password": password };
            // send jqAJAX
            console.log(username);
            console.log(password);
            var response;
            $.ajax({
                type: "POST",
                async: false,
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                url: window.location.origin + '/login/',
                data: JSON.stringify(data),
                success: function success(res) {
                    response = res;
                    console.log(res);
                },
                error: function error(res, exception) {
                    response = res;
                    console.log(res);
                }
            });
            if (response.responseText == 'Ok') {
                window.location.href = window.location.origin + '/overview/?year=2018';
            } else {
                var alreadyAlert = this.state.alreadyAlert;
                console.log(alreadyAlert);
                if (!alreadyAlert) {
                    $('.alert').transition('fade down');
                    alreadyAlert = true;
                    this.setState({ alreadyAlert: alreadyAlert });
                }
                console.log(this.state.alreadyAlert);
                $('#username').addClass('wrong');
                $('#password').addClass('wrong');
            }
        }
    }, {
        key: "render",
        value: function render() {
            var _this4 = this;

            return React.createElement(
                "div",
                { id: "login-button", onClick: function onClick() {
                        return _this4.handleClick();
                    } },
                "Login"
            );
        }
    }]);

    return LoginButton;
}(React.Component);

var Login = function (_React$Component4) {
    _inherits(Login, _React$Component4);

    function Login() {
        _classCallCheck(this, Login);

        return _possibleConstructorReturn(this, (Login.__proto__ || Object.getPrototypeOf(Login)).apply(this, arguments));
    }

    _createClass(Login, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "div",
                    { id: "alert" },
                    React.createElement(
                        "div",
                        { className: "alert alert-danger", role: "alert" },
                        "Wrong Password or Username"
                    )
                ),
                React.createElement(
                    "div",
                    { id: "login-text" },
                    "Login to Continue"
                ),
                React.createElement(
                    "div",
                    { id: "login-form" },
                    React.createElement(Username, null),
                    React.createElement(Password, null),
                    React.createElement(LoginButton, null)
                )
            );
        }
    }]);

    return Login;
}(React.Component);

ReactDOM.render(React.createElement(Login, null), document.getElementById('login'));