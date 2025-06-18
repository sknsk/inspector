<template>
  <div class="p-2">
    <Button @click="listTools" class="mb-2">List Tools</Button>
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
      <Textarea v-model="paramsText" rows="4" class="w-full" />
      <Button @click="callTool" class="mt-1">Run</Button>
    </div>
    <pre class="border p-2 h-40 overflow-auto">{{ toolResult }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { Button, Textarea } from "./ui";
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
