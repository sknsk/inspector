<template>
  <div><slot /></div>
</template>
<script setup lang="ts">
import { ref, provide } from "vue";
const props = withDefaults(defineProps<{ modelValue?: string }>(), {
  modelValue: "",
});
const value = ref(props.modelValue);
provide("tabsValue", value);
provide("setTabsValue", (v: string) => {
  value.value = v;
});
</script>
