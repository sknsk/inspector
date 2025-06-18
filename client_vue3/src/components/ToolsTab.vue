<template>
  <div class="p-2">
    <button @click="listTools" class="border px-2 py-1 mb-2">List Tools</button>
    <ul class="mb-2">
      <li
        v-for="t in tools"
        :key="t.name"
        @click="selectTool(t)"
        class="cursor-pointer hover:underline"
      >
        {{ t.name }}
      </li>
    </ul>
    <div v-if="selected" class="mb-2">
      <textarea v-model="paramsText" rows="4" class="border w-full"></textarea>
      <button @click="callTool" class="border px-2 py-1 mt-1">Run</button>
    </div>
    <pre class="border p-2 h-40 overflow-auto">{{ toolResult }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{
  sendRequest: (m: string, p: any) => Promise<any>;
}>();
const tools = ref<Array<any>>([]);
const selected = ref<any>(null);
const paramsText = ref("{}");
const toolResult = ref("");
async function listTools() {
  const r = await props.sendRequest("tools/list", {});
  tools.value = r.tools || [];
}
function selectTool(t: any) {
  selected.value = t;
  paramsText.value = "{}";
}
async function callTool() {
  if (!selected.value) return;
  const params = paramsText.value ? JSON.parse(paramsText.value) : {};
  const r = await props.sendRequest("tools/call", {
    name: selected.value.name,
    arguments: params,
  });
  toolResult.value = JSON.stringify(r, null, 2);
}
</script>
