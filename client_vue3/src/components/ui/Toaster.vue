<template>
  <div class="fixed top-2 right-2 space-y-2">
    <Toast v-for="t in toasts" :key="t.id" @close="remove(t.id)">{{
      t.message
    }}</Toast>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import Toast from "./Toast.vue";
const toasts = ref<{ id: number; message: string }[]>([]);
function remove(id: number) {
  toasts.value = toasts.value.filter((t) => t.id !== id);
}
function push(message: string) {
  const id = Date.now();
  toasts.value.push({ id, message });
  setTimeout(() => remove(id), 3000);
}

export { push };
</script>
