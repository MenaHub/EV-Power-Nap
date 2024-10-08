const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/MapPage.vue') },
      { path: '/vehicles', component: () => import('pages/VehiclePage.vue') },
      { path: '/account', component: () => import('pages/AccountPage.vue') },
      { path: '/registration', component: () => import('pages/RegistrationPage.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
