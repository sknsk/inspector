<template>
  <div class="p-2">
    <button @click="listPrompts" class="border px-2 py-1 mb-2">
      List Prompts
    </button>
    <ul class="mb-2">
      <li
        v-for="p in prompts"
        :key="p.name"
        @click="getPrompt(p.name)"
        class="cursor-pointer hover:underline"
      >
        {{ p.name }}
      </li>
    </ul>
    <pre class="border p-2 h-40 overflow-auto">{{ promptContent }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{
  sendRequest: (m: string, p: any) => Promise<any>;
}>();
const prompts = ref<Array<any>>([]);
const promptContent = ref("");
async function listPrompts() {
  const r = await props.sendRequest("prompts/list", {});
  prompts.value = r.prompts || [];
}
async function getPrompt(name: string) {
  const r = await props.sendRequest("prompts/get", { name });
  promptContent.value = JSON.stringify(r, null, 2);
}
</script>
