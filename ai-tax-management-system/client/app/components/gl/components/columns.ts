import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import { Badge } from '@/components/ui/badge'
import { Checkbox } from '@/components/ui/checkbox'
import type { GL } from '../data/schema'
import DataTableColumnHeader from './DataTableColumnHeader.vue'
import DataTableRowActions from './DataTableRowActions.vue'
import { FileText, Receipt, CircleAlert } from 'lucide-vue-next'
import { NuxtLink } from '#components'

export const columns: ColumnDef<GL>[] = [
  {
    id: 'select',
    header: ({ table }) => h(Checkbox, {
      'checked': table.getIsAllPageRowsSelected() || (table.getIsSomePageRowsSelected() && 'indeterminate'),
      'onUpdate:checked': (value: any) => table.toggleAllPageRowsSelected(!!value),
      'ariaLabel': 'Select all',
      'class': 'translate-y-0.5',
    }),
    cell: ({ row }) => h(Checkbox, { 'checked': row.getIsSelected(), 'onUpdate:checked': (value: any) => row.toggleSelected(!!value), 'ariaLabel': 'Select row', 'class': 'translate-y-0.5' }),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: 'vendorName',
    header: ({ column }) => h(DataTableColumnHeader, { column, title: 'Vendor Name' }),
    cell: ({ row }) => h('div', { class: 'text-sm text-muted-foreground' }, row.getValue('vendorName')),
  },
  {
    accessorKey: 'referenceNumber',
    header: ({ column }) => h(DataTableColumnHeader, { column, title: 'Reference Number' }),
    cell: ({ row }) => h('div', { class: 'text-sm' }, row.getValue('referenceNumber')),
  },
  {
    id: 'invoice',
    header: ({ column }) => h(DataTableColumnHeader, { column, title: 'Invoice' }),
    cell: ({ row }) => {
      const invoiceData = row.original.relatedInvoice
      if (invoiceData) {
        return h(NuxtLink, {
          to: `/mdm/invoice/${invoiceData.invoiceId}`,
          class: 'flex items-center gap-1.5 text-sm text-primary hover:underline',
          onClick: (e: Event) => e.stopPropagation(),
        }, () => [
          h(FileText, { class: 'size-4 shrink-0' }),
          h('span', { class: 'truncate max-w-[120px]' }, invoiceData.invoiceNumber || 'View'),
        ])
      }
      return h('div', { class: 'flex items-center gap-1.5 text-sm text-muted-foreground/50' }, [
        h(CircleAlert, { class: 'size-4 shrink-0 text-destructive' }),
        h('span', {}, 'Missing'),
      ])
    },
    enableSorting: false,
  },
  {
    id: 'taxInvoice',
    header: ({ column }) => h(DataTableColumnHeader, { column, title: 'Tax Invoice' }),
    cell: ({ row }) => {
      const taxInvoiceData = row.original.relatedTaxInvoice
      if (taxInvoiceData) {
        return h(NuxtLink, {
          to: `/mdm/tax-invoice/${taxInvoiceData.taxInvoiceId}`,
          class: 'flex items-center gap-1.5 text-sm text-primary hover:underline',
          onClick: (e: Event) => e.stopPropagation(),
        }, () => [
          h(Receipt, { class: 'size-4 shrink-0' }),
          h('span', { class: 'truncate max-w-[120px]' }, taxInvoiceData.taxInvoiceNumber || 'View'),
        ])
      }
      return h('div', { class: 'flex items-center gap-1.5 text-sm text-muted-foreground/50' }, [
        h(CircleAlert, { class: 'size-4 shrink-0 text-destructive' }),
        h('span', {}, 'Missing'),
      ])
    },
    enableSorting: false,
  },
  {
    accessorKey: 'documentDate',
    header: ({ column }) => h(DataTableColumnHeader, { column, title: 'Document Date' }),
    cell: ({ row }) => {
      const date = new Date(row.getValue('documentDate') as string)
      return h('div', { class: 'text-sm' }, date.toLocaleDateString())
    },
  },
  {
    id: 'actions',
    cell: ({ row }) => h(DataTableRowActions, { row }),
  },
]
