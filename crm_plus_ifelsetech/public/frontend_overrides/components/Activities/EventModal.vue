<template>
  <Dialog v-model="show" :options="{ title: __('Create Event'), size: 'xl' }">
    <template #body-content>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Subject') }} <span class="text-red-500">*</span>
          </label>
          <Input
            v-model="eventData.subject"
            type="text"
            :placeholder="__('Enter event subject')"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Event Category') }}
            </label>
            <Autocomplete
              v-model="eventData.event_category"
              :options="categoryOptions"
              :placeholder="__('Select category')"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Status') }}
            </label>
            <Autocomplete
              v-model="eventData.status"
              :options="statusOptions"
              :placeholder="__('Select status')"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Starts On') }} <span class="text-red-500">*</span>
            </label>
            <Input
              v-model="eventData.starts_on"
              type="datetime-local"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ __('Ends On') }}
            </label>
            <Input
              v-model="eventData.ends_on"
              type="datetime-local"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Description') }}
          </label>
          <textarea
            v-model="eventData.description"
            rows="4"
            class="form-textarea block w-full rounded border-gray-300"
            :placeholder="__('Enter event description')"
          />
        </div>

        <div>
          <label class="flex items-center gap-2">
            <input
              v-model="eventData.all_day"
              type="checkbox"
              class="form-checkbox"
            />
            <span class="text-sm text-gray-700">{{ __('All Day Event') }}</span>
          </label>
        </div>
      </div>
    </template>
    <template #actions>
      <Button
        variant="solid"
        theme="gray"
        :label="__('Cancel')"
        @click="show = false"
      />
      <Button
        variant="solid"
        :label="__('Create Event')"
        :loading="creating"
        @click="createEvent"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Dialog, Input, Autocomplete, Button, call } from 'frappe-ui'

const props = defineProps({
  dealName: {
    type: String,
    required: true,
  },
  modelValue: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'success'])

const show = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const eventData = ref({
  subject: '',
  event_category: 'Event',
  status: 'Open',
  starts_on: '',
  ends_on: '',
  description: '',
  all_day: false,
})

const creating = ref(false)

const categoryOptions = [
  { label: 'Event', value: 'Event' },
  { label: 'Meeting', value: 'Meeting' },
  { label: 'Call', value: 'Call' },
  { label: 'Sent/Received Email', value: 'Sent/Received Email' },
  { label: 'Other', value: 'Other' },
]

const statusOptions = [
  { label: 'Open', value: 'Open' },
  { label: 'Closed', value: 'Closed' },
  { label: 'Cancelled', value: 'Cancelled' },
]

async function createEvent() {
  if (!eventData.value.subject) {
    window.frappe?.show_alert?.({
      title: __('Error'),
      message: __('Please enter event subject'),
      indicator: 'red',
    })
    return
  }

  if (!eventData.value.starts_on) {
    window.frappe?.show_alert?.({
      title: __('Error'),
      message: __('Please enter start date and time'),
      indicator: 'red',
    })
    return
  }

  creating.value = true
  try {
    const result = await call('frappe.client.insert', {
      doc: {
        doctype: 'Event',
        subject: eventData.value.subject,
        event_category: eventData.value.event_category,
        status: eventData.value.status,
        starts_on: eventData.value.starts_on,
        ends_on: eventData.value.ends_on || null,
        description: eventData.value.description,
        all_day: eventData.value.all_day ? 1 : 0,
        crm_deal: props.dealName,
      }
    })

    window.frappe?.show_alert?.({
      title: __('Success'),
      message: __('Event created successfully'),
      indicator: 'green',
    })

    show.value = false
    emit('success', result)

    // Reset form
    eventData.value = {
      subject: '',
      event_category: 'Event',
      status: 'Open',
      starts_on: '',
      ends_on: '',
      description: '',
      all_day: false,
    }
  } catch (error) {
    console.error('Error creating event:', error)
    window.frappe?.show_alert?.({
      title: __('Error'),
      message: error.messages?.[0] || __('Failed to create event'),
      indicator: 'red',
    })
  } finally {
    creating.value = false
  }
}
</script>
