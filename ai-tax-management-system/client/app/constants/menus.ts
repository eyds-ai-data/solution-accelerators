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
        title: 'Reconciliation Process',
        icon: 'i-lucide-book-open',
        link: '/gl',
      },
      {
        title: 'Reference Data',
        icon: 'i-lucide-database',
        link: '/mdm',
      }
    ],
  },
]

export const navMenuBottom: NavMenuItems = [
  // {
  //   title: 'Master Data',
  //   icon: 'i-lucide-database',
  //   link: '/mdm',
  // },
  {
    title: 'Settings',
    icon: 'i-lucide-settings',
    link: '/settings',
  }
]
