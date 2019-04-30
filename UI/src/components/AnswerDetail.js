import React from 'react';
import { StyleSheet, ScrollView, Dimensions, View, Text, Image, Alert } from 'react-native';
import HTML from 'react-native-render-html';
import Card from './Card';
import CardSection from './CardSection';
import Button from './Button';
import { Actions } from 'react-native-router-flux';

const AnswerDetail = (props) => {
    console.log(props.answer)
    return(
        <Card>
            
            <CardSection>
                <View style = {styles.thumbNailContainerStyle}>
                    <Image 
                        style = {styles.thumbnailStyle}
                        source = {{ uri: 'https://vignette.wikia.nocookie.net/scribblenauts/images/6/60/Question_Mark.png/revision/latest?cb=20140409201911'}}
                    />
                </View>    
                
                <View style={styles.headerContentStyle}>
                    <Text>
                        {props.question}
                    </Text>
                   
                </View>
                
            </CardSection> 
            
            <CardSection>
<               ScrollView style={{ flex: 1 }}>
                    <Text style = {styles.textStyle}>Answer: </Text>
                    <HTML html={ props.answer} imagesMaxWidth={Dimensions.get('window').width} />
                </ScrollView>
            </CardSection>   

            <CardSection>
                {/* <Button 
                    onPress = {() => Alert.alert(
                        'Do not worry! Our ML model is on its way',
                        '',
                        [
                          {text: 'OK', onPress: () => console.log('OK Pressed')},
                        ],
                        { cancelable: false }
                      )}>
                    Not happy?  
                </Button> */}

                <Button 
                    onPress = {() => Actions.ubuntuBot({question: props.question})}
                >
                Click to ask our Bot!
                </Button>   
                     
            </CardSection>     
       
        </Card>    
    );
};

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

export default AnswerDetail;