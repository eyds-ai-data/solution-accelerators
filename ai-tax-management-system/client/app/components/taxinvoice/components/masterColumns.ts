import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import type { TaxInvoice } from '../data/schema'
import { formatNumber } from '@/components/gl/components/numbering'
import { Badge } from '@/components/ui/badge'

export const taxInvoiceMasterColumns: ColumnDef<TaxInvoice, any>[] = [
  // Auto-number column
  {
    id: 'index',
    header: 'No',
    cell: ({ row }) => h('div', { class: 'text-sm font-medium text-center' }, row.index + 1),
    enableSorting: false,
  },
  {
    accessorKey: 'taxInvoiceNumber',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Tax Invoice Number'),
    cell: ({ row }) => h('div', { class: 'text-sm font-mono' }, row.getValue('taxInvoiceNumber')),
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
    accessorKey: 'taxInvoiceDate',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Tax Invoice Date'),
    cell: ({ row }) => h('div', { class: 'text-sm' }, new Date(row.getValue('taxInvoiceDate')).toLocaleDateString()),
  },
  {
    accessorKey: 'namaPengusahaKenaPajak',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'PKP Name'),
    cell: ({ row }) => h('div', { class: 'text-sm break-words max-w-[200px] whitespace-normal' }, row.getValue('namaPengusahaKenaPajak')),
  },
  {
    accessorKey: 'npwpPengusahaKenaPajak',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'PKP NPWP'),
    cell: ({ row }) => h('div', { class: 'text-sm font-mono' }, row.getValue('npwpPengusahaKenaPajak')),
  },
  {
    accessorKey: 'namaPembeliKenaPajak',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Buyer Name'),
    cell: ({ row }) => h('div', { class: 'text-sm break-words max-w-[200px] whitespace-normal' }, row.getValue('namaPembeliKenaPajak')),
  },
  {
    accessorKey: 'npwpPembeliKenaPajak',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Buyer NPWP'),
    cell: ({ row }) => h('div', { class: 'text-sm font-mono' }, row.getValue('npwpPembeliKenaPajak')),
  },
  {
    accessorKey: 'dasarPengenaanPajak',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'DPP'),
    cell: ({ row }) => h('div', { class: 'text-sm text-right' }, formatNumber(row.getValue('dasarPengenaanPajak'))),
  },
  {
    accessorKey: 'jumlahPpn',
    header: ({ column }) => h('div', { class: 'text-sm font-medium text-right' }, 'PPN Amount'),
    cell: ({ row }) => h('div', { class: 'text-sm font-semibold text-right' }, formatNumber(row.getValue('jumlahPpn'))),
  },
  {
    accessorKey: 'createdAt',
    header: ({ column }) => h('div', { class: 'text-sm font-medium' }, 'Created At'),
    cell: ({ row }) => h('div', { class: 'text-sm text-muted-foreground' }, new Date(row.getValue('createdAt')).toLocaleString()),
  },
]
