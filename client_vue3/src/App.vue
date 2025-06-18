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

    <div v-if="connected" class="mb-2 space-x-2">
      <button @click="activeTab = 'resources'" class="border px-2 py-1">
        Resources
      </button>
      <button @click="activeTab = 'prompts'" class="border px-2 py-1">
        Prompts
      </button>
      <button @click="activeTab = 'tools'" class="border px-2 py-1">
        Tools
      </button>
      <button @click="activeTab = 'ping'" class="border px-2 py-1">Ping</button>
    </div>

    <component :is="currentTab" v-if="connected" :send-request="sendRequest" />

    <HistoryView :history="history" class="mt-4" />

    <pre class="border p-2 h-60 overflow-auto">{{ output }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import ResourcesTab from "./components/ResourcesTab.vue";
import PromptsTab from "./components/PromptsTab.vue";
import ToolsTab from "./components/ToolsTab.vue";
import PingTab from "./components/PingTab.vue";
import HistoryView from "./components/HistoryView.vue";

const command = ref("echo");
const args = ref("hello");
const output = ref("");
const mcpUrl = ref("http://localhost:6277");
const sessionId = ref<string | null>(null);
const connected = ref(false);
const history = ref<Array<{ request: string; response: string }>>([]);
const activeTab = ref<"resources" | "prompts" | "tools" | "ping">("resources");
const tabs = {
  resources: ResourcesTab,
  prompts: PromptsTab,
  tools: ToolsTab,
  ping: PingTab,
};
const currentTab = computed(() => tabs[activeTab.value]);

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
  sessionId.value = resp.headers.get("mcp-session-id");
  connected.value = true;
}

async function disconnectMcp() {
  if (!sessionId.value) return;
  await fetch(`/mcp?sessionId=${sessionId.value}`, { method: "DELETE" });
  sessionId.value = null;
  connected.value = false;
}

async function sendRequest(method: string, params: any) {
  if (!sessionId.value) return {};
  const body = JSON.stringify({
    jsonrpc: "2.0",
    id: Date.now(),
    method,
    params,
  });
  const resp = await fetch("/mcp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "mcp-session-id": sessionId.value,
    },
    body,
  });
  sessionId.value = resp.headers.get("mcp-session-id") || sessionId.value;
  const text = await resp.text();
  history.value.push({ request: body, response: text });
  try {
    return JSON.parse(text);
  } catch {
    return {};
  }
}
</script>

<style scoped>
body {
  font-family: sans-serif;
}
</style>
