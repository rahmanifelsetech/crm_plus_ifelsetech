<template>
  <div v-if="quotations.length">
    <div v-for="(quotation, i) in quotations" :key="quotation.name">
      <div
        class="activity flex cursor-pointer gap-6 rounded p-2.5 duration-300 ease-in-out hover:bg-surface-gray-1"
        @click="openQuotation(quotation)"
      >
        <div class="flex flex-1 flex-col gap-1.5 text-base truncate">
          <div class="flex items-center gap-2">
            <div class="font-medium text-ink-gray-9 truncate">
              {{ quotation.name }}
            </div>
            <Badge
              :variant="getStatusVariant(quotation.status)"
              :label="quotation.status"
            />
          </div>
          <div class="text-sm text-ink-gray-8 truncate">
            {{ quotation.party_name }}
          </div>
          <div class="flex gap-1.5 text-sm text-ink-gray-6">
            <div class="flex items-center gap-1.5">
              <CalendarIcon class="h-3.5 w-3.5" />
              {{ formatDate(quotation.transaction_date, 'D MMM, YYYY') }}
            </div>
            <div v-if="quotation.valid_till" class="flex items-center justify-center">
              <DotIcon class="h-2.5 w-2.5 text-ink-gray-5" :radius="2" />
            </div>
            <div v-if="quotation.valid_till" class="flex items-center gap-1.5">
              <span>{{ __('Valid till') }}:</span>
              {{ formatDate(quotation.valid_till, 'D MMM, YYYY') }}
            </div>
            <div v-if="quotation.grand_total" class="flex items-center justify-center">
              <DotIcon class="h-2.5 w-2.5 text-ink-gray-5" :radius="2" />
            </div>
            <div v-if="quotation.grand_total" class="font-medium">
              {{ formatCurrency(quotation.grand_total, quotation.currency) }}
            </div>
          </div>
        </div>
        <div class="flex items-center gap-1">
          <Dropdown
            :options="[
              {
                label: __('View'),
                icon: 'eye',
                onClick: () => openQuotation(quotation),
              },
              {
                label: __('Edit'),
                icon: 'edit',
                onClick: () => editQuotation(quotation),
              },
              {
                label: __('Delete'),
                icon: 'trash-2',
                onClick: () => {
                  $dialog({
                    title: __('Delete Quotation'),
                    message: __('Are you sure you want to delete this quotation?'),
                    actions: [
                      {
                        label: __('Delete'),
                        theme: 'red',
                        variant: 'solid',
                        onClick(close) {
                          deleteQuotation(quotation.name)
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
        v-if="i < quotations.length - 1"
        class="mx-2 h-px border-t border-outline-gray-modals"
      />
    </div>
  </div>
</template>

<script setup>
import CalendarIcon from '@/components/Icons/CalendarIcon.vue'
import DotIcon from '@/components/Icons/DotIcon.vue'
import { formatDate } from '@/utils'
import { globalStore } from '@/stores/global'
import { call, Badge, Dropdown } from 'frappe-ui'

const props = defineProps({
  quotations: Array,
})

const emit = defineEmits(['reload'])

const { $dialog } = globalStore()

function formatCurrency(amount, currency = 'USD') {
  if (!amount) return '-'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency || 'USD',
  }).format(amount)
}

function getStatusVariant(status) {
  const variants = {
    'Draft': 'subtle',
    'Sent': 'blue',
    'Accepted': 'green',
    'Rejected': 'red',
    'Expired': 'gray',
    'Cancelled': 'red',
  }
  return variants[status] || 'subtle'
}

function openQuotation(quotation) {
  window.open(`/app/crm-quotation/${quotation.name}`, '_blank')
}

function editQuotation(quotation) {
  window.open(`/app/crm-quotation/${quotation.name}`, '_blank')
}

async function deleteQuotation(name) {
  try {
    await call('frappe.client.delete', {
      doctype: 'CRM Quotation',
      name: name,
    })
    emit('reload')
  } catch (error) {
    console.error('Error deleting quotation:', error)
  }
}
</script>
