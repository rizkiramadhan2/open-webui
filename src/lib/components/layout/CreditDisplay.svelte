<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { getUserBalance } from '$lib/apis/payments';

	let balance: string | null = null;
	let loading = true;

	let refreshTimer: ReturnType<typeof setInterval> | null = null;

	$: balanceNum = balance !== null ? parseFloat(balance) : null;
	$: creditLevel =
		balanceNum === null
			? 'green'
			: balanceNum < 0.3
				? 'red'
				: balanceNum < 0.5
					? 'orange'
					: balanceNum <= 1
						? 'yellow'
						: 'green';

	async function fetchBalance() {
		try {
			const res = await getUserBalance(localStorage.token);
			balance = res.balance;
		} catch {
			balance = null;
		} finally {
			loading = false;
		}
	}

	onMount(() => {
		fetchBalance();
		refreshTimer = setInterval(fetchBalance, 5000);
	});

	onDestroy(() => {
		if (refreshTimer) clearInterval(refreshTimer);
	});

	export function refresh() {
		fetchBalance();
	}
</script>

{#if loading}
	<div class="credit-badge loading">
		<span class="credit-value">Credit: ...</span>
	</div>
{:else if balance !== null}
	<div class="credit-badge {creditLevel}">
		<span class="credit-value">Credit: {balanceNum?.toFixed(2)}</span>
	</div>
{/if}

<style>
	.credit-badge {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		height: 32px;
		padding: 0 10px;
		border-radius: 9999px;
		font-size: 12px;
		font-weight: 700;
		line-height: 1;
		white-space: nowrap;
		user-select: none;
	}

	.green {
		border: 1px solid rgba(52, 180, 100, 0.35);
		background: rgba(52, 180, 100, 0.12);
		color: #4ade80;
	}

	.yellow {
		border: 1px solid rgba(234, 179, 8, 0.35);
		background: rgba(234, 179, 8, 0.12);
		color: #facc15;
	}

	.orange {
		border: 1px solid rgba(249, 115, 22, 0.35);
		background: rgba(249, 115, 22, 0.12);
		color: #fb923c;
	}

	.red {
		border: 1px solid rgba(239, 68, 68, 0.35);
		background: rgba(239, 68, 68, 0.12);
		color: #f87171;
	}

	:global(.dark) .green {
		border-color: rgba(74, 222, 128, 0.3);
		background: rgba(74, 222, 128, 0.1);
		color: #4ade80;
	}

	:global(.dark) .yellow {
		border-color: rgba(250, 204, 21, 0.3);
		background: rgba(250, 204, 21, 0.1);
		color: #facc15;
	}

	:global(.dark) .orange {
		border-color: rgba(251, 146, 60, 0.3);
		background: rgba(251, 146, 60, 0.1);
		color: #fb923c;
	}

	:global(.dark) .red {
		border-color: rgba(248, 113, 113, 0.3);
		background: rgba(248, 113, 113, 0.1);
		color: #f87171;
	}

	.credit-value {
		letter-spacing: 0.02em;
	}

	.loading {
		opacity: 0.5;
		border: 1px solid rgba(128, 128, 128, 0.3);
		background: rgba(128, 128, 128, 0.1);
		color: #9ca3af;
	}
</style>
