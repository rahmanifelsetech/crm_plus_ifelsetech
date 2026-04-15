<template>
  <Dialog v-model="show" :options="{ title: __('Create Project from Deal'), size: 'xl' }">
    <template #body-content>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Project Name') }}
          </label>
          <Input
            v-model="projectName"
            type="text"
            :placeholder="__('Enter project name')"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ __('Project Template (Optional)') }}
          </label>
          <Autocomplete
            v-model="selectedTemplate"
            :options="templateOptions"
            :placeholder="__('Select a project template')"
          />
        </div>

        <div v-if="selectedTemplate" class="bg-gray-50 p-3 rounded">
          <p class="text-sm text-gray-600">
            {{ __('Template') }}: <span class="font-medium">{{ selectedTemplate }}</span>
          </p>
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
        :label="__('Create Project')"
        :loading="creating"
        @click="createProject"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Dialog, Input, Autocomplete, createResource, call, toast } from 'frappe-ui'

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

const projectName = ref('')
const selectedTemplate = ref('')
const creating = ref(false)

// Load project templates
const templates = createResource({
  url: 'crm_plus_ifelsetech.api.project.get_project_templates',
  auto: true,
})

const templateOptions = computed(() => {
  if (!templates.data) return []
  return templates.data.map(t => ({
    label: t.name,
    value: t.name,
  }))
})

async function createProject() {
  if (!projectName.value) {
    toast.error(__('Please enter a project name'))
    return
  }

  creating.value = true
  try {
    const result = await call('crm_plus_ifelsetech.api.project.create_project_from_deal', {
      deal_name: props.dealName,
      project_name: projectName.value,
      project_template: selectedTemplate.value || null,
    })

    toast.success(__('Project created successfully'))

    // Reset form
    projectName.value = ''
    selectedTemplate.value = ''

    show.value = false
    emit('success', result)
  } catch (error) {
    console.error('Error creating project:', error)
    toast.error(error.messages?.[0] || __('Failed to create project'))
  } finally {
    creating.value = false
  }
}
</script>
