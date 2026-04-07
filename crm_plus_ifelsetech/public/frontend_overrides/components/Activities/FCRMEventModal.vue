<template>
  <Dialog
    v-model="show"
    :options="{
      title: __('Create Event'),
      size: 'xl',
    }"
  >
    <template #body-content>
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <FormControl
            v-model="event.subject"
            :label="__('Subject')"
            type="text"
            :required="true"
          />
          <FormControl
            v-model="event.status"
            :label="__('Status')"
            type="select"
            :options="['Open', 'Closed', 'Cancelled']"
            :required="true"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <FormControl
            v-model="event.event_category"
            :label="__('Event Category')"
            type="select"
            :options="['Event', 'Meeting', 'Call', 'Sent/Received Email', 'Other']"
          />
          <FormControl
            v-model="event.color"
            :label="__('Color')"
            type="color"
          />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <FormControl
            v-model="event.starts_on"
            :label="__('Starts On')"
            type="datetime-local"
            :required="true"
          />
          <FormControl
            v-model="event.ends_on"
            :label="__('Ends On')"
            type="datetime-local"
          />
        </div>

        <FormControl
          v-model="event.all_day"
          :label="__('All Day')"
          type="checkbox"
        />

        <FormControl
          v-model="event.description"
          :label="__('Description')"
          type="textarea"
          :rows="4"
        />
      </div>
    </template>
    <template #actions>
      <Button
        variant="solid"
        :label="__('Create')"
        :loading="saving"
        @click="createEvent"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Dialog, FormControl, Button, call, createResource } from 'frappe-ui'

const props = defineProps({
  modelValue: Boolean,
  dealName: String,
})

const emit = defineEmits(['update:modelValue', 'success'])

const show = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})

const event = ref({
  subject: '',
  status: 'Open',
  event_category: 'Meeting',
  starts_on: new Date().toISOString().slice(0, 16),
  ends_on: '',
  all_day: false,
  description: '',
  color: '#3b82f6',
})

const saving = ref(false)

async function createEvent() {
  if (!event.value.subject || !event.value.starts_on) {
    console.error('Subject and start time are required')
    return
  }

  saving.value = true

  try {
    const response = await call('crm_plus_ifelsetech.api.fcrm_event.create_event', {
      subject: event.value.subject,
      starts_on: event.value.starts_on,
      ends_on: event.value.ends_on || null,
      status: event.value.status,
      event_category: event.value.event_category,
      color: event.value.color,
      all_day: event.value.all_day ? 1 : 0,
      description: event.value.description,
      reference_doctype: 'CRM Deal',
      reference_docname: props.dealName,
    })

    emit('success', response)
    show.value = false
  } catch (error) {
    console.error('Error creating event:', error)
  } finally {
    saving.value = false
  }
}
</script>
