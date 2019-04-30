import React, { Component } from 'react';
import CardSection from './CardSection';
import Card from './Card';
import { StyleSheet, ScrollView, Alert } from 'react-native';
import Input from './Input';
import Spinner from './Spinner';
import Button from './Button'
import axios from 'axios';
import { Actions } from 'react-native-router-flux';

class Bot extends Component {

    state = { 
        question: this.props.question,
        loading: false,
        answers: "",
        initial: true,
        height: 450,
        width: 350,
        inputQuestion: this.props.question,
        displayQuestion: ""
    };

    onDoneButtonPress() {
        Actions.initialScreen();
    }

    async onButtonPress() {

        if(this.state.inputQuestion === '') {
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
            
            this.setState({ loading: true });

            await axios.post('http://127.0.0.1:8000/ubuntuqa/questions', {
                "question": this.state.inputQuestion
            })
            .then(response => this.setState({ answers: response.data.answers }));

            if(this.state.displayQuestion == "") {
                this.setState({
                    displayQuestion: this.state.inputQuestion + '\n' + this.state.answers + '\n'
                })
            }
            else {
                this.setState({
                    displayQuestion: this.state.displayQuestion + '\n ' + 
                                    this.state.inputQuestion + '\n' + this.state.answers + '\n'
                })
            }
            this.setState({ 
                            loading: false, 
                            answers: "",
                            initial: false,
                            inputQuestion: ""                                       
                         })
            console.log('Question: ', this.state.question)

        }   
    }

    renderDoneButton() {
        if (this.state.loading) {
            return <Spinner />
        }
        return (
            <Button onPress = {this.onDoneButtonPress.bind(this)}>
                I'm done
            </Button>
        )
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

    renderQuestions() {
        if(this.state.initial) {
            return (
                <Input
                value = ""
                onChangeText = {displayQuestion => this.setState({ displayQuestion })}
                editable = {false}
                height = { this.state.height }
                width = { this.state.width }
            />)      
        }
        return (
            <Input
                value = { this.state.displayQuestion }
                onChangeText = {displayQuestion => this.setState({ displayQuestion })}
                placeholder = "Ask your question here..."
                editable = {false}
                height = { this.state.height }
                width = { this.state.width }
            />
        )
        
    }

    renderInputText() {
        
        if(this.state.loading) {
            return(
                <Input
                    value = { this.state.inputQuestion }
                    onChangeText = { inputQuestion => this.setState({ inputQuestion }) }
                    placeholder = "Ask your question here..."
                    editable = {false}
                    height = { 30 }
                    width = { 350 }
                />
            )   
        }
        return (
            <Input
                value = { this.state.inputQuestion }
                onChangeText = { inputQuestion => this.setState({ inputQuestion })}
                placeholder = "Ask your question here..."
                editable = {true}
                height = { 30 }
                width = { 350 }
            />
        )
    }

    render() {
        return (
            <Card>
                
                <ScrollView>
                    <CardSection>
                        {this.renderQuestions()}
                    </CardSection>
                </ScrollView>
        
                <CardSection>
                    {this.renderInputText()}
                </CardSection>
               
                <CardSection>
                    {this.renderButton()}
                </CardSection>

                <CardSection>
                    {this.renderDoneButton()}
                </CardSection>

            </Card> 
        );
    }   
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F8F8F8'
    },
    headerContentStyle: {
        flexDirection: 'column',
        justifyContent: 'space-around',
        flex: 1
    },
    thumbnailStyle: {
        height: 80,
        width: 60
    },
    thumbNailContainerStyle: {
        justifyContent: 'center',
        alignItems: 'center',
        marginLeft: 10,
        marginRight: 10
    },
    textStyle: {
        fontSize: 14,
        fontWeight: 'bold'
    },
    questionTextStyle: {
        fontSize: 14,
        display: 'flex',
        justifyContent: 'space-around'
    },
    
});

export default Bot;
