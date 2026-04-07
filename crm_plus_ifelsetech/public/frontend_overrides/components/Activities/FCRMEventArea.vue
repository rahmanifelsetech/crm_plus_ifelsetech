<template>
  <div>
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-base font-medium text-ink-gray-9">
        {{ events.length > 0 ? __('Events ({0})', [events.length]) : __('No Events') }}
      </h3>
      <Button
        variant="solid"
        :label="__('Create Event')"
        @click="showCreateModal = true"
      >
        <template #prefix>
          <FeatherIcon name="plus" class="h-4 w-4" />
        </template>
      </Button>
    </div>

    <div v-if="events.length">
      <div v-for="(event, i) in events" :key="event.name">
      <div
        class="activity flex cursor-pointer gap-6 rounded p-2.5 duration-300 ease-in-out hover:bg-surface-gray-1"
        @click="openEvent(event)"
      >
        <div class="flex flex-1 flex-col gap-1.5 text-base truncate">
          <div class="flex items-center gap-2">
            <div class="font-medium text-ink-gray-9 truncate">
              {{ event.subject }}
            </div>
            <Badge
              v-if="event.status"
              :variant="getStatusVariant(event.status)"
              :label="event.status"
            />
          </div>
          <div v-if="event.event_category" class="text-sm text-ink-gray-8 truncate">
            {{ event.event_category }}
            <span v-if="event.event_type"> - {{ event.event_type }}</span>
          </div>
          <div class="flex gap-1.5 text-sm text-ink-gray-6">
            <div class="flex items-center gap-1.5">
              <CalendarIcon class="h-3.5 w-3.5" />
              {{ formatDate(event.starts_on, 'D MMM, YYYY h:mm A') }}
            </div>
            <div v-if="event.ends_on" class="flex items-center justify-center">
              <DotIcon class="h-2.5 w-2.5 text-ink-gray-5" :radius="2" />
            </div>
            <div v-if="event.ends_on" class="flex items-center gap-1.5">
              <span>{{ __('to') }}</span>
              {{ formatDate(event.ends_on, 'D MMM, YYYY h:mm A') }}
            </div>
          </div>
        </div>
        <div class="flex items-center gap-1">
          <Dropdown
            :options="[
              {
                label: __('View'),
                icon: 'eye',
                onClick: () => openEvent(event),
              },
              {
                label: __('Edit'),
                icon: 'edit',
                onClick: () => editEvent(event),
              },
              {
                label: __('Delete'),
                icon: 'trash-2',
                onClick: () => {
                  $dialog({
                    title: __('Delete Event'),
                    message: __('Are you sure you want to delete this event?'),
                    actions: [
                      {
                        label: __('Delete'),
                        theme: 'red',
                        variant: 'solid',
                        onClick(close) {
                          deleteEvent(event.name)
                          close()
                        },
                      },
                    ],
                  })
                },
              },
            ]"
            @click.stop
          >
            <Button
              icon="more-horizontal"
              variant="ghosted"
              class="hover:bg-surface-gray-4 text-ink-gray-9"
            />
          </Dropdown>
        </div>
      </div>
      <div
        v-if="i < events.length - 1"
        class="mx-2 h-px border-t border-outline-gray-modals"
      />
    </div>
    </div>

    <FCRMEventModal
      v-if="showCreateModal"
      v-model="showCreateModal"
      :deal-name="dealName"
      @success="handleEventCreated"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CalendarIcon from '@/components/Icons/CalendarIcon.vue'
import DotIcon from '@/components/Icons/DotIcon.vue'
import { formatDate } from '@/utils'
import { globalStore } from '@/stores/global'
import { call, Badge, Dropdown, Button, FeatherIcon } from 'frappe-ui'
import FCRMEventModal from './FCRMEventModal.vue'

const props = defineProps({
  events: Array,
  dealName: String,
})

const emit = defineEmits(['reload'])

const { $dialog } = globalStore()
const showCreateModal = ref(false)

function handleEventCreated(event) {
  showCreateModal.value = false
  emit('reload')
}

function getStatusVariant(status) {
  const variants = {
    'Open': 'blue',
    'Closed': 'green',
    'Cancelled': 'red',
  }
  return variants[status] || 'subtle'
}

function openEvent(event) {
  window.open(`/app/fcrm-event/${event.name}`, '_blank')
}

function editEvent(event) {
  window.open(`/app/fcrm-event/${event.name}`, '_blank')
}

async function deleteEvent(name) {
  try {
    await call('crm_plus_ifelsetech.api.fcrm_event.delete_event', {
      name: name,
    })
    emit('reload')
  } catch (error) {
    console.error('Error deleting event:', error)
  }
}
</script>
