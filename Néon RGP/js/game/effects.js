export const EFFECT_TYPES = Object.freeze({
    STUN: 'stun',
    BURN: 'burn',
    POISON: 'poison',
    CRITICAL: 'critical'
});

export const EFFECT_DEFINITIONS = Object.freeze({
    [EFFECT_TYPES.STUN]: {
        name: 'Étourdissement',
        color: '#ffe066',
        visual: { type: 'shake', amplitude: 3 }
    },
    [EFFECT_TYPES.BURN]: {
        name: 'Brûlure',
        color: '#ff7a45',
        visual: { type: 'flames' }
    },
    [EFFECT_TYPES.POISON]: {
        name: 'Poison',
        color: '#9dff57',
        visual: { type: 'bubbles' }
    },
    [EFFECT_TYPES.CRITICAL]: {
        name: 'Coup critique',
        color: '#ffcf5c',
        visual: { type: 'burst' }
    }
});

export function applyEffect(target, effectType, duration) {
    if (!EFFECT_DEFINITIONS[effectType]) {
        throw new Error(`Effet inconnu : ${effectType}`);
    }

    if (!target.activeEffects) target.activeEffects = new Map();

    // Réappliquer un effet rafraîchit sa durée sans la raccourcir.
    const currentDuration = target.activeEffects.get(effectType) || 0;
    target.activeEffects.set(effectType, Math.max(currentDuration, duration));
}

export function updateEffects(target, elapsedMs) {
    if (!target.activeEffects) return;

    for (const [effectType, remainingMs] of target.activeEffects) {
        const nextDuration = remainingMs - elapsedMs;
        if (nextDuration <= 0) {
            target.activeEffects.delete(effectType);
        } else {
            target.activeEffects.set(effectType, nextDuration);
        }
    }
}

export function hasEffect(target, effectType) {
    return Boolean(target.activeEffects?.has(effectType));
}

export function getEffectShakeOffset(target) {
    if (!hasEffect(target, EFFECT_TYPES.STUN)) return { x: 0, y: 0 };

    const amplitude = EFFECT_DEFINITIONS[EFFECT_TYPES.STUN].visual.amplitude;
    const phase = Date.now() / 28 + target.x + target.y;
    return {
        x: Math.sin(phase) * amplitude,
        y: Math.cos(phase * 1.7) * amplitude
    };
}
