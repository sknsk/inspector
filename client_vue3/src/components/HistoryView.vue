<template>
  <div class="p-2">
    <h3>History</h3>
    <ul class="space-y-2 max-h-48 overflow-auto">
      <li v-for="(item, idx) in history" :key="idx" class="border p-2">
        <div class="text-xs text-gray-600">Request:</div>
        <pre class="whitespace-pre-wrap">{{ item.request }}</pre>
        <div class="text-xs text-gray-600">Response:</div>
        <pre class="whitespace-pre-wrap">{{ item.response }}</pre>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  history: Array<{ request: string; response: string }>;
}>();
</script>
