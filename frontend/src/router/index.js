/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

Vue.use(Router)
import HelloWorld from '@/components/HelloWorld.vue'
import settlement from '@/components/settlement'
import Rule from '@/components/Rule'
import User from '@/components/User'
import Member from '@/components/Member'
import nopick from '@/components/nopick'
import person from '@/components/person'
import financial from '@/components/financial'
import nojoin from '@/components/nojoin'
import dataView from '@/components/dataView'


export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/User',
      name: 'User',
      component: User
    },
    {
      path: '/person',
      name: 'person',
      component: person
    },
    {
      path: '/settlement',
      name: 'settlement',
      component: settlement
    },
    {
      path: '/Rule',
      name: 'Rule',
      component: Rule
    },
    {
      path: '/HelloWorld',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/Member',
      name: 'Member',
      component: Member
    },
    {
      path: '/nopick',
      name: 'nopick',
      component: nopick
    },
    {
      path: '/financial',
      name: 'financial',
      component: financial
    },
    {
      path: '/nojoin',
      name: 'nojoin',
      component: nojoin
    },
    {
      path: '/dataView',
      name: 'dataView',
      component: dataView
    }
  ]
})
