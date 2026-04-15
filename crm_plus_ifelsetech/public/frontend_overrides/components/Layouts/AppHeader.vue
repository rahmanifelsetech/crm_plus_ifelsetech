<template>
  <div class="flex border-b pr-5">
    <div id="app-header" class="flex-1"></div>
    <div class="flex items-center justify-center gap-3">
      <UserStatusDropdown />
      <CallUI />
    </div>
  </div>
</template>

<script setup>
import CallUI from '@/components/Telephony/CallUI.vue'
import UserStatusDropdown from '../UserStatusDropdown.vue'
</script>
