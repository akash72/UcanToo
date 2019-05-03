import React, { Component } from 'react';
import { ScrollView } from 'react-native';
import AnswerDetail from './AnswerDetail';

class Question extends Component {

    state = { 
                answers: this.props.answers,
                question: this.props.question
            };


    renderAnswers() {
        return this.state.answers.map(answer => 
            <AnswerDetail key ={answer} answer = {answer} question = {this.state.question} />       
        );
    }

    render() {
        console.log('Inside question: ', this.state);
        return (
            <ScrollView>
                {this.renderAnswers()} 
            </ScrollView>    
        );
    }   
}

export default Question;