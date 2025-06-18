<template>
  <div
    class="pointer-events-auto flex items-center justify-between space-x-2 rounded-md border bg-white p-4 shadow"
  >
    <div><slot /></div>
    <button @click="$emit('close')" class="ml-2 text-gray-500">×</button>
  </div>
</template>
<script setup lang="ts"></script>
