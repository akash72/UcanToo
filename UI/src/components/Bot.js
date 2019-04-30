import React, { Component } from 'react';
import CardSection from './CardSection';
import Card from './Card';
import { Text, StyleSheet, ScrollView } from 'react-native';
import Spinner from './Spinner';
import axios from 'axios';
import AnswerDetail from './AnswerDetail';

class Bot extends Component {

    state = { 
        question: this.props.question,
        loading: true,
        answers: []
    };

    renderAnswers() {
        return this.state.answers.map(answer => 
            <AnswerDetail key ={answer} answer = {answer} question = {this.state.question} />       
        );
    }

    async renderAnswer() {
        
        await axios.post('http://127.0.0.1:5000/askubuntu/questions', {
            "question": this.state.question
        })
        .then(response => this.setState({ answers: response.data.answers }));
        this.setState({loading: false})
        console.log("Answers: ", this.state.answers)
        
        return (
            <ScrollView>
                {this.renderAnswers()} 
            </ScrollView>  
        )
    }

    render() {
        return (
            <Card>
                <CardSection>
                    <Text>{this.state.question}</Text>
                </CardSection>
                
                <CardSection>
                    {this.renderAnswer.bind(this)}
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
        // textAlignVertical: 'top',
        // flex: 1,
        // flexWrap: 'wrap',
        // flexDirection: 'row',
        // width: 350,
        // flexGrow: 1,
        // marginLeft: 10,
        fontSize: 14,
        display: 'flex',
        justifyContent: 'space-around'
    },
    
});

export default Bot;