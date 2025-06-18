<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">MCP Inspector Vue3</h1>
    <div class="mb-2">
      <label class="mr-2">Command:</label>
      <input v-model="command" class="border p-1" />
      <label class="ml-2 mr-2">Args:</label>
      <input v-model="args" class="border p-1" />
      <button @click="run" class="ml-2 border px-2 py-1">Run</button>
    </div>
    <div class="mb-2">
      <label class="mr-2">MCP URL:</label>
      <input v-model="mcpUrl" class="border p-1 w-96" />
      <button @click="connectMcp" class="ml-2 border px-2 py-1">Connect</button>
      <button @click="disconnectMcp" class="ml-2 border px-2 py-1">
        Close
      </button>
    </div>
    <pre class="border p-2 h-60 overflow-auto" v-html="output"></pre>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const command = ref("echo");
const args = ref("hello");
const output = ref("");
const mcpUrl = ref("http://localhost:6277");
let sessionId: string | null = null;

async function run() {
  const url = `/stdio?command=${encodeURIComponent(command.value)}&args=${encodeURIComponent(args.value)}`;
  const evtSource = new EventSource(url);
  output.value = "";
  evtSource.onmessage = (ev) => {
    output.value += ev.data;
  };
  evtSource.onerror = () => {
    evtSource.close();
  };
}

async function connectMcp() {
  const resp = await fetch(`/mcp?url=${encodeURIComponent(mcpUrl.value)}`, {
    method: "POST",
  });
  sessionId = resp.headers.get("mcp-session-id");
  const reader = resp.body!.getReader();
  output.value = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    output.value += new TextDecoder().decode(value);
  }
}

async function disconnectMcp() {
  if (!sessionId) return;
  await fetch(`/mcp?sessionId=${sessionId}`, { method: "DELETE" });
  sessionId = null;
}
</script>

<style scoped>
body {
  font-family: sans-serif;
}
</style>
