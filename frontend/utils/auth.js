import AsyncStorage from '@react-native-async-storage/async-storage';
import jwtDecode from 'jwt-decode';

export const storeToken = async (token) => {
  try {
    await AsyncStorage.setItem('token', token);
  } catch (err) {
    console.error('Failed to store token', err);
  }
};

export const getToken = async () => {
  try {
    return await AsyncStorage.getItem('token');
  } catch (err) {
    console.error('Failed to get token', err);
    return null;
  }
};

export const getUserInfo = async () => {
  try {
    const token = await getToken();
    if (!token) return null;
    return jwtDecode(token);
  } catch (err) {
    console.error('Failed to decode token', err);
    return null;
  }
};

export const clearToken = async () => {
  try {
    await AsyncStorage.removeItem('token');
  } catch (err) {
    console.error('Failed to clear token', err);
  }
};
