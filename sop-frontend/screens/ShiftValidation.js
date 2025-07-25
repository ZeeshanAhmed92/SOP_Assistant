import React, { useEffect, useState } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../api/api';

export default function ShiftValidation({ navigation }) {
  const [status, setStatus] = useState(null);

  const validateShift = async () => {
    const token = await AsyncStorage.getItem('token');
    const res = await api.get('/employee/on-shift', { headers: { Authorization: `Bearer ${token}` } });
    if (res.data.on_shift) {
      navigation.replace('EmployeeHome');
    } else {
      setStatus('You are not currently on shift.');
    }
  };

  useEffect(() => {
    validateShift();
  }, []);

  return (
    <View style={{ padding: 20 }}>
      {status ? <Text>{status}</Text> : <Text>Checking shift status...</Text>}
    </View>
  );
}