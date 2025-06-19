<template>
  <v-label v-bind="attrsWithoutClass" :for="forId">
    <slot />
  </v-label>
</template>

<script setup lang="ts">
import { computed, useAttrs } from "vue";
import { VLabel } from "vuetify/components";

const props = defineProps<{ forId?: string }>();
const attrs = useAttrs();
const attrsWithoutClass = computed(() => {
  const { class: _cls, ...rest } = attrs as any;
  return rest;
});
</script>
