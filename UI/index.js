import React from 'react';
import { AppRegistry, View } from 'react-native';
import Router from './src/Router';


console.disableYellowBox = true;
const App = () => (
    <View style = {{ flex: 1 }}>
        {/* <Header headerText = {'UCanToo'}/> */}
        {/* <Question /> */}
        {/* <AskQuestion /> */}
        <Router />
    </View> 
);


AppRegistry.registerComponent('UI', () => App);