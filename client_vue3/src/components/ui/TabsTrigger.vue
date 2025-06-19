<template>
  <button
    @click="setTabsValue(value)"
    :class="[
      'px-3 py-1 text-sm rounded-md',
      isActive ? 'bg-white shadow' : 'bg-transparent',
    ]"
  >
    <slot />
  </button>
</template>
<script setup lang="ts">
import { inject, computed } from "vue";
const props = defineProps<{ value: string }>();
const tabsValue = inject("tabsValue") as any;
const setTabsValue = inject("setTabsValue") as (v: string) => void;
const isActive = computed(() => tabsValue.value === props.value);
</script>
