import { Component } from "react";
import UserService from "../services/user.service";

type Props = {};

type State = {
    content: string;
}

export default class Home extends Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            content: "테스트"
        };
    }

    componentDidMount() {
        UserService.getPublicContent().then(
            response => {
                this.setState({
                    content: JSON.stringify(response.data)
                });
            },
            error => {
                this.setState({
                    content:
                        (error.response && error.response.data) ||
                        error.message ||
                        error.toString()
                });
            }
        );
    }

    render() {
        return (
            <div className="container">
                <header className="jumbotron">
                    <h3>{this.state.content}</h3>
                    <img className="logo-img" src="logo512.png"/>
                </header>
            </div>
        );
    }
}