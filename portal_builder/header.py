# -*- coding: utf-8 -*-

def get_header():
    return """<!DOCTYPE html>
<html lang="de" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visar Murseli | Enterprise Knowledge Hub & S/4HANA Career OS</title>
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Vue 3 via CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            ssb: {
              yellow: '#FFDD00',
              dark: '#0F172A',
              navy: '#0B1329',
              accent: '#2563EB',
              amber: '#D97706',
              success: '#059669',
              slate: '#334155'
            }
          }
        }
      }
    }
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    code, pre {
      font-family: 'JetBrains Mono', monospace;
    }
    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #f1f5f9;
    }
    .dark .custom-scrollbar::-webkit-scrollbar-track {
      background: #0f172a;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #94a3b8;
      border-radius: 3px;
    }
    .dark .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #334155;
    }
    .tag-badge {
      display: inline-flex;
      align-items: center;
      padding: 0.15rem 0.5rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 600;
    }
  </style>
</head>
<body class="h-full bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100 flex flex-col custom-scrollbar transition-colors duration-200">
  <div id="app" class="flex-1 flex flex-col min-h-screen">
    
    <!-- Top Global Header -->
    <header class="sticky top-0 z-50 bg-white/95 dark:bg-slate-900/95 backdrop-blur border-b border-slate-200 dark:border-slate-800 px-4 lg:px-8 py-2.5 transition-colors">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 via-yellow-400 to-amber-500 flex items-center justify-center font-extrabold text-slate-900 shadow-md">
            VM
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h1 class="text-base sm:text-lg font-bold tracking-tight text-slate-900 dark:text-white">
                Visar Murseli | Enterprise Knowledge Hub & S/4HANA Career OS
              </h1>
              <span class="bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">M.Sc. 1,6 | Thesis 1,0</span>
            </div>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              24 Monate IT-PMO S/4HANA bei der Stuttgarter Straßenbahnen AG | ERP-Transformation, Plattformisierung & Clean Core Governance
            </p>
          </div>
        </div>

        <!-- Global Search & Actions -->
        <div class="flex items-center space-x-3">
          <div class="relative w-full md:w-80">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Suche im Wissensportal (Clean Core, SuSa, CALM, BTP)..." 
              class="w-full pl-9 pr-8 py-1.5 text-xs bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-slate-900 dark:text-white"
            >
            <span class="absolute left-3 top-2 text-slate-400">🔍</span>
            <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-2.5 top-1.5 text-xs text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">✕</button>
          </div>

          <!-- Dark Mode Toggle -->
          <button 
            @click="toggleDarkMode" 
            class="p-2 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition"
            :title="isDark ? 'Heller Modus' : 'Dunkler Modus'"
          >
            <span v-if="isDark">☀️</span>
            <span v-else>🌙</span>
          </button>
        </div>
      </div>

      <!-- Navigation Tabs Bar -->
      <div class="max-w-7xl mx-auto mt-2.5 overflow-x-auto flex space-x-1 border-t border-slate-100 dark:border-slate-800 pt-2 custom-scrollbar">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all flex items-center space-x-1.5',
            activeTab === tab.id 
              ? 'bg-blue-600 text-white shadow-sm ring-1 ring-blue-500' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/80'
          ]"
        >
          <span>{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
          <span v-if="tab.badge" :class="[
            'ml-1 px-1.5 py-0.2 text-[9px] rounded-full font-bold',
            tab.badgeColor || 'bg-white/20 text-white'
          ]">{{ tab.badge }}</span>
        </button>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 lg:px-8 py-6 space-y-6">
      
      <!-- Search Filter Alert if Active -->
      <div v-if="searchQuery" class="p-3 bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800 rounded-xl flex items-center justify-between text-xs text-blue-900 dark:text-blue-200">
        <div class="flex items-center space-x-2">
          <span>🔍</span>
          <span>Suchfilter aktiv für: <strong>"{{ searchQuery }}"</strong>. Durchsucht das gesamte Wissensportal, Konzepte, Q&A und Dokumente.</span>
        </div>
        <button @click="searchQuery = ''" class="font-bold underline hover:text-blue-700">Filter zurücksetzen</button>
      </div>
"""
