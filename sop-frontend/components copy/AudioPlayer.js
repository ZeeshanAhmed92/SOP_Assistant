import React, { useState } from 'react';
import { View, Button } from 'react-native';
import { Audio } from 'expo-av';
import api from '../api/api';

export default function AudioPlayer({ text }) {
  const [playing, setPlaying] = useState(false);

  const playAudio = async () => {
    setPlaying(true);
    try {
      const res = await api.post('/audio/text-to-speech', { text }, { responseType: 'blob' });
      const uri = URL.createObjectURL(new Blob([res.data], { type: 'audio/mpeg' }));

      const { sound } = await Audio.Sound.createAsync({ uri });
      await sound.playAsync();
      sound.setOnPlaybackStatusUpdate(status => {
        if (!status.isPlaying) {
          setPlaying(false);
        }
      });
    } catch (err) {
      console.error('TTS failed', err);
      setPlaying(false);
    }
  };

  return (
    <View style={{ marginTop: 10 }}>
      <Button title={playing ? 'Playing...' : 'Play Audio'} onPress={playAudio} disabled={playing} />
    </View>
  );
}
