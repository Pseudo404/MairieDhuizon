// ============================================================
// input.js — Gestion des entrées (Clavier + Joystick Tactile)
// ============================================================

const keys = {};

// Joystick virtuel
let joystickActive = false;
let joystickCenter = { x: 0, y: 0 };
let joystickDelta = { dx: 0, dy: 0 };

export function initInput() {
    // --- CLAVIER ---
    window.addEventListener("keydown", (e) => { keys[e.code] = true; });
    window.addEventListener("keyup", (e) => { keys[e.code] = false; });

    // --- JOYSTICK TACTILE ---
    const joyZone = document.getElementById('joystick-zone');
    const joyBase = document.getElementById('joystick');
    const joyKnob = document.getElementById('joystickKnob');
    const maxDistance = 40; // Rayon max du joystick

    if (!joyZone || !joyBase || !joyKnob) return; // Sécurité

    joyZone.addEventListener('touchstart', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        
        joystickActive = true;
        joystickCenter = { x: touch.clientX, y: touch.clientY };
        joystickDelta = { dx: 0, dy: 0 };

        // Afficher la base là où on touche
        joyBase.style.display = 'block';
        // Le CSS le centre avec translate(-50%, -50%) ? Non, l'ancien CSS a juste width/height 110px et translate non défini sur #joystick.
        joyBase.style.left = `${touch.clientX - 55}px`;
        joyBase.style.top = `${touch.clientY - 55}px`;
        joyKnob.style.transform = `translate(-50%, -50%)`;
    }, { passive: false });

    joyZone.addEventListener('touchmove', (e) => {
        e.preventDefault();
        if (!joystickActive) return;

        const touch = e.touches[0];
        const dx = touch.clientX - joystickCenter.x;
        const dy = touch.clientY - joystickCenter.y;
        
        const distance = Math.sqrt(dx * dx + dy * dy);
        const clampedDistance = Math.min(distance, maxDistance);
        
        let dirX = 0, dirY = 0;
        if (distance > 0) {
            dirX = dx / distance;
            dirY = dy / distance;
        }

        joystickDelta = { dx: dirX, dy: dirY };

        const knobX = dirX * clampedDistance;
        const knobY = dirY * clampedDistance;
        joyKnob.style.transform = `translate(calc(-50% + ${knobX}px), calc(-50% + ${knobY}px))`;
    }, { passive: false });

    const endJoystick = (e) => {
        if(e) e.preventDefault();
        joystickActive = false;
        joystickDelta = { dx: 0, dy: 0 };
        joyBase.style.display = 'none';
        joyKnob.style.transform = `translate(-50%, -50%)`;
    };

    joyZone.addEventListener('touchend', endJoystick);
    joyZone.addEventListener('touchcancel', endJoystick);
}

export function getInput() {
    let dx = 0;
    let dy = 0;

    if (keys["KeyW"] || keys["KeyZ"] || keys["ArrowUp"]) dy -= 1;
    if (keys["KeyS"] || keys["ArrowDown"]) dy += 1;
    if (keys["KeyA"] || keys["KeyQ"] || keys["ArrowLeft"]) dx -= 1;
    if (keys["KeyD"] || keys["ArrowRight"]) dx += 1;

    const length = Math.sqrt(dx * dx + dy * dy);
    if (length > 0) {
        dx /= length;
        dy /= length;
    }

    if (dx !== 0 || dy !== 0) {
        return { dx, dy };
    }

    return joystickDelta;
}
