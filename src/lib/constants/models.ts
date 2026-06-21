import { writable } from 'svelte/store';

import { getModelTiers } from '$lib/apis/models';

export type ModelTier = 'free' | 'eco' | 'reg' | 'pro';

export const modelTierMap = writable<Record<string, string>>({});

let tierLoadPromise: Promise<void> | null = null;

export const loadModelTiers = async (token: string = '') => {
	if (tierLoadPromise) {
		return tierLoadPromise;
	}

	tierLoadPromise = (async () => {
		try {
			const tiers = await getModelTiers(token);
			if (tiers) {
				modelTierMap.set(tiers);
			}
		} catch (e) {
			console.error('Failed to load model tiers', e);
		} finally {
			tierLoadPromise = null;
		}
	})();

	return tierLoadPromise;
};
