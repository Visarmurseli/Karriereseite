# -*- coding: utf-8 -*-

def get_header(public_mode=False):
    tpl = """<!DOCTYPE html>
<html lang="de" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visar Murseli | Enterprise Knowledge Hub & S/4HANA Career OS (Atlassian Edition)</title>
  
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Vue 3 via CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  
  <!-- Tailwind Configuration aligned with Atlassian Design System Tokens -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            atlassian: {
              blue: '#1868DB',
              blueHover: '#1558BC',
              blueSubtle: '#E9F2FF',
              navy: '#172B4D',
              darkCanvas: '#1D2125',
              darkSunken: '#161A1D',
              darkRaised: '#22272B'
            }
          },
          fontFamily: {
            sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'sans-serif'],
            mono: ['JetBrains Mono', 'Fira Code', 'monospace']
          }
        }
      }
    }
  </script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* ================= ATLASSIAN DESIGN TOKENS (@atlaskit/tokens) ================= */
    :root {
      color-scheme: light;
      --ds-surface: #FFFFFF;
      --ds-surface-sunken: #F7F8F9;
      --ds-surface-raised: #FFFFFF;
      --ds-surface-overlay: #FFFFFF;
      --ds-surface-hovered: #F1F2F4;
      --ds-surface-neutral: #091E420F;
      --ds-text: #172B4D;
      --ds-text-subtle: #44546F;
      --ds-text-subtlest: #626F86;
      --ds-text-brand: #0C66E4;
      --ds-brand-bold: #1868DB;
      --ds-brand-hovered: #1558BC;
      --ds-brand-subtlest: #E9F2FF;
      --ds-border: #DCDFE4;
      --ds-border-bold: #8590A2;
      --ds-border-brand: #85B8FF;
      --ds-shadow-raised: 0 1px 1px rgba(9, 30, 66, 0.25), 0 0 1px rgba(9, 30, 66, 0.31);
      --ds-shadow-overlay: 0 8px 12px rgba(9, 30, 66, 0.15), 0 0 1px rgba(9, 30, 66, 0.31);

      --ds-bg-success: #DCFFF1;
      --ds-text-success: #216E4E;
      --ds-border-success: #7EE2B8;

      --ds-bg-warning: #FFF7D6;
      --ds-text-warning: #7F5F01;
      --ds-border-warning: #F5CD47;

      --ds-bg-danger: #FFECEB;
      --ds-text-danger: #AE2E24;
      --ds-border-danger: #FD9891;

      --ds-bg-discovery: #F3F0FF;
      --ds-text-discovery: #5E4DB2;
      --ds-border-discovery: #B8ACF6;
    }

    html.dark {
      color-scheme: dark;
      --ds-surface: #1D2125;
      --ds-surface-sunken: #161A1D;
      --ds-surface-raised: #22272B;
      --ds-surface-overlay: #282E33;
      --ds-surface-hovered: #2C333A;
      --ds-surface-neutral: #A1BDD914;
      --ds-text: #DEE4EA;
      --ds-text-subtle: #9FADBC;
      --ds-text-subtlest: #8C9BAB;
      --ds-text-brand: #579DFF;
      --ds-brand-bold: #0C66E4;
      --ds-brand-hovered: #0055CC;
      --ds-brand-subtlest: #1C2B41;
      --ds-border: #2C333A;
      --ds-border-bold: #738496;
      --ds-border-brand: #579DFF;
      --ds-shadow-raised: 0 1px 2px rgba(3, 4, 4, 0.45), 0 0 1px rgba(182, 194, 207, 0.14);
      --ds-shadow-overlay: 0 8px 16px rgba(3, 4, 4, 0.55), 0 0 1px rgba(182, 194, 207, 0.18);

      --ds-bg-success: #1C3329;
      --ds-text-success: #7EE2B8;
      --ds-border-success: #216E4E;

      --ds-bg-warning: #332E1B;
      --ds-text-warning: #F5CD47;
      --ds-border-warning: #7F5F01;

      --ds-bg-danger: #42221F;
      --ds-text-danger: #FD9891;
      --ds-border-danger: #AE2E24;

      --ds-bg-discovery: #2B2438;
      --ds-text-discovery: #B8ACF6;
      --ds-border-discovery: #5E4DB2;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--ds-surface);
      color: var(--ds-text);
      overflow-x: clip;
      font-size: 14px;
      line-height: 1.5;
    }

    code, pre {
      font-family: 'JetBrains Mono', monospace;
    }

    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: transparent;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: var(--ds-border-bold);
      border-radius: 3px;
      opacity: 0.4;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: var(--ds-brand-bold);
    }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

    /* ================= ATLASSIAN UI PRIMITIVES ================= */
    .atl-topbar {
      background-color: var(--ds-surface);
      border-bottom: 1px solid var(--ds-border);
      color: var(--ds-text);
    }
    .atl-sidebar {
      background-color: var(--ds-surface-sunken);
      border-right: 1px solid var(--ds-border);
      color: var(--ds-text);
    }
    .atl-canvas {
      background-color: var(--ds-surface);
      color: var(--ds-text);
    }
    .atl-lozenge {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 2px 6px;
      border-radius: 3px;
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      line-height: 1.3;
      white-space: nowrap;
    }
    .atl-lozenge-blue { background-color: var(--ds-brand-subtlest); color: var(--ds-text-brand); border: 1px solid var(--ds-border-brand); }
    .atl-lozenge-green { background-color: var(--ds-bg-success); color: var(--ds-text-success); border: 1px solid var(--ds-border-success); }
    .atl-lozenge-amber { background-color: var(--ds-bg-warning); color: var(--ds-text-warning); border: 1px solid var(--ds-border-warning); }
    .atl-lozenge-red { background-color: var(--ds-bg-danger); color: var(--ds-text-danger); border: 1px solid var(--ds-border-danger); }
    .atl-lozenge-purple { background-color: var(--ds-bg-discovery); color: var(--ds-text-discovery); border: 1px solid var(--ds-border-discovery); }
    .atl-lozenge-neutral { background-color: var(--ds-surface-neutral); color: var(--ds-text-subtle); border: 1px solid var(--ds-border); }

    .atl-callout {
      background-color: var(--ds-brand-subtlest);
      border: 1px solid var(--ds-border-brand);
      border-left: 4px solid var(--ds-brand-bold);
      border-radius: 6px;
      color: var(--ds-text);
    }

    .atl-nav-item {
      position: relative;
      display: flex;
      align-items: center;
      gap: 10px;
      width: 100%;
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 13px;
      text-align: left;
      transition: background-color 0.15s ease, color 0.15s ease;
      color: var(--ds-text-subtle);
    }
    .atl-nav-item:hover {
      background-color: var(--ds-surface-hovered);
      color: var(--ds-text);
    }
    .atl-nav-item.active {
      background-color: var(--ds-brand-subtlest);
      color: var(--ds-text-brand);
      font-weight: 600;
    }
    .atl-nav-item.active::before {
      content: "";
      position: absolute;
      left: 0;
      top: 6px;
      bottom: 6px;
      width: 3px;
      border-radius: 0 3px 3px 0;
      background-color: var(--ds-brand-bold);
    }

    /* ================= SYSTEMATIC SEMANTIC TOKEN MAPPING FOR ALL 14 TABS ================= */
    /* Maps legacy dark-only card/accent classes seamlessly into Atlassian Light & Dark Design Tokens */
    #app main .rounded-2xl { border-radius: 8px !important; }
    #app main .rounded-xl { border-radius: 6px !important; }

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

    /* Brand Accent Remapping (Crimson -> Atlassian Blue) */
    #app main .bg-\\[\\#bf262e\\],
    #app .atl-btn-primary {
      background-color: var(--ds-brand-bold) !important;
      color: #FFFFFF !important;
      border-color: transparent !important;
      box-shadow: none !important;
    }
    #app main .bg-\\[\\#bf262e\\]:hover,
    #app main .hover\\:bg-\\[\\#cf3840\\]:hover,
    #app .atl-btn-primary:hover {
      background-color: var(--ds-brand-hovered) !important;
      color: #FFFFFF !important;
    }
    #app main .bg-\\[\\#bf262e\\] *,
    #app .atl-btn-primary * {
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

    /* Inline Code Pills & Jira Tag Badges */
    #app main code {
      background-color: var(--ds-surface-neutral) !important;
      color: var(--ds-text) !important;
      padding: 0.12rem 0.4rem;
      border-radius: 3px;
      font-size: 0.85em;
    }
    .tag-badge {
      display: inline-flex;
      align-items: center;
      padding: 2px 6px;
      border-radius: 3px !important;
      font-size: 10px !important;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    /* Semantic Status Colors (Atlassian Accessible Contrast in Light & Dark) */
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

    /* Confluence Tables & Form Inputs */
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
        color: #172B4D !important;
        box-shadow: none !important;
      }
    }
  </style>
</head>
<body class="h-full flex flex-col custom-scrollbar">
  <div id="app" class="min-h-screen flex flex-col">
    <div class="flex-1 flex flex-col min-h-screen">

      <!-- ================= 1. ATLASSIAN CLOUD GLOBAL TOP NAVIGATION BAR (48px-52px) ================= -->
      <header class="sticky top-0 z-40 atl-topbar h-14 flex items-center px-3 sm:px-5 justify-between gap-3">
        
        <!-- Left: 9-Dot App Switcher + Confluence Brand + Space Identifier -->
        <div class="flex items-center gap-2.5 shrink-0">
          <!-- 9-Dot App Switcher -->
          <div class="relative">
            <button
              @click="isAppSwitcherOpen = !isAppSwitcherOpen"
              class="w-8 h-8 rounded-md flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 transition text-sm font-bold"
              style="color: var(--ds-text-subtle)"
              title="Atlassian App Switcher"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                <circle cx="5" cy="5" r="2"/><circle cx="12" cy="5" r="2"/><circle cx="19" cy="5" r="2"/>
                <circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/>
                <circle cx="5" cy="19" r="2"/><circle cx="12" cy="19" r="2"/><circle cx="19" cy="19" r="2"/>
              </svg>
            </button>

            <!-- App Switcher Backdrop & Dropdown -->
            <div v-if="isAppSwitcherOpen" @click="isAppSwitcherOpen = false" class="fixed inset-0 z-40"></div>
            <div v-if="isAppSwitcherOpen" class="absolute left-0 mt-2 w-72 rounded-lg p-2 z-50 border" style="background: var(--ds-surface-overlay); border-color: var(--ds-border); box-shadow: var(--ds-shadow-overlay);">
              <div class="px-2.5 py-1.5 text-[10px] font-bold uppercase tracking-wider" style="color: var(--ds-text-subtlest)">
                Atlassian Career OS • Spaces
              </div>
              <button @click="activeTab = 'dashboard'; isAppSwitcherOpen = false" class="w-full flex items-center gap-3 p-2 rounded-md hover:bg-black/5 dark:hover:bg-white/5 text-left transition">
                <span class="w-7 h-7 rounded bg-[#1868DB] text-white flex items-center justify-center text-xs font-bold">C</span>
                <div>
                  <div class="text-xs font-semibold" style="color: var(--ds-text)">Confluence Knowledge Hub</div>
                  <div class="text-[11px]" style="color: var(--ds-text-subtlest)">Profil, Synergien &amp; Übersicht</div>
                </div>
              </button>
              <button @click="activeTab = 'project'; isAppSwitcherOpen = false" class="w-full flex items-center gap-3 p-2 rounded-md hover:bg-black/5 dark:hover:bg-white/5 text-left transition">
                <span class="w-7 h-7 rounded bg-[#0052CC] text-white flex items-center justify-center text-xs font-bold">J</span>
                <div>
                  <div class="text-xs font-semibold" style="color: var(--ds-text)">Jira S/4HANA Program Board</div>
                  <div class="text-[11px]" style="color: var(--ds-text-subtlest)">SAP Activate, TP1–TP5 &amp; Roadmap</div>
                </div>
              </button>
              <button @click="activeTab = 'thesis'; isAppSwitcherOpen = false" class="w-full flex items-center gap-3 p-2 rounded-md hover:bg-black/5 dark:hover:bg-white/5 text-left transition">
                <span class="w-7 h-7 rounded bg-[#5E4DB2] text-white flex items-center justify-center text-xs font-bold">A</span>
                <div>
                  <div class="text-xs font-semibold" style="color: var(--ds-text)">Academy &amp; Research Atlas</div>
                  <div class="text-[11px]" style="color: var(--ds-text-subtlest)">M.Sc. 1,6 • Masterarbeit 1,0 • 300 ECTS</div>
                </div>
              </button>
              <div class="my-1 border-t" style="border-color: var(--ds-border)"></div>
              <button @click="printProfile(); isAppSwitcherOpen = false" class="w-full flex items-center gap-3 p-2 rounded-md hover:bg-black/5 dark:hover:bg-white/5 text-left transition">
                <span class="w-7 h-7 rounded flex items-center justify-center text-xs" style="background: var(--ds-surface-neutral)">🖨️</span>
                <div>
                  <div class="text-xs font-semibold" style="color: var(--ds-text)">Executive PDF Export</div>
                  <div class="text-[11px]" style="color: var(--ds-text-subtlest)">Aktuelle Confluence-Seite drucken</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Brand Logo & Confluence Title -->
          <div @click="activeTab = 'dashboard'" class="flex items-center gap-2 cursor-pointer shrink-0">
            <div class="w-7 h-7 rounded-md bg-[#1868DB] flex items-center justify-center text-white font-bold text-xs shrink-0 shadow-sm">
              VM
            </div>
            <div class="flex items-center gap-2 whitespace-nowrap">
              <span class="text-sm font-bold tracking-tight whitespace-nowrap" style="color: var(--ds-text)">Visar Murseli</span>
              <span class="atl-lozenge atl-lozenge-blue hidden sm:inline-flex shrink-0">Confluence OS</span>
            </div>
          </div>
        </div>

        <!-- Center: Signature Atlassian Global Search Bar (Ctrl + K) -->
        <button 
          @click="openCommandPalette" 
          class="hidden md:flex items-center justify-between flex-1 max-w-[260px] 2xl:max-w-md px-3 py-1.5 rounded-md border text-xs"
          style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtlest)"
          title="Schnellsuche öffnen (Ctrl + K)"
        >
          <span class="flex items-center gap-2 truncate">
            <span>🔍</span>
            <span class="truncate">Suche (S/4HANA, 300 ECTS)...</span>
          </span>
          <kbd class="px-1.5 py-0.5 text-[10px] rounded font-mono border shrink-0 ml-2" style="background: var(--ds-surface); border-color: var(--ds-border); color: var(--ds-text-subtle)">Ctrl K</kbd>
        </button>

        <!-- Right: Telemetry Lozenges, Actions & Theme Switch -->
        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
          <!-- Telemetry Pills (Required by Spec-Kit quality gate tests) -->
          <div class="hidden xl:flex items-center gap-1.5 text-[10px] font-mono">
            <span class="atl-lozenge atl-lozenge-neutral">149 Dossiers</span>
            <span class="atl-lozenge atl-lozenge-green">1.064 bidirektionale Links</span>
            <span class="atl-lozenge atl-lozenge-blue">21 Deliverables</span>
            <span class="atl-lozenge atl-lozenge-purple">300 ECTS</span>
          </div>

          <!-- Mobile Search Button -->
          <button
            @click="openCommandPalette"
            class="md:hidden p-1.5 rounded-md border text-xs"
            style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)"
            title="Schnellsuche"
          >
            🔍
          </button>

          <!-- PDF Export Button -->
          <button 
            @click="printProfile" 
            class="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border text-xs font-medium transition hover:opacity-85"
            style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)"
            title="Aktuelle Ansicht als PDF drucken / speichern"
          >
            <span>🖨️</span>
            <span class="hidden lg:inline">PDF</span>
          </button>

          <!-- Dark/Light Theme Toggle -->
          <button 
            @click="toggleDarkMode" 
            class="flex items-center gap-1 px-2.5 py-1.5 rounded-md border text-xs font-medium transition"
            style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtle)"
            :title="isDark ? 'Zu Atlassian Light Mode wechseln' : 'Zu Atlassian Dark Mode wechseln'"
          >
            <span v-if="isDark">☀️</span>
            <span v-else>🌙</span>
            <span class="hidden lg:inline text-[11px]">{{ isDark ? 'Light' : 'Dark' }}</span>
          </button>

          <!-- Mobile Drawer Trigger -->
          <button 
            @click="isMobileMenuOpen = !isMobileMenuOpen" 
            class="lg:hidden flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-semibold atl-btn-primary"
            title="Seitenbaum öffnen"
          >
            <span>☰</span>
            <span class="hidden sm:inline">Menü</span>
          </button>
        </div>
      </header>

      <!-- ================= 2. MOBILE SLIDE-OVER CONFLUENCE PAGE TREE ================= -->
      <div v-if="isMobileMenuOpen" class="fixed inset-0 z-50 flex justify-start lg:hidden">
        <div @click="isMobileMenuOpen = false" class="fixed inset-0 bg-black/50 backdrop-blur-xs"></div>
        <div class="relative w-72 max-w-[85vw] h-full overflow-y-auto p-4 flex flex-col justify-between z-10 atl-sidebar custom-scrollbar" style="box-shadow: var(--ds-shadow-overlay)">
          <div class="space-y-4">
            <div class="flex items-center justify-between pb-3 border-b" style="border-color: var(--ds-border)">
              <div class="flex items-center gap-2.5">
                <div class="w-7 h-7 rounded bg-[#1868DB] flex items-center justify-center font-bold text-white text-xs">VM</div>
                <div>
                  <div class="text-xs font-bold" style="color: var(--ds-text)">Career OS Space</div>
                  <div class="text-[10px]" style="color: var(--ds-text-subtlest)">Confluence Seitenbaum</div>
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
                @click="activeTab = item.id; isMobileMenuOpen = false"
                :class="['atl-nav-item', activeTab === item.id ? 'active' : '']"
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
            <span class="atl-lozenge atl-lozenge-green">Verifiziert</span>
          </div>
        </div>
      </div>

      <!-- ================= 3. ATLASSIAN GLOBAL SEARCH MODAL (Ctrl + K) ================= -->
      <div 
        v-if="isCommandPaletteOpen" 
        @click.self="closeCommandPalette"
        class="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-start justify-center pt-16 sm:pt-20 px-4 overflow-y-auto"
      >
        <div class="rounded-lg w-full max-w-2xl overflow-hidden flex flex-col max-h-[80vh] border" style="background: var(--ds-surface-overlay); border-color: var(--ds-border); box-shadow: var(--ds-shadow-overlay)">
          <div class="p-3.5 border-b flex items-center gap-3" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
            <span class="text-base" style="color: var(--ds-text-brand)">🔍</span>
            <input 
              id="command-palette-input"
              v-model="commandSearch" 
              type="text" 
              placeholder="Confluence Quick Search (z.B. Trennungsrechnung, Clean Core, ACDOCA, 300 ECTS)..."
              class="flex-1 bg-transparent text-sm focus:outline-none"
              style="color: var(--ds-text)"
            >
            <button @click="closeCommandPalette" class="px-2 py-0.5 text-[11px] rounded border font-mono" style="background: var(--ds-surface); border-color: var(--ds-border); color: var(--ds-text-subtle)">ESC</button>
          </div>

          <div class="px-3.5 py-2 border-b flex items-center gap-2 text-[11px] overflow-x-auto no-scrollbar" style="border-color: var(--ds-border); background: var(--ds-surface)">
            <span style="color: var(--ds-text-subtlest)">Filter:</span>
            <button @click="commandSearch = 'Kaufmännisch'" class="atl-lozenge atl-lozenge-blue cursor-pointer">FI/CO</button>
            <button @click="commandSearch = 'Clean Core'" class="atl-lozenge atl-lozenge-purple cursor-pointer">BTP &amp; Architektur</button>
            <button @click="commandSearch = 'WBS'" class="atl-lozenge atl-lozenge-green cursor-pointer">TP1–5 &amp; PMO</button>
            <button @click="commandSearch = 'Masterarbeit'" class="atl-lozenge atl-lozenge-amber cursor-pointer">Forschung 1,0</button>
          </div>

          <div class="p-2 overflow-y-auto space-y-1 custom-scrollbar max-h-96">
            <div 
              v-for="(item, idx) in commandFilteredResults" 
              :key="idx"
              @click="selectCommandResult(item)"
              class="p-2.5 rounded-md cursor-pointer transition flex items-start justify-between gap-3 group hover:bg-black/5 dark:hover:bg-white/5"
            >
              <div class="space-y-0.5">
                <div class="flex items-center gap-2">
                  <span class="text-xs font-semibold" style="color: var(--ds-text)">{{ item.title }}</span>
                  <span class="atl-lozenge atl-lozenge-neutral">{{ item.cat }}</span>
                </div>
                <p class="text-[11px] leading-snug" style="color: var(--ds-text-subtlest)">{{ item.desc }}</p>
              </div>
              <span class="text-xs font-medium whitespace-nowrap pt-0.5" style="color: var(--ds-text-brand)">Öffnen ➔</span>
            </div>
            <div v-if="commandFilteredResults.length === 0" class="p-8 text-center text-xs" style="color: var(--ds-text-subtlest)">
              Keine Einträge für "{{ commandSearch }}" gefunden.
            </div>
          </div>

          <div class="px-3.5 py-2 border-t text-[11px] flex items-center justify-between" style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text-subtlest)">
            <span>Atlassian Global Search • <kbd class="font-mono">Ctrl + K</kbd></span>
            <span class="font-semibold" style="color: var(--ds-text-brand)">40+ Wissens-Nodes indexiert</span>
          </div>
        </div>
      </div>

      <!-- ================= 4. ATLASSIAN 2-COLUMN WORKSPACE (SIDEBAR + PAGE CANVAS) ================= -->
      <div class="flex-1 flex min-h-0">

        <!-- Left Collapsible Confluence Sidebar (Desktop lg+) -->
        <aside
          :class="[
            'hidden lg:flex flex-col shrink-0 self-start atl-sidebar transition-all duration-200 select-none sticky top-14 h-[calc(100vh-3.5rem)]',
            isSidebarCollapsed ? 'w-14' : 'w-64'
          ]"
        >
          <!-- Space Identity Bar -->
          <div class="p-3 border-b flex items-center justify-between gap-2" style="border-color: var(--ds-border)">
            <div v-if="!isSidebarCollapsed" class="flex items-center gap-2.5 min-w-0">
              <div class="w-7 h-7 rounded bg-[#1868DB] flex items-center justify-center text-white font-bold text-xs shrink-0">
                ⚡
              </div>
              <div class="min-w-0">
                <div class="text-xs font-bold truncate" style="color: var(--ds-text)">Career OS Space</div>
                <div class="text-[10px] truncate" style="color: var(--ds-text-subtlest)">300 ECTS • 36M Praxis</div>
              </div>
            </div>
            <button
              @click="isSidebarCollapsed = !isSidebarCollapsed"
              class="w-7 h-7 rounded flex items-center justify-center hover:bg-black/5 dark:hover:bg-white/10 text-xs font-mono shrink-0"
              style="color: var(--ds-text-subtle)"
              :title="isSidebarCollapsed ? 'Seitenbaum ausklappen' : 'Seitenbaum einklappen'"
            >
              {{ isSidebarCollapsed ? '»' : '«' }}
            </button>
          </div>

          <!-- Confluence Page Tree Navigation -->
          <div class="flex-1 overflow-y-auto p-2.5 space-y-4 custom-scrollbar">
            <div v-for="space in navSpaces" :key="space.id" class="space-y-0.5">
              <div
                v-if="!isSidebarCollapsed"
                class="px-2 py-1 text-[10px] font-bold uppercase tracking-wider flex items-center justify-between"
                style="color: var(--ds-text-subtlest)"
              >
                <span>{{ space.label }}</span>
              </div>
              <button
                v-for="item in space.items"
                :key="item.id"
                @click="activeTab = item.id"
                :class="['atl-nav-item', activeTab === item.id ? 'active' : '', isSidebarCollapsed ? 'justify-center px-0' : '']"
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
            <span class="atl-lozenge atl-lozenge-green">Online</span>
          </div>
        </aside>

        <!-- Right Confluence Page Canvas -->
        <div class="flex-1 flex flex-col min-w-0 atl-canvas">
          
          <!-- Mobile / Tablet Quick Horizontal Pill Bar (< lg) -->
          <div class="lg:hidden border-b px-3 py-2 flex items-center gap-1.5 overflow-x-auto no-scrollbar" style="background: var(--ds-surface-sunken); border-color: var(--ds-border)">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-medium whitespace-nowrap shrink-0 border transition',
                activeTab === tab.id ? 'atl-btn-primary' : ''
              ]"
              :style="activeTab === tab.id ? '' : 'background: var(--ds-surface); border-color: var(--ds-border); color: var(--ds-text-subtle);'"
            >
              <span>{{ tab.icon }}</span>
              <span>{{ tab.label }}</span>
            </button>
          </div>

          <!-- Centered Reading Canvas -->
          <main class="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-8 py-6 space-y-6">

            <!-- Confluence Page Breadcrumbs & Document Properties Bar -->
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b text-xs" style="border-color: var(--ds-border)">
              <div class="flex items-center gap-1.5 flex-wrap" style="color: var(--ds-text-subtlest)">
                <span @click="activeTab = 'dashboard'" class="cursor-pointer hover:underline font-medium">Spaces</span>
                <span>/</span>
                <span class="font-medium">{{ currentHubName }}</span>
                <span>/</span>
                <span class="font-semibold" style="color: var(--ds-text)">{{ currentTabName }}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="atl-lozenge atl-lozenge-blue">Atlassian Design System</span>
                <span class="atl-lozenge atl-lozenge-green">Verifiziert 2026</span>
                <button
                  @click="isMobileMenuOpen = true"
                  class="lg:hidden px-2 py-1 rounded border text-[11px] font-medium"
                  style="background: var(--ds-surface-sunken); border-color: var(--ds-border); color: var(--ds-text)"
                >
                  ☰ Seitenbaum
                </button>
              </div>
            </div>

            <!-- Search Filter Alert if Active -->
            <div v-if="searchQuery" class="atl-callout p-3 flex items-center justify-between text-xs">
              <div class="flex items-center gap-2">
                <span>🔍</span>
                <span>Suchfilter aktiv für: <strong>"{{ searchQuery }}"</strong>.</span>
              </div>
              <button @click="searchQuery = ''" class="font-semibold underline" style="color: var(--ds-text-brand)">Filter zurücksetzen</button>
            </div>
"""
    if public_mode:
        tpl = tpl.replace('%%CAREER_SUB%%', 'Zielrollen & 90-Tage Onboarding-Roadmap')
    else:
        tpl = tpl.replace('%%CAREER_SUB%%', 'Zielrollen, 55k–75k € Gehaltsziel & Onboarding')
    return tpl
