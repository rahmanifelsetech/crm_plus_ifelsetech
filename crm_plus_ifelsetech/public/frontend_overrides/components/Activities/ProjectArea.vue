<template>
  <div>
    <div class="mb-4 flex items-center justify-between">
      <h3 class="text-base font-medium text-ink-gray-9">
        {{ projects.length > 0 ? __('Projects ({0})', [projects.length]) : __('No Projects') }}
      </h3>
      <Button
        variant="solid"
        :label="__('Create Project')"
        @click="showCreateModal = true"
      >
        <template #prefix>
          <FeatherIcon name="plus" class="h-4 w-4" />
        </template>
      </Button>
    </div>

    <div v-if="projects.length">
      <div v-for="(project, i) in projects" :key="project.name">
      <div
        class="activity flex cursor-pointer gap-6 rounded p-2.5 duration-300 ease-in-out hover:bg-surface-gray-1"
        @click="openProject(project)"
      >
        <div class="flex flex-1 flex-col gap-1.5 text-base truncate">
          <div class="flex items-center gap-2">
            <div class="font-medium text-ink-gray-9 truncate">
              {{ project.project_name }}
            </div>
            <Badge
              v-if="project.status"
              :variant="getStatusVariant(project.status)"
              :label="project.status"
            />
          </div>
          <div v-if="project.priority" class="text-sm text-ink-gray-8 truncate">
            {{ __('Priority') }}: {{ project.priority }}
          </div>
          <div class="flex gap-1.5 text-sm text-ink-gray-6">
            <div v-if="project.start_date" class="flex items-center gap-1.5">
              <CalendarIcon class="h-3.5 w-3.5" />
              {{ formatDate(project.start_date, 'D MMM, YYYY') }}
            </div>
            <div v-if="project.end_date" class="flex items-center justify-center">
              <DotIcon class="h-2.5 w-2.5 text-ink-gray-5" :radius="2" />
            </div>
            <div v-if="project.end_date" class="flex items-center gap-1.5">
              <span>{{ __('to') }}</span>
              {{ formatDate(project.end_date, 'D MMM, YYYY') }}
            </div>
            <div v-if="project.percent_complete" class="flex items-center justify-center">
              <DotIcon class="h-2.5 w-2.5 text-ink-gray-5" :radius="2" />
            </div>
            <div v-if="project.percent_complete" class="font-medium">
              {{ project.percent_complete }}% {{ __('complete') }}
            </div>
          </div>
        </div>
        <div class="flex items-center gap-1">
          <Dropdown
            :options="[
              {
                label: __('View'),
                icon: 'eye',
                onClick: () => openProject(project),
              },
              {
                label: __('Open in New Tab'),
                icon: 'external-link',
                onClick: () => window.open(`/app/project/${project.name}`, '_blank'),
              },
              {
                label: __('Delete'),
                icon: 'trash-2',
                onClick: () => {
                  $dialog({
                    title: __('Delete Project'),
                    message: __('Are you sure you want to delete this project?'),
                    actions: [
                      {
                        label: __('Delete'),
                        theme: 'red',
                        variant: 'solid',
                        onClick(close) {
                          deleteProject(project.name)
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
        v-if="i < projects.length - 1"
        class="mx-2 h-px border-t border-outline-gray-modals"
      />
    </div>
    </div>

    <CreateProjectModal
      v-if="showCreateModal"
      v-model="showCreateModal"
      :deal-name="dealName"
      @success="handleProjectCreated"
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
import CreateProjectModal from '../CreateProjectModal.vue'

const props = defineProps({
  projects: Array,
  dealName: String,
})

const emit = defineEmits(['reload'])

const { $dialog } = globalStore()
const showCreateModal = ref(false)

function handleProjectCreated(project) {
  showCreateModal.value = false
  emit('reload')
}

function getStatusVariant(status) {
  const variants = {
    'Open': 'blue',
    'Completed': 'green',
    'Cancelled': 'red',
    'Template': 'gray',
  }
  return variants[status] || 'subtle'
}

function openProject(project) {
  // Navigate to ERPNext project form
  window.location.href = `/app/project/${project.name}`
}

function editProject(project) {
  // Navigate to ERPNext project form
  window.location.href = `/app/project/${project.name}`
}

async function deleteProject(name) {
  try {
    await call('frappe.client.delete', {
      doctype: 'Project',
      name: name,
    })
    emit('reload')
  } catch (error) {
    console.error('Error deleting project:', error)
  }
}
</script>
