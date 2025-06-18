<template>
  <div class="p-2">
    <button @click="ping" class="border px-2 py-1 mb-2">Ping</button>
    <pre class="border p-2 h-20 overflow-auto">{{ result }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{
  sendRequest: (m: string, p: any) => Promise<any>;
}>();
const result = ref("");
async function ping() {
  const r = await props.sendRequest("ping", {});
  result.value = JSON.stringify(r, null, 2);
}
</script>
