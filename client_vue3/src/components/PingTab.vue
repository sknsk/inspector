<template>
  <div class="p-2">
    <Button @click="ping" class="mb-2">Ping</Button>
    <pre class="border p-2 h-20 overflow-auto">{{ result }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Button } from "./ui";
const props = defineProps<{
  sendRequest: (m: string, p: any) => Promise<any>;
}>();
const result = ref("");
async function ping() {
  const r = await props.sendRequest("ping", {});
  result.value = JSON.stringify(r, null, 2);
}
</script>
