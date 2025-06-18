<template>
  <div v-show="tabsValue.value === value" class="mt-2"><slot /></div>
</template>
<script setup lang="ts">
import { inject } from "vue";
const props = defineProps<{ value: string }>();
const tabsValue = inject("tabsValue") as any;
</script>
