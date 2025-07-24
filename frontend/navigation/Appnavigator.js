import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from '../screens/LoginScreen';
import EmployeeHome from '../screens/EmployeeHome';
import AdminDashboard from '../screens/AdminDashboard';
import ShiftValidation from '../screens/ShiftValidation';

const Stack = createNativeStackNavigator();

const AppNavigator = () => {
  return (
    <Stack.Navigator initialRouteName="Login">
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="ShiftValidation" component={ShiftValidation} />
      <Stack.Screen name="EmployeeHome" component={EmployeeHome} />
      <Stack.Screen name="AdminDashboard" component={AdminDashboard} />
    </Stack.Navigator>
  );
};

export default AppNavigator;
