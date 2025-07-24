import React, { useState } from 'react';
import { View, Text, Button, TextInput } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import api from '../api/api';

export default function AdminDashboard() {
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileUpload = async () => {
    const file = await DocumentPicker.getDocumentAsync({ type: '*/*' });
    if (!file.canceled) {
      const formData = new FormData();
      formData.append('file', {
        uri: file.uri,
        name: file.name,
        type: file.mimeType || 'application/pdf'
      });

      const res = await api.post('/sop/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setUploadStatus(res.data.message);
    }
  };

  return (
    <View style={{ padding: 20 }}>
      <Text>Admin Dashboard</Text>
      <Button title="Upload SOP" onPress={handleFileUpload} />
      <Text>{uploadStatus}</Text>
    </View>
  );
}
