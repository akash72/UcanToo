import React from 'react';
import { AppRegistry, View } from 'react-native';
import Header from './src/components/Header';
import Question from './src/components/Question';
import AskQuestion from './src/components/AskQuestion';
import Router from './src/Router';

const App = () => (
    <View style = {{ flex: 1 }}>
        {/* <Header headerText = {'UCanToo'}/> */}
        {/* <Question /> */}
        {/* <AskQuestion /> */}
        <Router />
    </View> 
);


AppRegistry.registerComponent('UI', () => App);