import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import api from '../api/api';
import AudioRecorder from '../components/AudioRecorder';
import AudioPlayer from '../components/AudioPlayer';

export default function EmployeeHome() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const handleQuery = async () => {
    try {
      const res = await api.post('/assistant/query', { question });
      setResponse(res.data.response);
    } catch (err) {
      Alert.alert('Error', 'Failed to fetch response');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Ask your SOP Question:</Text>
      <TextInput value={question} onChangeText={setQuestion} style={{ borderBottomWidth: 1 }} />
      <Button title="Ask" onPress={handleQuery} />
      <AudioRecorder onTranscribed={setQuestion} />
      <Text style={{ marginTop: 20 }}>Response:</Text>
      <Text>{response}</Text>
      {response && <AudioPlayer text={response} />}
    </View>
  );
}
