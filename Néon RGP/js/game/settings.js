// ============================================================
//  settings.js — Chargement / sauvegarde des préférences joueur.
// ============================================================
const KEY = "neonSettings";

export function loadSettings() {
    return JSON.parse(localStorage.getItem(KEY) || '{"sound":true,"hpBars":false}');
}

export function saveSettings(settings) {
    localStorage.setItem(KEY, JSON.stringify(settings));
}
