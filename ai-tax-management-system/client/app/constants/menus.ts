import type { NavMenu, NavMenuItems } from '~/types/nav'

export const navMenu: NavMenu[] = [
  {
    heading: '',
    items: [
      {
        title: 'Dashboard',
        icon: 'i-lucide-layout-dashboard',
        link: '/',
      }
    ],
  },
  {
    heading: 'WHT Management',
    items: [
      {
        title: 'GL Transactions',
        icon: 'i-lucide-book-open',
        link: '/gl',
      }
    ],
  },
]

export const navMenuBottom: NavMenuItems = [
  {
    title: 'Master Data',
    icon: 'i-lucide-database',
    link: '/mdm',
  },
]
