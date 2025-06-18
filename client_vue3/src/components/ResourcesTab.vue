<template>
  <div class="p-2">
    <button @click="listResources" class="border px-2 py-1 mb-2">
      List Resources
    </button>
    <ul class="mb-2">
      <li
        v-for="r in resources"
        :key="r.uri"
        @click="readResource(r.uri)"
        class="cursor-pointer hover:underline"
      >
        {{ r.name }}
      </li>
    </ul>
    <pre class="border p-2 h-40 overflow-auto">{{ resourceContent }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const props = defineProps<{
  sendRequest: (m: string, p: any) => Promise<any>;
}>();
const resources = ref<Array<any>>([]);
const resourceContent = ref("");
async function listResources() {
  const r = await props.sendRequest("resources/list", {});
  resources.value = r.resources || [];
}
async function readResource(uri: string) {
  const r = await props.sendRequest("resources/read", { uri });
  resourceContent.value = JSON.stringify(r, null, 2);
}
</script>
