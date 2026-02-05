import type { NavMenu, NavMenuItems } from '~/types/nav'

export const navMenu: NavMenu[] = [
  {
    heading: '',
    items: [
      {
        title: 'Home',
        icon: 'i-lucide-home',
        link: '/',
      }
    ],
  },
  {
    heading: 'Tax Uploads',
    items: [
      {
        title: 'GL Table',
        icon: 'i-lucide-sheet',
        link: '/gl',
      },
    ],
  },
]

export const navMenuBottom: NavMenuItems = []
