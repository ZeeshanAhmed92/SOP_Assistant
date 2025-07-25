import React, { useState } from 'react';
import { View, Text, TextInput, Button, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../api/api';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [pin, setPin] = useState('');

  const handleLogin = async () => {
    try {
      const res = await api.post('/auth/login', { email, pin });
      await AsyncStorage.setItem('token', res.data.token);
      await AsyncStorage.setItem('role', res.data.role);
      if (res.data.role === 'Supervisor') {
        navigation.replace('AdminDashboard');
      } else {
        navigation.replace('ShiftValidation');
      }
    } catch (err) {
      Alert.alert('Login Failed', 'Invalid credentials');
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Email:</Text>
      <TextInput value={email} onChangeText={setEmail} autoCapitalize="none" style={{ borderBottomWidth: 1 }} />
      <Text>PIN:</Text>
      <TextInput value={pin} onChangeText={setPin} secureTextEntry style={{ borderBottomWidth: 1 }} />
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}
