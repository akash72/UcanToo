import React from 'react';
import { Text, View, TextInput } from 'react-native';

const Input = ({ label, value, onChangeText, placeholder, editable, height, width }) => {
    // if(this.props.label != null) {
    //     return( 
    //         <View style>
    //             <Text >
    //                 { label }
    //             </Text>
    //             <TextInput
    //                 value = { value }
    //                 onChangeText = { onChangeText }
    //                 multiline={true}
    //                 blurOnSubmit = {true}
    //                 flexDirection = 'row'
    //                 autoCorrect = {false}
    //                 placeholder = {placeholder}
    //                 editable = {editable}
    //                 height = { height }
    //                 width = { width }
    //             />
    //         </View>      
    //     );
    // }

    return( 
        <View style>
            <TextInput
                value = { value }
                onChangeText = { onChangeText }
                multiline={true}
                blurOnSubmit = {true}
                flexDirection = 'row'
                autoCorrect = {false}
                placeholder = {placeholder}
                editable = {editable}
                height = { height }
                width = { width }
            />
        </View>      
    );
};

const styles = {
    inputStyle: {
        color: '#000',
        paddingRight: 5,
        paddingLeft: 5,
        fontSize: 18,
        lineHeight: 23,
        flex: 2,
    },
    labelStyle: {
        fontSize: 18,
        paddingLeft: 20,
        flex: 1
    },
    containerStyle: {
        height: 400,
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center'
    }
}

export default Input;