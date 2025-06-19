<template>
  <v-text-field v-model="model" :type="type" v-bind="attrsWithoutClass" />
</template>

<script setup lang="ts">
import { computed, useAttrs } from "vue";
import { VTextField } from "vuetify/components";

const props = withDefaults(defineProps<{ modelValue?: any; type?: string }>(), {
  type: "text",
});
const emit = defineEmits(["update:modelValue"]);
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: _cls, ...rest } = attrs as any;
  return rest;
});

const model = computed({
  get: () => props.modelValue,
  set: (v) => emit("update:modelValue", v),
});
</script>
