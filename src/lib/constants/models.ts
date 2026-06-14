export type ModelTier = 'free' | 'eco' | 'reg' | 'pro';

const MODEL_TIER_MAP: Record<string, ModelTier> = {
	'liquid/lfm-2.5-1.2b': 'free',
	'gpt-oss': 'free',
	'claude-haiku-4.5': 'eco',
	'claude-opus-4.6': 'reg',
	'claude-opus-4.7': 'pro',
	'claude-sonnet-4.5': 'reg',
	'codebuddy/claude-opus-4.6': 'reg',
	'deepseek-v4-flash': 'free',
	'gpt-5.4': 'reg',
	'gpt-5.5': 'pro',
	'kiro/claude-sonnet-4.5': 'reg',
	'qwen-3.7-max': 'free',
	'qwen3.5:0.8b': 'free',
	'qwen3.6-plus': 'free',
	'xiaomi-mimo-v2.5': 'free'
};

export function getModelTier(modelName: string): ModelTier | null {
	return MODEL_TIER_MAP[modelName] ?? null;
}
