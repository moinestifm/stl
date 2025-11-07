<template>
    <div>
      <h2>Receivers</h2>
      <ul>
        <li v-for="r in receivers" :key="r">
          {{ r }}
          <button @click="start(r)">Start</button>
          <button @click="stop(r)">Stop</button>
          <LogViewer :receiverId="r" />
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import LogViewer from './LogViewer.vue';
  
  const receivers = ref([]);
  
  const fetchReceivers = async () => {
    const res = await axios.get('http://localhost:8000/receivers');
    receivers.value = res.data;
  };
  
  const start = async (id) => await axios.post(`http://localhost:8000/receivers/start/${id}`);
  const stop = async (id) => await axios.post(`http://localhost:8000/receivers/stop/${id}`);
  
  onMounted(fetchReceivers);
  </script>
  