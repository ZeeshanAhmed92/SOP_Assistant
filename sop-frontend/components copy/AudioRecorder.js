import React, { useState } from 'react';
import { View, Button, Text, ActivityIndicator } from 'react-native';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';
import api from '../api/api';

export default function AudioRecorder({ onTranscribed }) {
  const [recording, setRecording] = useState(null);
  const [loading, setLoading] = useState(false);

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (permission.status !== 'granted') return;

      await Audio.setAudioModeAsync({ allowsRecordingIOS: true, playsInSilentModeIOS: true });
      const { recording } = await Audio.Recording.createAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
      setRecording(recording);
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  const stopRecording = async () => {
    setLoading(true);
    setRecording(undefined);
    await recording.stopAndUnloadAsync();
    const uri = recording.getURI();

    const fileInfo = await FileSystem.getInfoAsync(uri);
    const formData = new FormData();
    formData.append('audio', {
      uri,
      name: 'recording.wav',
      type: 'audio/wav'
    });

    try {
      const res = await api.post('/audio/speech-to-text', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onTranscribed(res.data.text);
    } catch (err) {
      console.error('STT failed', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ marginVertical: 20 }}>
      {recording ? (
        <Button title="Stop Recording" onPress={stopRecording} />
      ) : (
        <Button title="Start Recording" onPress={startRecording} />
      )}
      {loading && <ActivityIndicator style={{ marginTop: 10 }} />}
    </View>
  );
}
