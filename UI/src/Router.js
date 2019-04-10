import React from 'react';
import { Scene, Router } from 'react-native-router-flux';
import AskQuestion from './components/AskQuestion';
import Question from './components/Question';

const RouterComponent = () => {
    return(
        <Router>
            <Scene key="root">
                <Scene key="askQuestion" component={AskQuestion} title = "UCanToo" initial/>
                <Scene key="question" component={Question} title="UCanToo"/>
            </Scene>
            
        </Router>

    );
};

export default RouterComponent;
