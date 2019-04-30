import React, { Component } from 'react';
import { Alert } from 'react-native';
import Card from './Card';
import CardSection from './CardSection';
import Button from './Button';
import Input from './Input';
import Spinner from './Spinner';
import axios from 'axios';
import { Actions } from 'react-native-router-flux';

class AskQuestion extends Component {

    state = { question: '', loading: false,  answers: []};

    async onButtonPress() {

        if(this.state.question === '') {
            Alert.alert(
                'Please enter a question',
                '',
                [
                  {text: 'OK', onPress: () => console.log('OK Pressed')},
                ],
                { cancelable: false }
              )
        }
        else {
            const { question, answers } = this.state;
            this.setState({ loading: true });

            await axios.post('http://127.0.0.1:5000/askubuntu/questions', {
                "question": question
            })
            .then(response => this.setState({ answers: response.data.answers }));
            this.setState({loading: false})
            Actions.question({question: question, answers: answers});
        }   
    }

    renderButton() {
        if (this.state.loading) {
            return <Spinner />
        }
        return (
            <Button onPress = {this.onButtonPress.bind(this)}>
                Ask me!
            </Button>
        )
    }

    renderInputText() {
        if(this.state.loading) {
            return(
                <Input
                    value = { this.state.question }
                    onChangeText = {question => this.setState({ question })}
                    label = "Question"
                    placeholder = "Ask your question here..."
                    editable = {false}
                />
            )   
        }
        return (
            <Input
                value = { this.state.question }
                onChangeText = {question => this.setState({ question })}
                label = "Question"
                placeholder = "Ask your question here..."
                editable = {true}
            />
        )
    }

    render() {
        return(
            <Card>
                <CardSection>
                    {this.renderInputText()}
                </CardSection>
                
                <CardSection>
                    {this.renderButton()}
                </CardSection>
            </Card>
        );
    }   
}

export default AskQuestion;