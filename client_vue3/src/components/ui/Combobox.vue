<template>
  <div>
    <input
      v-model="query"
      @focus="open = true"
      @input="onInput"
      class="border px-2 py-1 rounded w-full"
    />
    <ul v-if="open" class="border rounded mt-1 bg-white max-h-40 overflow-auto">
      <li
        v-for="option in filtered"
        :key="option"
        @click="select(option)"
        class="px-2 py-1 hover:bg-gray-100 cursor-pointer"
      >
        {{ option }}
      </li>
    </ul>
  </div>
</template>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
const props = defineProps<{ options: string[] }>();
const emit = defineEmits(["update:modelValue"]);
const query = ref("");
const open = ref(false);
const filtered = computed(() =>
  props.options.filter((o) =>
    o.toLowerCase().includes(query.value.toLowerCase()),
  ),
);
function select(o: string) {
  emit("update:modelValue", o);
  query.value = o;
  open = false;
}
function onInput() {
  open = true;
  emit("update:modelValue", query.value);
}
</script>
