# -*- coding: utf-8 -*-

def get_header(public_mode=False):
    tpl = """<!DOCTYPE html>
<html lang="de" class="min-h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visar Murseli | Enterprise Knowledge Hub & S/4HANA Career OS</title>
  
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Vue 3 via CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  
  <!-- Modern Enterprise Theme Configuration -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#eff6ff',
              100: '#dbeafe',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8'
            }
          },
          fontFamily: {
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
            mono: ['JetBrains Mono', 'Fira Code', 'monospace']
          }
        }
      }
    }
  </script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* ================= MODERN EXECUTIVE DESIGN TOKENS (LIGHT & DARK) ================= */
    :root {
      color-scheme: light;
      --ds-surface: #F8FAFC;
      --ds-surface-sunken: #F1F5F9;
      --ds-surface-raised: #FFFFFF;
      --ds-surface-overlay: #FFFFFF;
      --ds-surface-hovered: #E2E8F0;
      --ds-surface-neutral: #F1F5F9;
      --ds-text: #0F172A;
      --ds-text-subtle: #334155;
      --ds-text-subtlest: #64748B;
      --ds-text-brand: #2563EB;
      --ds-brand-bold: #2563EB;
      --ds-brand-hovered: #1D4ED8;
      --ds-brand-subtlest: #EFF6FF;
      --ds-border: #E2E8F0;
      --ds-border-bold: #94A3B8;
      --ds-border-brand: #93C5FD;
      --ds-shadow-raised: 0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04);
      --ds-shadow-lifted: 0 10px 25px -5px rgba(37, 99, 235, 0.12), 0 4px 10px -2px rgba(15, 23, 42, 0.05);
      --ds-shadow-overlay: 0 12px 32px rgba(15, 23, 42, 0.14);

      --ds-bg-success: #ECFDF5;
      --ds-text-success: #047857;
      --ds-border-success: #6EE7B7;

      --ds-bg-warning: #FFFBEB;
      --ds-text-warning: #B45309;
      --ds-border-warning: #FCD34D;

      --ds-bg-danger: #FEF2F2;
      --ds-text-danger: #B91C1C;
      --ds-border-danger: #FCA5A5;

      --ds-bg-discovery: #F5F3FF;
      --ds-text-discovery: #6D28D9;
      --ds-border-discovery: #C4B5FD;
    }

    html.dark {
      color-scheme: dark;
      --ds-surface: #0B1120;
      --ds-surface-sunken: #0F172A;
      --ds-surface-raised: #161F33;
      --ds-surface-overlay: #1E293B;
      --ds-surface-hovered: #1E293B;
      --ds-surface-neutral: rgba(148, 163, 184, 0.12);
      --ds-text: #F1F5F9;
      --ds-text-subtle: #CBD5E1;
      --ds-text-subtlest: #94A3B8;
      --ds-text-brand: #60A5FA;
      --ds-brand-bold: #2563EB;
      --ds-brand-hovered: #3B82F6;
      --ds-brand-subtlest: rgba(37, 99, 235, 0.16);
      --ds-border: rgba(148, 163, 184, 0.18);
      --ds-border-bold: #475569;
      --ds-border-brand: rgba(96, 165, 250, 0.45);
      --ds-shadow-raised: 0 4px 16px rgba(0, 0, 0, 0.35);
      --ds-shadow-lifted: 0 12px 28px -4px rgba(37, 99, 235, 0.25);
      --ds-shadow-overlay: 0 16px 40px rgba(0, 0, 0, 0.6);

      --ds-bg-success: rgba(16, 185, 129, 0.14);
      --ds-text-success: #6EE7B7;
      --ds-border-success: rgba(16, 185, 129, 0.35);

      --ds-bg-warning: rgba(245, 158, 11, 0.14);
      --ds-text-warning: #FCD34D;
      --ds-border-warning: rgba(245, 158, 11, 0.35);

      --ds-bg-danger: rgba(239, 68, 68, 0.14);
      --ds-text-danger: #FCA5A5;
      --ds-border-danger: rgba(239, 68, 68, 0.35);

      --ds-bg-discovery: rgba(139, 92, 246, 0.15);
      --ds-text-discovery: #C4B5FD;
      --ds-border-discovery: rgba(139, 92, 246, 0.35);
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--ds-surface);
      color: var(--ds-text);
      overflow-x: clip;
      font-size: 14px;
      line-height: 1.55;
    }

    code, pre {
      font-family: 'JetBrains Mono', monospace;
    }

    .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: var(--ds-border-bold);
      border-radius: 9999px;
      opacity: 0.45;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: var(--ds-brand-bold); }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

    /* ================= DYNAMIC ANIMATIONS & MICRO-INTERACTIONS ================= */
    @keyframes tabReveal {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    #app main > div[v-show] {
      animation: tabReveal 0.28s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .app-topbar {
      background-color: var(--ds-surface-raised);
      border-bottom: 1px solid var(--ds-border);
      color: var(--ds-text);
      backdrop-filter: blur(12px);
    }
    .app-sidebar {
      background-color: var(--ds-surface-sunken);
      border-right: 1px solid var(--ds-border);
      color: var(--ds-text);
    }
    .app-canvas {
      background-color: var(--ds-surface);
      color: var(--ds-text);
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 9999px;
      font-size: 10.5px;
      font-weight: 600;
      letter-spacing: 0.01em;
      line-height: 1.3;
      white-space: nowrap;
    }
    .status-pill-blue { background-color: var(--ds-brand-subtlest); color: var(--ds-text-brand); border: 1px solid var(--ds-border-brand); }
    .status-pill-green { background-color: var(--ds-bg-success); color: var(--ds-text-success); border: 1px solid var(--ds-border-success); }
    .status-pill-amber { background-color: var(--ds-bg-warning); color: var(--ds-text-warning); border: 1px solid var(--ds-border-warning); }
    .status-pill-red { background-color: var(--ds-bg-danger); color: var(--ds-text-danger); border: 1px solid var(--ds-border-danger); }
    .status-pill-purple { background-color: var(--ds-bg-discovery); color: var(--ds-text-discovery); border: 1px solid var(--ds-border-discovery); }
    .status-pill-neutral { background-color: var(--ds-surface-neutral); color: var(--ds-text-subtle); border: 1px solid var(--ds-border); }

    .info-callout {
      background: linear-gradient(135deg, var(--ds-brand-subtlest) 0%, var(--ds-surface-raised) 100%);
      border: 1px solid var(--ds-border-brand);
      border-left: 4px solid var(--ds-brand-bold);
      border-radius: 12px;
      color: var(--ds-text);
    }

    .nav-item {
      position: relative;
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      padding: 8px 11px;
      border-radius: 10px;
      font-size: 13px;
      text-align: left;
      transition: transform 0.16s ease, background-color 0.15s ease, color 0.15s ease;
      color: var(--ds-text-subtle);
    }
    .nav-item:hover {
      background-color: var(--ds-surface-hovered);
      color: var(--ds-text);
      transform: translateX(2px);
    }
    .nav-item.active {
      background-color: var(--ds-brand-subtlest);
      color: var(--ds-text-brand);
      font-weight: 600;
      box-shadow: inset 0 0 0 1px var(--ds-border-brand);
    }

    /* Interactive Card Lift inside Content */
    #app main .cursor-pointer,
    #app main button.rounded-xl {
      transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.18s ease, border-color 0.18s ease;
    }
    #app main .cursor-pointer:hover,
    #app main button.rounded-xl:hover {
      transform: translateY(-2px);
      box-shadow: var(--ds-shadow-lifted) !important;
    }

    /* ================= SYSTEMATIC SEMANTIC TOKEN MAPPING FOR ALL 14 TABS ================= */
    #app main .rounded-2xl { border-radius: 14px !important; }
    #app main .rounded-xl { border-radius: 10px !important; }

    #app main .bg-\\[\\#0d0d0d\\] {
      background-color: var(--ds-surface) !important;
    }
    #app main .bg-\\[\\#141414\\],
    #app main .bg-\\[\\#121212\\],
    #app main .bg-\\[\\#181818\\],
    #app main .bg-\\[\\#111111\\],
    #app main .glass-card {
      background-color: var(--ds-surface-raised) !important;
      border-color: var(--ds-border) !important;
      box-shadow: var(--ds-shadow-raised) !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
    }
    #app main [class*="bg-gradient-to-"] {
      background: var(--ds-surface-raised) !important;
      background-image: none !important;
      border: 1px solid var(--ds-border) !important;
      border-left: 4px solid var(--ds-brand-bold) !important;
      box-shadow: var(--ds-shadow-raised) !important;
    }
    #app main .bg-white\\/5,
    #app main .bg-white\\/10,
    #app main .bg-black\\/20,
    #app main .bg-black\\/30,
    #app main .bg-black\\/40,
    #app main .bg-black\\/50,
    #app main .bg-black\\/60 {
      background-color: var(--ds-surface-sunken) !important;
      border-color: var(--ds-border) !important;
    }

    /* Typography Hierarchy */
    #app main .text-white,
    #app main .text-\\[\\#f5f3f3\\] {
      color: var(--ds-text) !important;
    }
    #app main .text-\\[\\#c4bebe\\],
    #app main .text-\\[\\#d6d0d0\\],
    #app main .text-\\[\\#f0eded\\] {
      color: var(--ds-text-subtle) !important;
    }
    #app main .text-\\[\\#8f8888\\] {
      color: var(--ds-text-subtlest) !important;
    }

    /* Modern Indigo/Blue Accent Remapping */
    #app main .bg-\\[\\#bf262e\\],
    #app .btn-primary {
      background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
      color: #FFFFFF !important;
      border-color: transparent !important;
      box-shadow: 0 2px 10px rgba(37, 99, 235, 0.25) !important;
    }
    #app main .bg-\\[\\#bf262e\\]:hover,
    #app main .hover\\:bg-\\[\\#cf3840\\]:hover,
    #app .btn-primary:hover {
      background: linear-gradient(135deg, #1D4ED8 0%, #4338CA 100%) !important;
      color: #FFFFFF !important;
    }
    #app main .bg-\\[\\#bf262e\\] *,
    #app .btn-primary * {
      color: #FFFFFF !important;
    }
    #app main .text-\\[\\#bf262e\\],
    #app main .text-\\[\\#f87171\\] {
      color: var(--ds-text-brand) !important;
    }
    #app main .bg-\\[\\#bf262e\\]\\/10,
    #app main .bg-\\[\\#bf262e\\]\\/15,
    #app main .bg-\\[\\#bf262e\\]\\/20,
    #app main .bg-\\[\\#bf262e\\]\\/30,
    #app main .hover\\:bg-\\[\\#bf262e\\]\\/10:hover,
    #app main .hover\\:bg-\\[\\#bf262e\\]\\/15:hover {
      background-color: var(--ds-brand-subtlest) !important;
    }
    #app main .border-\\[\\#bf262e\\]\\/30,
    #app main .border-\\[\\#bf262e\\]\\/40,
    #app main .border-\\[\\#bf262e\\]\\/50,
    #app main .hover\\:border-\\[\\#bf262e\\]:hover,
    #app main .hover\\:border-\\[\\#bf262e\\]\\/30:hover,
    #app main .hover\\:border-\\[\\#bf262e\\]\\/40:hover,
    #app main .hover\\:border-\\[\\#bf262e\\]\\/50:hover {
      border-color: var(--ds-border-brand) !important;
    }
    #app main .border-white\\/5,
    #app main .border-white\\/10,
    #app main .border-white\\/15,
    #app main .border-white\\/20 {
      border-color: var(--ds-border) !important;
    }

    #app main code {
      background-color: var(--ds-surface-neutral) !important;
      color: var(--ds-text) !important;
      padding: 0.14rem 0.45rem;
      border-radius: 6px;
      font-size: 0.85em;
    }
    .tag-badge {
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 9999px !important;
      font-size: 10.5px !important;
      font-weight: 600;
      letter-spacing: 0.01em;
    }

    /* Accessible Semantic Status Colors */
    #app main .bg-emerald-500\\/10,
    #app main .bg-emerald-500\\/15,
    #app main .bg-emerald-500\\/20,
    #app main .bg-emerald-500\\/25 { background-color: var(--ds-bg-success) !important; }
    #app main .text-emerald-200,
    #app main .text-emerald-300,
    #app main .text-emerald-400 { color: var(--ds-text-success) !important; }
    #app main .border-emerald-500\\/20,
    #app main .border-emerald-500\\/30,
    #app main .border-emerald-500\\/40 { border-color: var(--ds-border-success) !important; }

    #app main .bg-blue-500\\/10,
    #app main .bg-blue-500\\/15,
    #app main .bg-blue-500\\/20,
    #app main .bg-blue-500\\/25,
    #app main .bg-indigo-500\\/15,
    #app main .bg-indigo-500\\/20 { background-color: var(--ds-brand-subtlest) !important; }
    #app main .text-blue-200,
    #app main .text-blue-300,
    #app main .text-blue-400,
    #app main .text-indigo-300,
    #app main .text-indigo-400 { color: var(--ds-text-brand) !important; }
    #app main .border-blue-500\\/20,
    #app main .border-blue-500\\/30,
    #app main .border-blue-500\\/40 { border-color: var(--ds-border-brand) !important; }

    #app main .bg-amber-500\\/10,
    #app main .bg-amber-500\\/15,
    #app main .bg-amber-500\\/20 { background-color: var(--ds-bg-warning) !important; }
    #app main .text-amber-200,
    #app main .text-amber-300,
    #app main .text-amber-400 { color: var(--ds-text-warning) !important; }
    #app main .border-amber-500\\/20,
    #app main .border-amber-500\\/30,
    #app main .border-amber-500\\/40 { border-color: var(--ds-border-warning) !important; }

    #app main .bg-purple-500\\/10,
    #app main .bg-purple-500\\/15,
    #app main .bg-purple-500\\/20 { background-color: var(--ds-bg-discovery) !important; }
    #app main .text-purple-200,
    #app main .text-purple-300,
    #app main .text-purple-400 { color: var(--ds-text-discovery) !important; }
    #app main .border-purple-500\\/20,
    #app main .border-purple-500\\/30,
    #app main .border-purple-500\\/40 { border-color: var(--ds-border-discovery) !important; }

    #app main .bg-red-500\\/10,
    #app main .bg-red-500\\/15,
    #app main .bg-red-500\\/20 { background-color: var(--ds-bg-danger) !important; }
    #app main .text-red-300,
    #app main .text-red-400 { color: var(--ds-text-danger) !important; }
    #app main .border-red-500\\/30,
    #app main .border-red-500\\/40 { border-color: var(--ds-border-danger) !important; }

    /* Modern Tables & Form Inputs */
    #app main table { border-collapse: collapse; width: 100%; }
    #app main thead th {
      background-color: var(--ds-surface-sunken) !important;
      color: var(--ds-text-subtle) !important;
      border-bottom: 2px solid var(--ds-border) !important;
      font-weight: 600;
    }
    #app main tbody td {
      border-bottom: 1px solid var(--ds-border) !important;
    }
    #app main tbody tr:hover {
      background-color: var(--ds-surface-hovered) !important;
    }
    #app main input, #app main select, #app main textarea {
      background-color: var(--ds-surface) !important;
      color: var(--ds-text) !important;
      border-color: var(--ds-border-bold) !important;
    }
    #app main input:focus, #app main select:focus, #app main textarea:focus {
      border-color: var(--ds-brand-bold) !important;
      outline: 2px solid var(--ds-brand-subtlest);
    }

    /* ================= PRINT / PDF EXPORT MODE ================= */
    @media print {
      header, aside, footer, .no-print { display: none !important; }
      body, #app, main, div {
        background: #FFFFFF !important;
        color: #0F172A !important;
        box-shadow: none !important;
      }
    }
  </style>
</head>
<body class="min-h-full flex flex-col custom-scrollbar">
  <div id="app" class="min-h-screen flex flex-col">
    <!-- Top Scroll Progress Line -->
    <div
      class="fixed top-0 left-0 h-0.5 z-50 transition-all duration-150 pointer-events-none"
      style="background: linear-gradient(90deg, #2563EB, #4F46E5, #0EA5E9);"
      :style="{ width: scrollProgress + '%' }"
    ></div>

    <div class="flex-1 flex flex-col min-h-screen">

      <!-- ================= 1. MODERN TOP NAVIGATION HEADER ================= -->
      <header class="sticky top-0 z-40 app-topbar h-14 flex items-center px-4 sm:px-6 justify-between gap-4">
        
        <!-- Left: Brand Identity & Status -->
        <div @click="selectTab('dashboard')" class="flex items-center gap-3 cursor-pointer shrink-0">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-xs shadow-sm btn-primary">
            VM
          </div>
          <div class="flex items-center gap-2.5 whitespace-nowrap">
            <span class="text-sm sm:text-base font-bold tracking-tight" style="color: var(--ds-text)">Visar Murseli</span>
            <span class="hidden sm:inline-flex items-center gap-1.5 status-pill status-pill-green">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>M.Sc. Wirtschaftsinformatik</span>
            </span>
          </div>
        </div>

        <!-- Right: Compact Core Credential Badge, PDF Export, Theme Toggle & Mobile Menu -->
        <div class="flex items-center gap-2 shrink-0">
          <div class="hidden xl:flex items-center gap-1.5 text-[10.5px] font-mono">
            <span class="status-pill status-pill-blue">36M Enterprise Praxis</span>
            <span class="status-pill status-pill-purple">300 ECTS • M.Sc. 1,6</span>
          </div>

          <!-- PDF Export Button -->
          <button 
            @click="printProfile" 
            class="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition hover:opacity-85"
            style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)"
            title="Aktuelle Ansicht als PDF drucken / speichern"
          >
            <span>🖨️</span>
            <span class="hidden lg:inline">PDF Export</span>
          </button>

          <!-- Light / Dark Theme Toggle -->
          <button 
            @click="toggleDarkMode" 
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium transition"
            style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)"
            :title="isDark ? 'Heller Modus aktivieren' : 'Dunkler Modus aktivieren'"
          >
            <span v-if="isDark">☀️</span>
            <span v-else>🌙</span>
            <span class="hidden lg:inline text-[11px]">{{ isDark ? 'Light' : 'Dark' }}</span>
          </button>

          <!-- Mobile Drawer Trigger -->
          <button 
            @click="isMobileMenuOpen = !isMobileMenuOpen" 
            class="lg:hidden flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold btn-primary"
            title="Navigation öffnen"
          >
            <span>☰</span>
            <span class="hidden sm:inline">Menü</span>
          </button>
        </div>
      </header>

      <!-- ================= 2. MOBILE SLIDE-OVER NAVIGATION DRAWER ================= -->
      <div v-if="isMobileMenuOpen" class="fixed inset-0 z-50 flex justify-start lg:hidden">
        <div @click="isMobileMenuOpen = false" class="fixed inset-0 bg-black/50 backdrop-blur-xs"></div>
        <div class="relative w-72 max-w-[85vw] h-full overflow-y-auto p-4 flex flex-col justify-between z-10 app-sidebar custom-scrollbar" style="box-shadow: var(--ds-shadow-overlay)">
          <div class="space-y-4">
            <div class="flex items-center justify-between pb-3 border-b" style="border-color: var(--ds-border)">
              <div class="flex items-center gap-2.5">
                <div class="w-7 h-7 rounded-lg btn-primary flex items-center justify-center font-bold text-white text-xs">VM</div>
                <div>
                  <div class="text-xs font-bold" style="color: var(--ds-text)">Wissensportal</div>
                  <div class="text-[10px]" style="color: var(--ds-text-subtlest)">Kapitel-Navigation</div>
                </div>
              </div>
              <button @click="isMobileMenuOpen = false" class="p-1.5 rounded hover:bg-black/5 text-xs font-mono" style="color: var(--ds-text-subtle)">✕</button>
            </div>

            <div v-for="space in navSpaces" :key="space.id" class="space-y-1">
              <div class="px-2 py-1 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5" style="color: var(--ds-text-subtlest)">
                <span>{{ space.icon }}</span>
                <span>{{ space.label }}</span>
              </div>
              <button
                v-for="item in space.items"
                :key="item.id"
                @click="selectTab(item.id)"
                :class="['nav-item', activeTab === item.id ? 'active' : '']"
              >
                <span class="text-sm shrink-0">{{ item.icon }}</span>
                <div class="min-w-0">
                  <div class="truncate text-xs">{{ item.label }}</div>
                </div>
              </button>
            </div>
          </div>

          <div class="pt-3 mt-4 border-t text-[11px] flex items-center justify-between" style="border-color: var(--ds-border); color: var(--ds-text-subtlest)">
            <span>Visar Murseli, M.Sc.</span>
            <span class="status-pill status-pill-green">Verifiziert</span>
          </div>
        </div>
      </div>

      <!-- ================= 3. MODERN 2-COLUMN WORKSPACE (SIDEBAR + DYNAMIC CANVAS) ================= -->
      <div class="flex-1 flex min-h-0">

        <!-- Left Collapsible Sidebar Rail (Desktop lg+) -->
        <aside
          :class="[
            'hidden lg:flex flex-col shrink-0 self-start app-sidebar transition-all duration-200 select-none sticky top-14 h-[calc(100vh-3.5rem)]',
            isSidebarCollapsed ? 'w-16' : 'w-64'
          ]"
        >
          <!-- Sidebar Header -->
          <div class="p-3.5 border-b flex items-center justify-between gap-2" style="border-color: var(--ds-border)">
            <div v-if="!isSidebarCollapsed" class="flex items-center gap-2.5 min-w-0">
              <div class="w-7 h-7 rounded-lg btn-primary flex items-center justify-center text-white font-bold text-xs shrink-0">
                ⚡
              </div>
              <div class="min-w-0">
                <div class="text-xs font-bold truncate" style="color: var(--ds-text)">Wissensportal</div>
                <div class="text-[10px] truncate" style="color: var(--ds-text-subtlest)">300 ECTS • 36M Praxis</div>
              </div>
            </div>
            <button
              @click="isSidebarCollapsed = !isSidebarCollapsed"
              class="w-7 h-7 rounded-md flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 text-xs font-mono shrink-0"
              style="color: var(--ds-text-subtle)"
              :title="isSidebarCollapsed ? 'Navigation ausklappen' : 'Navigation einklappen'"
            >
              {{ isSidebarCollapsed ? '»' : '«' }}
            </button>
          </div>

          <!-- Grouped Navigation Tree -->
          <div class="flex-1 overflow-y-auto p-2.5 space-y-4 custom-scrollbar">
            <div v-for="space in navSpaces" :key="space.id" class="space-y-0.5">
              <div
                v-if="!isSidebarCollapsed"
                class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider"
                style="color: var(--ds-text-subtlest)"
              >
                {{ space.label }}
              </div>
              <button
                v-for="item in space.items"
                :key="item.id"
                @click="selectTab(item.id)"
                :class="['nav-item', activeTab === item.id ? 'active' : '', isSidebarCollapsed ? 'justify-center px-0' : '']"
                :title="item.label"
              >
                <span class="text-sm shrink-0">{{ item.icon }}</span>
                <div v-if="!isSidebarCollapsed" class="min-w-0 flex-1">
                  <div class="truncate text-[12.5px]">{{ item.label }}</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Sidebar Footer -->
          <div v-if="!isSidebarCollapsed" class="p-3 border-t text-[11px] flex items-center justify-between" style="border-color: var(--ds-border); color: var(--ds-text-subtlest)">
            <span>M.Sc. 1,6 • B.Sc. 3,0</span>
            <span class="status-pill status-pill-green">Online</span>
          </div>
        </aside>

        <!-- Right Scrollable Canvas -->
        <div class="flex-1 flex flex-col min-w-0 app-canvas">
          
          <!-- Mobile / Tablet Quick Horizontal Pill Bar (< lg) -->
          <div class="lg:hidden border-b px-3 py-2 flex items-center gap-1.5 overflow-x-auto no-scrollbar" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="selectTab(tab.id)"
              :class="[
                'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[11px] font-medium whitespace-nowrap shrink-0 border transition',
                activeTab === tab.id ? 'btn-primary' : ''
              ]"
              :style="activeTab === tab.id ? '' : 'background: var(--ds-surface-raised); border-color: var(--ds-border); color: var(--ds-text-subtle);'"
            >
              <span>{{ tab.icon }}</span>
              <span>{{ tab.label }}</span>
            </button>
          </div>

          <!-- Centered Reading Canvas -->
          <main class="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-8 py-6 space-y-6">

            <!-- Dynamic Breadcrumbs & Chapter Counter -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b text-xs" style="border-color: var(--ds-border)">
              <div class="flex items-center gap-1.5 flex-wrap" style="color: var(--ds-text-subtlest)">
                <span @click="selectTab('dashboard')" class="cursor-pointer hover:underline font-medium">Übersicht</span>
                <span>›</span>
                <span class="font-medium">{{ currentHubName }}</span>
                <span>›</span>
                <span class="font-semibold" style="color: var(--ds-text)">{{ currentTabName }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="status-pill status-pill-blue">Kapitel {{ currentTabIndex + 1 }} / {{ tabs.length }}</span>
                <span class="status-pill status-pill-green">Verifiziert 2026</span>
                <button
                  @click="isMobileMenuOpen = true"
                  class="lg:hidden px-2.5 py-1 rounded-lg border text-[11px] font-medium"
                  style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                >
                  ☰ Kapitel
                </button>
              </div>
            </div>
"""
    if public_mode:
        tpl = tpl.replace('%%CAREER_SUB%%', 'Zielrollen & 90-Tage Onboarding-Roadmap')
    else:
        tpl = tpl.replace('%%CAREER_SUB%%', 'Zielrollen, 55k–75k € Gehaltsziel & Onboarding')
    return tpl
