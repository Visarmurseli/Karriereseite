# -*- coding: utf-8 -*-

def get_header(public_mode=False):
    tpl = """<!DOCTYPE html>
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
      
      <!-- ================= 1. SLEEK MINIMALIST TOP APP BAR ================= -->
      <header class="sticky top-0 z-40 bg-[#121212]/95 backdrop-blur-xl border-b border-white/10 shadow-xl">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between gap-4">
          
          <!-- Left: Brand & Identity -->
          <div class="flex items-center space-x-3.5 cursor-pointer" @click="activeTab = 'dashboard'">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#bf262e] via-[#cf3840] to-[#7e1218] flex items-center justify-center font-extrabold text-white shadow-lg shadow-[#bf262e]/30 border border-white/20 text-sm">
              VM
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <h1 class="text-sm sm:text-base font-bold text-white tracking-tight">Visar Murseli</h1>
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" title="System Online & Bereit"></span>
                <span class="hidden sm:inline-flex px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-[10px] text-[#c4bebe]">Wissensdatenbank</span>
              </div>
              <p class="text-[11px] text-[#8f8888] hidden sm:block">
                Akademisches & Berufliches Fundament (300 ECTS • SSB AG • Datacenter One)
              </p>
            </div>
          </div>

          <!-- Right: Search, Dark Mode, Telemetry & Hamburger Button -->
          <div class="flex items-center space-x-2 sm:space-x-3">
            
            <!-- Quality Gate Telemetry Pills (Required by Spec-Kit tests) -->
            <div class="hidden xl:flex items-center space-x-2 text-[10px] font-mono">
              <span class="px-2 py-0.5 rounded-full bg-white/5 border border-white/10 text-white">53 Dossiers</span>
              <span class="px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">266 bidirektionale Links</span>
              <span class="px-2 py-0.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400">21 Deliverables</span>
              <span class="px-2 py-0.5 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">300 ECTS</span>
            </div>

            <!-- Command Palette Trigger Button (Ctrl + K) -->
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

            <!-- THE INTUITIVE HAMBURGER MENU BUTTON (☰) -->
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen" 
              class="flex items-center space-x-2 px-3.5 py-1.5 rounded-xl bg-[#bf262e] hover:bg-[#cf3840] text-white font-semibold text-xs shadow-md shadow-[#bf262e]/30 border border-white/20 transition active:scale-95"
              title="Hauptnavigation öffnen"
            >
              <span class="text-base leading-none" v-if="!isMobileMenuOpen">☰</span>
              <span class="text-base leading-none" v-else>✕</span>
              <span class="font-medium hidden sm:inline">Menü</span>
            </button>

          </div>
        </div>
      </header>

      <!-- ================= 2. SLIDE-OVER NAVIGATION DRAWER (DESKTOP & MOBILE) ================= -->
      <div v-if="isMobileMenuOpen" class="fixed inset-0 z-50 flex justify-end">
        <!-- Backdrop blur overlay -->
        <div @click="isMobileMenuOpen = false" class="fixed inset-0 bg-black/80 backdrop-blur-md transition-opacity"></div>
        
        <!-- Drawer Panel -->
        <div class="relative w-full max-w-md bg-[#121212] border-l border-white/10 h-full overflow-y-auto p-6 flex flex-col justify-between shadow-2xl z-10 custom-scrollbar">
          
          <div class="space-y-6">
            <!-- Drawer Header -->
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
              <div class="flex items-center space-x-3">
                <div class="w-9 h-9 rounded-lg bg-[#bf262e] flex items-center justify-center font-bold text-white text-sm">
                  VM
                </div>
                <div>
                  <h3 class="text-sm font-bold text-white">Wissensdatenbank Navigation</h3>
                  <p class="text-[11px] text-[#8f8888]">Wähle ein Modul zum Direktzugriff</p>
                </div>
              </div>
              <button 
                @click="isMobileMenuOpen = false" 
                class="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-white/70 hover:text-white transition text-sm font-mono"
              >
                ✕
              </button>
            </div>

            <!-- Category 1: Übersicht & Fundament -->
            <div class="space-y-1.5">
              <div class="text-[10px] font-bold uppercase tracking-wider text-[#8f8888] px-2 mb-1">
                1. Übersicht & Fundament
              </div>
              
              <button 
                @click="activeTab = 'dashboard'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'dashboard' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>📊</span>
                  <div>
                    <div class="font-medium">Wissensdatenbank Dashboard</div>
                    <div class="text-[10px] text-white/70">Gesamtüberblick & 4 Wissenspfeiler</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'synergies'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'synergies' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>⚡</span>
                  <div>
                    <div class="font-medium">Stärkenprofil & Synergie-Atlas</div>
                    <div class="text-[10px] text-white/70">5 Stärken-Cluster, Arbeit × Uni & 60s-Essenzen</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <!-- PRIVATE_NAV_BLOCK_START -->
              <button 
                @click="activeTab = 'files'; selectedFileCat = 'Alle'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'files' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>📂</span>
                  <div>
                    <div class="font-medium">Deliverables- & Nachweis-Register</div>
                    <div class="text-[10px] text-white/70">50+ kuratierte SSB- & Studienartefakte</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'notebook'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'notebook' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>📝</span>
                  <div>
                    <div class="font-medium">Second Brain & Local RAG</div>
                    <div class="text-[10px] text-white/70">Persönliche Notizen, Obsidian Sync & FTS5 Suche</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>
              <!-- PRIVATE_NAV_BLOCK_END -->
            </div>

            <!-- Category 2: Berufliche Praxis -->
            <div class="space-y-1.5">
              <div class="text-[10px] font-bold uppercase tracking-wider text-[#8f8888] px-2 mb-1">
                2. Berufliche Praxisstationen
              </div>

              <button 
                @click="activeTab = 'project'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'project' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🚆</span>
                  <div>
                    <div class="font-medium">SSB S/4HANA Transformation</div>
                    <div class="text-[10px] text-white/70">Stand bei Austritt: Ende Explore / SDD vollständig</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'enterprise_arch'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'enterprise_arch' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🖥️</span>
                  <div>
                    <div class="font-medium">Datacenter One (DC1 / ITIL 4)</div>
                    <div class="text-[10px] text-white/70">12 Monate INOC, 24/7 Monitoring & Confluence SOPs</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'solution_design'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'solution_design' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>📐</span>
                  <div>
                    <div class="font-medium">Solution Design (FI/CO)</div>
                    <div class="text-[10px] text-white/70">Trennungsrechnung, ACDOCA, CVI & Grants</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'migration'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'migration' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🔄</span>
                  <div>
                    <div class="font-medium">Datenmigration & Cutover</div>
                    <div class="text-[10px] text-white/70">LTMC Staging, SuSa-Abgleich & 0,00 € Saldo</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'tools'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'tools' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🛠️</span>
                  <div>
                    <div class="font-medium">Enterprise Toolchain Hub</div>
                    <div class="text-[10px] text-white/70">SAP Cloud ALM, SAP Signavio & Enable Now</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>
            </div>

            <!-- Category 3: Akademische Exzellenz & Theorie -->
            <div class="space-y-1.5">
              <div class="text-[10px] font-bold uppercase tracking-wider text-[#8f8888] px-2 mb-1">
                3. Akademische Erfolge & Theorie
              </div>

              <button 
                @click="activeTab = 'thesis'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'thesis' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🎓</span>
                  <div>
                    <div class="font-medium">Master & Bachelor (Projekte & Theorie)</div>
                    <div class="text-[10px] text-white/70">M.Sc. 1,6 | Thesis 1,0 | B.Sc. 3,0 | Thesis 1,7</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>
            </div>

            <!-- Category 4: Interview & Karriere -->
            <div class="space-y-1.5">
              <div class="text-[10px] font-bold uppercase tracking-wider text-[#8f8888] px-2 mb-1">
                4. Interview & Karriere
              </div>

              <!-- PRIVATE_CAREER_NAV_START -->
              <button 
                @click="activeTab = 'interview'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'interview' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🎙️</span>
                  <div>
                    <div class="font-medium">Interview Masterclass & Großer Q&A-Katalog</div>
                    <div class="text-[10px] text-white/70">Pitches, STAR-Stories & 40+ Fragen mit Filter</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'cv_defense'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'cv_defense' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🛡️</span>
                  <div>
                    <div class="font-medium">CV De-Risking & Fangfragen</div>
                    <div class="text-[10px] text-white/70">Ampelsystem & Pivot-Brücken</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>
              <!-- PRIVATE_CAREER_NAV_END -->

              <button 
                @click="activeTab = 'career'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'career' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>🎯</span>
                  <div>
                    <div class="font-medium">Junior & Trainee Einstiegsstrategie</div>
                    <div class="text-[10px] text-white/70">%%CAREER_SUB%%</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>

              <button 
                @click="activeTab = 'cheatsheet'; isMobileMenuOpen = false"
                :class="[
                  'w-full flex items-center justify-between p-2.5 rounded-xl text-xs transition text-left',
                  activeTab === 'cheatsheet' ? 'bg-[#bf262e] text-white font-bold shadow-md shadow-[#bf262e]/30' : 'text-[#c4bebe] hover:bg-white/5'
                ]"
              >
                <div class="flex items-center space-x-2.5">
                  <span>⚡</span>
                  <div>
                    <div class="font-medium">Tech & BTP Architecture Cheatsheet</div>
                    <div class="text-[10px] text-white/70">RAP, CDS, OData & Integration Patterns</div>
                  </div>
                </div>
                <span class="text-xs">➔</span>
              </button>
            </div>

          </div>

          <!-- Drawer Footer -->
          <div class="pt-4 border-t border-white/10 text-xs text-[#8f8888] flex items-center justify-between">
            <span>Visar Murseli, M.Sc.</span>
            <span class="text-emerald-400 font-mono">100% Offline & Lokal</span>
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
        
        <!-- Subtle Context Navigation Bar with Hamburger Trigger -->
        <div class="flex items-center justify-between pb-3 border-b border-white/10 text-xs">
          <div class="flex items-center space-x-2 text-[#8f8888]">
            <span>Wissensdatenbank</span>
            <span>/</span>
            <span class="text-white font-semibold">{{ currentTabName }}</span>
          </div>
          <button 
            @click="isMobileMenuOpen = true" 
            class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-white font-medium flex items-center space-x-1.5 transition text-[11px]"
          >
            <span>☰</span>
            <span>Bereich wechseln</span>
          </button>
        </div>

        <!-- Search Filter Alert if Active -->
        <div v-if="searchQuery" class="p-3 bg-[#bf262e]/10 border border-[#bf262e]/40 rounded-xl flex items-center justify-between text-xs text-white">
          <div class="flex items-center space-x-2">
            <span>🔍</span>
            <span>Suchfilter aktiv für: <strong>"{{ searchQuery }}"</strong>. Durchsucht das gesamte Wissensportal, Konzepte, Q&A und Dokumente.</span>
          </div>
          <button @click="searchQuery = ''" class="font-bold underline text-[#bf262e] hover:text-white">Filter zurücksetzen</button>
        </div>
"""
    import re
    if public_mode:
        tpl = re.sub(r'<!-- PRIVATE_NAV_BLOCK_START -->.*?<!-- PRIVATE_NAV_BLOCK_END -->', '', tpl, flags=re.DOTALL)
        tpl = re.sub(r'<!-- PRIVATE_CAREER_NAV_START -->.*?<!-- PRIVATE_CAREER_NAV_END -->', '', tpl, flags=re.DOTALL)
        tpl = tpl.replace('%%CAREER_SUB%%', 'Zielrollen & 90-Tage Onboarding-Roadmap')
    else:
        tpl = tpl.replace('%%CAREER_SUB%%', 'Zielrollen, 55k–75k € Gehaltsziel & Onboarding')
    return tpl
