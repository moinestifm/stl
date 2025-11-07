<template>
    <div>
      <h4>Logs:</h4>
      <pre>{{ logs.join('\n') }}</pre>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  const props = defineProps({ receiverId: String });
  const logs = ref([]);
  
  onMounted(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/logs/${props.receiverId}`);
    ws.onmessage = (event) => logs.value.push(event.data);
  });
  </script>
  