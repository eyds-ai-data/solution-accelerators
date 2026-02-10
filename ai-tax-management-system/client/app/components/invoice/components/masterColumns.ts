import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import type { Invoice } from '../data/schema'
import { formatNumber } from '@/components/gl/components/numbering'
import { Badge } from '@/components/ui/badge'

export const invoiceMasterColumns: ColumnDef<Invoice, any>[] = [
  // Auto-number column
  {
    id: 'index',
    header: 'No',
    cell: ({ row }) => h('div', { class: 'text-sm font-medium text-center' }, row.index + 1),
    enableSorting: false,
  },
  {
    accessorKey: 'invoiceNumber',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Invoice Number'),
    cell: ({ row }) => h('div', { class: 'text-sm font-mono' }, row.getValue('invoiceNumber')),
  },
  {
    accessorKey: 'urn',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'URN'),
    cell: ({ row }) => h('div', { class: 'text-sm text-muted-foreground font-mono' }, row.getValue('urn')),
  },
  {
    accessorKey: 'projectNumber',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Project Number'),
    cell: ({ row }) => h('div', { class: 'text-sm' }, row.getValue('projectNumber')),
  },
  {
    accessorKey: 'currency',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Currency'),
    cell: ({ row }) => h(Badge, { variant: 'outline', class: 'text-xs' }, () => row.getValue('currency')),
  },
  {
    accessorKey: 'subTotalAmount',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'Subtotal'),
    cell: ({ row }) => h('div', { class: 'text-sm text-right' }, formatNumber(row.getValue('subTotalAmount'))),
  },
  {
    accessorKey: 'vatAmount',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'VAT Amount'),
    cell: ({ row }) => h('div', { class: 'text-sm text-right' }, formatNumber(row.getValue('vatAmount'))),
  },
  {
    accessorKey: 'discountAmount',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'Discount'),
    cell: ({ row }) => h('div', { class: 'text-sm text-right' }, formatNumber(row.getValue('discountAmount'))),
  },
  {
    accessorKey: 'whtAmount',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'WHT Amount'),
    cell: ({ row }) => h('div', { class: 'text-sm text-right' }, formatNumber(row.getValue('whtAmount'))),
  },
  {
    accessorKey: 'totalAmount',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'Total Amount'),
    cell: ({ row }) => h('div', { class: 'text-sm font-semibold text-right' }, formatNumber(row.getValue('totalAmount'))),
  },
  {
    accessorKey: 'createdAt',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Created At'),
    cell: ({ row }) => h('div', { class: 'text-sm text-muted-foreground' }, new Date(row.getValue('createdAt')).toLocaleString()),
  },
]
