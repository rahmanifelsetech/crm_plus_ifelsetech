<template>
  <Dropdown :options="statusOptions" placement="left">
    <template #default="{ open }">
      <Button variant="ghost" class="!px-2">
        <template #prefix>
          <div class="flex items-center gap-2">
            <div
              :class="[
                'h-2.5 w-2.5 rounded-full',
                statusIndicatorClass
              ]"
            ></div>
            <span class="text-sm font-medium">{{ currentStatus }}</span>
          </div>
        </template>
        <template #suffix>
          <FeatherIcon
            :name="open ? 'chevron-up' : 'chevron-down'"
            class="h-4 w-4 text-ink-gray-6"
          />
        </template>
      </Button>
    </template>
  </Dropdown>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Dropdown, Button, createResource, FeatherIcon, toast } from 'frappe-ui'

const currentStatus = ref('Available')
const isLoading = ref(false)

const statusOptions = computed(() => [
  {
    label: 'Available',
    icon: 'circle',
    iconClasses: 'text-green-500',
    onClick: () => updateStatus('Available'),
  },
  {
    label: 'Busy',
    icon: 'circle',
    iconClasses: 'text-red-500',
    onClick: () => updateStatus('Busy'),
  },
  {
    label: 'Free',
    icon: 'circle',
    iconClasses: 'text-blue-500',
    onClick: () => updateStatus('Free'),
  },
  {
    label: 'Do Not Disturb',
    icon: 'circle',
    iconClasses: 'text-gray-500',
    onClick: () => updateStatus('Do Not Disturb'),
  },
])

const statusIndicatorClass = computed(() => {
  const statusColors = {
    'Available': 'bg-green-500',
    'Busy': 'bg-red-500',
    'Free': 'bg-blue-500',
    'Do Not Disturb': 'bg-gray-500',
  }
  return statusColors[currentStatus.value] || 'bg-gray-400'
})

const userStatus = createResource({
  url: 'crm_plus_ifelsetech.api.user_status.get_user_status',
  auto: true,
  onSuccess(data) {
    currentStatus.value = data.status || 'Available'
  },
})

const updateUserStatusResource = createResource({
  url: 'crm_plus_ifelsetech.api.user_status.update_user_status',
  onSuccess(data) {
    currentStatus.value = data.status || currentStatus.value
    toast.success(`Status updated to ${data.status}`)
  },
  onError(error) {
    console.error('Error updating status:', error)
    toast.error('Failed to update status')
  },
})

async function updateStatus(status) {
  if (isLoading.value) return

  isLoading.value = true
  try {
    await updateUserStatusResource.submit({ status })
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (!userStatus.data) {
    userStatus.fetch()
  }
})
</script>
