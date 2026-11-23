# -*- coding: utf-8 -*-

def get_header():
    return """<!DOCTYPE html>
<html lang="de" class="h-full dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visar Murseli | Enterprise Knowledge Hub & S/4HANA Career OS</title>
  
  <!-- Tailwind CSS via CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Vue 3 via CDN -->
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  
  <!-- Tailwind Configuration matching Portfolioseite (Hue 358 - Crimson Red) -->
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            crimson: {
              50: '#fff1f2',
              100: '#ffe4e6',
              200: '#fecdd3',
              300: '#fda4af',
              400: '#fb7185',
              500: '#bf262e', // Portfolioseite --first-color: hsla(358, 66%, 45%, 0.9)
              600: '#a31b22',
              700: '#7e1218',
              800: '#5c0c11',
              900: '#3d060a',
              accent: '#cf3840' // Portfolioseite --first-color-alt
            },
            obsidian: {
              body: '#0d0d0d', // Portfolioseite --body-color
              card: '#141414', // Portfolioseite --card-color
              surface: '#181818',
              container: '#1f1a1a',
              border: 'rgba(255, 255, 255, 0.08)',
              hover: 'rgba(191, 38, 46, 0.35)'
            }
          },
          fontFamily: {
            sans: ['Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'sans-serif'],
            mono: ['JetBrains Mono', 'Fira Code', 'monospace']
          }
        }
      }
    }
  </script>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    :root {
      --hue-color: 358;
      --first-color: #bf262e;
      --first-color-alt: #cf3840;
      --first-color-lighter: #fecdd3;
      --body-color: #0d0d0d;
      --card-color: #141414;
      --card-background: rgba(20, 20, 20, 0.88);
      --title-color: #f5f3f3;
      --text-color: #c4bebe;
      --border-color: rgba(255, 255, 255, 0.08);
      --body-font: 'Poppins', sans-serif;
    }

    body {
      font-family: var(--body-font);
      background-color: var(--body-color);
      color: var(--text-color);
      overflow-x: hidden;
    }

    code, pre {
      font-family: 'JetBrains Mono', monospace;
    }

    .custom-scrollbar::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
      background: #0d0d0d;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
      background: #2a2223;
      border-radius: 3px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
      background: #bf262e;
    }

    .glass-card {
      background: rgba(20, 20, 20, 0.88);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-card:hover {
      border-color: rgba(191, 38, 46, 0.45);
      box-shadow: 0 8px 24px -4px rgba(191, 38, 46, 0.25);
    }

    .crimson-glow {
      box-shadow: 0 4px 20px -2px rgba(191, 38, 46, 0.35);
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
<body class="h-full bg-[#0d0d0d] text-[#c4bebe] flex flex-col custom-scrollbar transition-colors duration-200">
  <div id="app" class="min-h-screen flex flex-col bg-[#0d0d0d] text-[#c4bebe]">
    <div class="flex-1 flex flex-col min-h-screen">
      
      <!-- ================= 1. RESPONSIVE TOP APP BAR ================= -->
      <header class="sticky top-0 z-40 bg-[#121212]/95 backdrop-blur-xl border-b border-white/10 shadow-xl">
        <!-- Top Brand & Telemetry Line -->
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between gap-4">
          
          <!-- Brand & Profile Identity -->
          <div class="flex items-center space-x-3.5 cursor-pointer" @click="activeTab = 'dashboard'">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#bf262e] via-[#cf3840] to-[#7e1218] flex items-center justify-center font-extrabold text-white shadow-lg shadow-[#bf262e]/30 border border-white/20 text-sm">
              VM
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <h1 class="text-sm sm:text-base font-bold text-white tracking-tight">Visar Murseli</h1>
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" title="System Online & Bereit"></span>
                <span class="hidden sm:inline-flex px-2 py-0.5 rounded-full bg-[#bf262e]/20 text-[#f87171] border border-[#bf262e]/40 text-[10px] font-bold">🎯 Junior Einstieg & Traineeprogramm</span>
              </div>
              <div class="flex items-center space-x-2 text-[11px] text-[#c4bebe]">
                <span>M.Sc. Note 1,6 (120 ECTS)</span>
                <span class="text-white/40">•</span>
                <span class="text-emerald-400 font-medium">Masterarbeit 1,0</span>
                <span class="text-white/40">•</span>
                <span class="text-[#8f8888]">24M SSB S/4HANA PMO</span>
              </div>
            </div>
          </div>

          <!-- Telemetry Badges & Action Controls -->
          <div class="flex items-center space-x-2 sm:space-x-3">
            
            <!-- Quality Gate Telemetry Pills (Required by Spec-Kit tests) -->
            <div class="hidden xl:flex items-center space-x-2 text-[10px] font-mono">
              <span class="px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-white">53 Dossiers</span>
              <span class="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">266 bidirektionale Links</span>
              <span class="px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">21 Deliverables</span>
              <span class="px-2 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">300 ECTS</span>
            </div>

            <!-- Command Palette Trigger Button -->
            <button 
              @click="openCommandPalette" 
              class="flex items-center space-x-2 px-3 py-1.5 text-xs bg-black/40 hover:bg-[#bf262e]/10 border border-white/10 hover:border-[#bf262e]/50 rounded-xl text-[#c4bebe] hover:text-white transition group shadow-inner"
              title="Schnellsuche öffnen (Ctrl + K)"
            >
              <span class="text-[#bf262e] group-hover:scale-110 transition">⚡</span>
              <span class="hidden sm:inline font-medium">Schnellsuche</span>
              <kbd class="px-1.5 py-0.5 text-[10px] bg-white/10 border border-white/10 rounded font-mono text-[#8f8888] group-hover:text-white">Ctrl K</kbd>
            </button>

            <!-- Dark/Light Mode Toggle -->
            <button 
              @click="toggleDarkMode" 
              class="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-[#c4bebe] hover:text-white border border-white/10 transition"
              :title="isDark ? 'Heller Modus' : 'Dunkler Modus'"
            >
              <span v-if="isDark">☀️</span>
              <span v-else>🌙</span>
            </button>

            <!-- Mobile Drawer Hamburger Toggle -->
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen" 
              class="lg:hidden p-2 rounded-xl bg-white/5 hover:bg-white/10 text-white border border-white/10"
              title="Menü öffnen"
            >
              <span v-if="!isMobileMenuOpen">☰</span>
              <span v-else>✕</span>
            </button>
          </div>
        </div>

        <!-- Segmented Navigation: 5 Core Hubs -->
        <div class="border-t border-white/10 bg-black/40">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between overflow-x-auto custom-scrollbar py-2">
            <div class="flex items-center space-x-1.5 sm:space-x-2">
              
              <!-- Hub 1: Profil & Einstieg -->
              <button 
                @click="activeTab = 'dashboard'"
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center space-x-2 whitespace-nowrap',
                  activeTab === 'dashboard'
                    ? 'bg-[#bf262e] text-white shadow-md shadow-[#bf262e]/30'
                    : 'text-[#c4bebe] hover:text-white hover:bg-white/5'
                ]"
              >
                <span>📊</span>
                <span>Profil & Einstieg</span>
              </button>

              <!-- Hub 2: S/4HANA Transformation -->
              <button 
                @click="activeTab = 'project'"
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center space-x-2 whitespace-nowrap',
                  ['project', 'solution_design', 'migration', 'tools'].includes(activeTab)
                    ? 'bg-[#bf262e] text-white shadow-md shadow-[#bf262e]/30'
                    : 'text-[#c4bebe] hover:text-white hover:bg-white/5'
                ]"
              >
                <span>🚆</span>
                <span>S/4HANA Transformation</span>
              </button>

              <!-- Hub 3: Akademische Exzellenz -->
              <button 
                @click="activeTab = 'thesis'"
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center space-x-2 whitespace-nowrap',
                  ['thesis', 'enterprise_arch'].includes(activeTab)
                    ? 'bg-[#bf262e] text-white shadow-md shadow-[#bf262e]/30'
                    : 'text-[#c4bebe] hover:text-white hover:bg-white/5'
                ]"
              >
                <span>🎓</span>
                <span>Akademische Exzellenz (1,0)</span>
              </button>

              <!-- Hub 4: Junior & Trainee Karriere -->
              <button 
                @click="activeTab = 'career'"
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center space-x-2 whitespace-nowrap',
                  ['career', 'cheatsheet'].includes(activeTab)
                    ? 'bg-[#bf262e] text-white shadow-md shadow-[#bf262e]/30'
                    : 'text-[#c4bebe] hover:text-white hover:bg-white/5'
                ]"
              >
                <span>🎯</span>
                <span>Junior & Trainee Karriere</span>
              </button>

              <!-- Hub 5: Interview & Nachweise -->
              <button 
                @click="activeTab = 'interview'"
                :class="[
                  'px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all flex items-center space-x-2 whitespace-nowrap',
                  ['interview', 'cv_defense', 'files', 'notebook'].includes(activeTab)
                    ? 'bg-[#bf262e] text-white shadow-md shadow-[#bf262e]/30'
                    : 'text-[#c4bebe] hover:text-white hover:bg-white/5'
                ]"
              >
                <span>🎙️</span>
                <span>Interview & Nachweise</span>
              </button>
            </div>

            <!-- Breadcrumb / Deliverables Jump -->
            <div class="hidden md:flex items-center space-x-2 pl-4">
              <button 
                @click="activeTab = 'files'; selectedFileCat = 'Aktuelle Bewerbungsunterlagen'"
                class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-white text-[11px] font-medium flex items-center space-x-1.5 transition whitespace-nowrap"
              >
                <span>📁</span>
                <span>Deliverables-Register</span>
              </button>
            </div>
          </div>

          <!-- Contextual Sub-Navigation Pill Bar -->
          <div v-if="['project', 'solution_design', 'migration', 'tools'].includes(activeTab)" class="border-t border-white/5 bg-black/60 px-4 sm:px-6 lg:px-8 py-1.5">
            <div class="max-w-7xl mx-auto flex items-center space-x-2 overflow-x-auto text-[11px] custom-scrollbar">
              <span class="text-[#8f8888] font-medium whitespace-nowrap mr-1">Perspektive:</span>
              <button @click="activeTab = 'project'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'project' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🏛️ TP1–TP5 Steuerung & WBS
              </button>
              <button @click="activeTab = 'solution_design'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'solution_design' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                📐 Solution Design (FI/CO & Trennungsrechnung)
              </button>
              <button @click="activeTab = 'migration'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'migration' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🔄 Datenmigration & CVI (0,00 € Saldo)
              </button>
              <button @click="activeTab = 'tools'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'tools' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🛠️ Toolchain Hub (CALM & Signavio)
              </button>
            </div>
          </div>

          <div v-if="['thesis', 'enterprise_arch'].includes(activeTab)" class="border-t border-white/5 bg-black/60 px-4 sm:px-6 lg:px-8 py-1.5">
            <div class="max-w-7xl mx-auto flex items-center space-x-2 overflow-x-auto text-[11px] custom-scrollbar">
              <span class="text-[#8f8888] font-medium whitespace-nowrap mr-1">Perspektive:</span>
              <button @click="activeTab = 'thesis'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'thesis' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🎓 Masterarbeit 1,0 (12 Interviews & CSF)
              </button>
              <button @click="activeTab = 'enterprise_arch'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'enterprise_arch' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🏛️ TOGAF 9 ADM & ITIL 4 Service Operations
              </button>
            </div>
          </div>

          <div v-if="['career', 'cheatsheet'].includes(activeTab)" class="border-t border-white/5 bg-black/60 px-4 sm:px-6 lg:px-8 py-1.5">
            <div class="max-w-7xl mx-auto flex items-center space-x-2 overflow-x-auto text-[11px] custom-scrollbar">
              <span class="text-[#8f8888] font-medium whitespace-nowrap mr-1">Perspektive:</span>
              <button @click="activeTab = 'career'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'career' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🎯 Junior & Trainee Zielrollen (55k-65k €)
              </button>
              <button @click="activeTab = 'cheatsheet'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'cheatsheet' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                ⚡ Tech & BTP Architecture Cheatsheet
              </button>
            </div>
          </div>

          <div v-if="['interview', 'cv_defense', 'files', 'notebook'].includes(activeTab)" class="border-t border-white/5 bg-black/60 px-4 sm:px-6 lg:px-8 py-1.5">
            <div class="max-w-7xl mx-auto flex items-center space-x-2 overflow-x-auto text-[11px] custom-scrollbar">
              <span class="text-[#8f8888] font-medium whitespace-nowrap mr-1">Perspektive:</span>
              <button @click="activeTab = 'interview'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'interview' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🎙️ Pitches, STAR-Stories & Q&A
              </button>
              <button @click="activeTab = 'cv_defense'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'cv_defense' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                🛡️ CV De-Risking & Fangfragen
              </button>
              <button @click="activeTab = 'files'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'files' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                📂 Deliverables- & Nachweis-Register
              </button>
              <button @click="activeTab = 'notebook'" :class="['px-2.5 py-0.5 rounded-lg font-medium transition whitespace-nowrap', activeTab === 'notebook' ? 'bg-white/20 text-white font-bold' : 'text-[#8f8888] hover:text-white']">
                📝 Second Brain Notizbuch
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Mobile Slide-over Drawer for Small Screens -->
      <div v-if="isMobileMenuOpen" class="lg:hidden fixed inset-0 z-50 flex">
        <div @click="isMobileMenuOpen = false" class="fixed inset-0 bg-black/80 backdrop-blur-sm"></div>
        <div class="relative w-72 max-w-[80%] bg-[#121212] border-r border-white/10 h-full overflow-y-auto p-4 flex flex-col justify-between">
          <div class="space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-white/10">
              <span class="text-xs font-bold text-white">Navigation</span>
              <button @click="isMobileMenuOpen = false" class="text-white/60 hover:text-white text-sm">✕</button>
            </div>
            <div class="space-y-1">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition text-left',
                  activeTab === tab.id ? 'bg-[#bf262e] text-white font-bold' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2">
                  <span>{{ tab.icon }}</span>
                  <span>{{ tab.label }}</span>
                </div>
                <span v-if="tab.badge" class="text-[9px] px-1.5 py-0.2 rounded-full bg-white/20 text-white">{{ tab.badge }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Command Palette Modal (Ctrl + K) -->
      <div 
        v-if="isCommandPaletteOpen" 
        @click.self="closeCommandPalette"
        class="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-start justify-center pt-16 sm:pt-24 px-4 overflow-y-auto"
      >
        <div class="bg-[#141414] border border-white/15 rounded-2xl w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col max-h-[80vh]">
          
          <!-- Search Header -->
          <div class="p-4 border-b border-white/10 flex items-center space-x-3 bg-black/30">
            <span class="text-lg text-[#bf262e]">🔍</span>
            <input 
              id="command-palette-input"
              v-model="commandSearch" 
              type="text" 
              placeholder="Wonach suchst du? (z.B. Trennungsrechnung, Clean Core, WBS, 12 Interviews, Gehalt)..."
              class="flex-1 bg-transparent text-sm text-white placeholder-[#8f8888] focus:outline-none"
            >
            <button @click="closeCommandPalette" class="px-2 py-1 text-xs text-[#8f8888] hover:text-white bg-white/5 rounded-lg font-mono">ESC</button>
          </div>

          <!-- Quick Filters -->
          <div class="px-4 py-2 bg-black/40 border-b border-white/10 flex items-center space-x-2 text-[11px] overflow-x-auto custom-scrollbar">
            <span class="text-[#8f8888]">Direktfilter:</span>
            <button @click="commandSearch = 'Kaufmännisch'" class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 font-medium hover:bg-blue-500/30">FI/CO</button>
            <button @click="commandSearch = 'Clean Core'" class="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-medium hover:bg-purple-500/30">BTP & Architektur</button>
            <button @click="commandSearch = 'WBS'" class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-medium hover:bg-emerald-500/30">TP1-5 & PMO</button>
            <button @click="commandSearch = 'Masterarbeit'" class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-medium hover:bg-amber-500/30">Forschung 1,0</button>
            <button @click="commandSearch = 'Gehalt'" class="px-2 py-0.5 rounded bg-[#bf262e]/30 text-[#f87171] font-medium hover:bg-[#bf262e]/40">Karriere</button>
          </div>

          <!-- Results List -->
          <div class="p-2 overflow-y-auto space-y-1 custom-scrollbar max-h-96">
            <div 
              v-for="(item, idx) in commandFilteredResults" 
              :key="idx"
              @click="selectCommandResult(item)"
              class="p-3 rounded-xl hover:bg-white/5 cursor-pointer transition flex items-start justify-between space-x-3 group border border-transparent hover:border-white/10"
            >
              <div class="space-y-1">
                <div class="flex items-center space-x-2">
                  <span class="text-xs font-bold text-white group-hover:text-[#bf262e] transition">{{ item.title }}</span>
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-[#c4bebe]">{{ item.cat }}</span>
                </div>
                <p class="text-[11px] text-[#8f8888] leading-snug">{{ item.desc }}</p>
              </div>
              <div class="text-xs text-[#8f8888] group-hover:text-[#bf262e] flex items-center space-x-1 font-medium whitespace-nowrap pt-1">
                <span>Öffnen</span>
                <span>➔</span>
              </div>
            </div>
            <div v-if="commandFilteredResults.length === 0" class="p-8 text-center text-xs text-[#8f8888]">
              Keine Einträge für "{{ commandSearch }}" gefunden. Versuche Begriffe wie "Clean Core", "ACDOCA", "Trennungsrechnung" oder "WBS".
            </div>
          </div>

          <!-- Keyboard Hint Footer -->
          <div class="p-2.5 bg-black/50 border-t border-white/10 text-[11px] text-[#8f8888] flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <span>Navigation: <kbd class="px-1 py-0.5 bg-white/10 rounded font-mono text-[10px]">Klick</kbd> zum Öffnen</span>
              <span>Schließen: <kbd class="px-1 py-0.5 bg-white/10 rounded font-mono text-[10px]">ESC</kbd></span>
            </div>
            <span class="text-[#bf262e] font-medium">40+ Wissens-Nodes indexiert</span>
          </div>
        </div>
      </div>

      <!-- Main Content Area -->
      <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        
        <!-- Search Filter Alert if Active -->
        <div v-if="searchQuery" class="p-3 bg-[#bf262e]/10 border border-[#bf262e]/40 rounded-xl flex items-center justify-between text-xs text-white">
          <div class="flex items-center space-x-2">
            <span>🔍</span>
            <span>Suchfilter aktiv für: <strong>"{{ searchQuery }}"</strong>. Durchsucht das gesamte Wissensportal, Konzepte, Q&A und Dokumente.</span>
          </div>
          <button @click="searchQuery = ''" class="font-bold underline text-[#bf262e] hover:text-white">Filter zurücksetzen</button>
        </div>
"""
