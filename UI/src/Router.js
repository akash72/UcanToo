import React from 'react';
import { Scene, Router } from 'react-native-router-flux';
import AskQuestion from './components/AskQuestion';
import Question from './components/Question';
import Bot from './components/Bot';

const RouterComponent = () => {
    return(
        <Router>
            <Scene key="root" hideNavBar>
                <Scene key = "initialScreen">
                    <Scene key="askQuestion" component={AskQuestion} title = "UCanToo" initial/>
                    <Scene key="question" component={Question} title = "UCanToo"/>
                </Scene>
                
                <Scene key = "ubuntuBot">
                    <Scene key="bot" component={Bot} title = "UCanToo Bot"/>
                </Scene>
                
            </Scene>
            
        </Router>

    );
};

export default RouterComponent;
