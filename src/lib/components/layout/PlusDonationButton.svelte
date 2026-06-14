<script lang="ts">
	import { createPayment, getPaymentStatus } from '$lib/apis/payments';
	import { user } from '$lib/stores';
	import QRCode from 'qrcode';
	import { onDestroy } from 'svelte';

	export let message = 'Top up Credit';

	const CREDIT_VALUE = 10000;
	const MIN_CREDITS = 1;
	const MAX_CREDITS = 10;

	let open = false;
	let credits = 5;
	let loading = false;
	let error = '';
	let qrDataUrl = '';
	let paymentStatus = '';
	let trxId = '';
	let showTooltip = false;

	$: amount = credits * CREDIT_VALUE;

	let pollTimer: ReturnType<typeof setInterval> | null = null;

	function cleanup() {
		if (pollTimer) {
			clearInterval(pollTimer);
			pollTimer = null;
		}
	}

	onDestroy(cleanup);

	function decrementCredits() {
		if (credits > MIN_CREDITS) credits--;
	}

	function incrementCredits() {
		if (credits < MAX_CREDITS) credits++;
	}

	function handleCreditsInput(e: Event) {
		const val = parseInt((e.target as HTMLInputElement).value, 10);
		if (!isNaN(val)) {
			credits = Math.max(MIN_CREDITS, Math.min(MAX_CREDITS, val));
		}
	}

	async function startPayment() {
		if (!$user?.id) return;

		loading = true;
		error = '';
		qrDataUrl = '';
		paymentStatus = '';
		trxId = '';
		cleanup();

		// overwrite the user id for development
		// user_id = '19d98736-b895-46c5-b3f8-7da99f0107c9';

		try {
			const res = await createPayment(localStorage.token, {
				user_id: $user.id,
				provider: 'pakasir',
				amount,
				currency: 'IDR',
				description: `${credits} credit top up`,
				return_url: `${window.location.origin}/payment/success`,
				method: 'qris'
			});

			trxId = res.trx_id;
			paymentStatus = res.status;

			if (res.payment_url) {
				qrDataUrl = await QRCode.toDataURL(res.payment_url, {
					width: 280,
					margin: 2,
					color: {
						dark: '#000000',
						light: '#ffffff'
					}
				});
			}

			if (res.status === 'pending') {
				let pollErrors = 0;

				pollTimer = setInterval(async () => {
					try {
						const status = await getPaymentStatus(localStorage.token, trxId);
						pollErrors = 0;
						paymentStatus = status.status;

						if (status.status !== 'pending') {
							cleanup();
						}
					} catch {
						pollErrors++;
						if (pollErrors >= 10) {
							error = 'Lost connection to payment service';
							cleanup();
						}
					}
				}, 1000);
			}
		} catch (e) {
			error = typeof e === 'string' ? e : 'Failed to create payment';
		} finally {
			loading = false;
		}
	}

	function handleOpen() {
		open = !open;
	}

	function handleClose() {
		open = false;
		cleanup();
	}

	function handleRetry() {
		qrDataUrl = '';
		paymentStatus = '';
		trxId = '';
		error = '';
		startPayment();
	}

	function handleBack() {
		cleanup();
		qrDataUrl = '';
		paymentStatus = '';
		trxId = '';
		error = '';
	}
</script>

<div class="relative shrink-0">
	<button
		type="button"
		class="plus-button"
		aria-label="Top up Credit"
		on:click|stopPropagation={handleOpen}
	>
		<span class="plus-text">TOP UP</span>
	</button>

	{#if open}
		<button
			type="button"
			class="fixed inset-0 z-[9998] cursor-default bg-transparent"
			aria-label="Close donation popup"
			on:click={handleClose}
		></button>

		<div class="donation-popover">
			<div class="flex items-start justify-between gap-2">
				<p class="title">{message}</p>

				<button
					type="button"
					class="close-button"
					aria-label="Close"
					on:click={handleClose}
				>
					×
				</button>
			</div>

			{#if qrDataUrl || paymentStatus === 'completed' || paymentStatus === 'expired'}
				{#if paymentStatus === 'completed'}
					<div class="qr-placeholder">
						<div class="success-icon">✓</div>
						<p class="success-text">Payment successful!</p>
						<p class="hint">{credits} credit{credits > 1 ? 's' : ''} added</p>
						<button type="button" class="back-button" on:click={handleBack}>
							← Buy more
						</button>
					</div>
				{:else if paymentStatus === 'expired'}
					<div class="qr-placeholder">
						<p class="error-text">Payment expired</p>
						<button type="button" class="retry-button" on:click={handleRetry}>Retry</button>
						<button type="button" class="back-button" on:click={handleBack}>← Back</button>
					</div>
				{:else if loading}
					<div class="qr-placeholder">
						<div class="spinner"></div>
						<p class="hint">Generating QRIS...</p>
					</div>
				{:else if error}
					<div class="qr-placeholder">
						<p class="error-text">{error}</p>
						<button type="button" class="retry-button" on:click={handleRetry}>Retry</button>
						<button type="button" class="back-button" on:click={handleBack}>← Back</button>
					</div>
				{:else if qrDataUrl}
					<img src={qrDataUrl} alt="QRIS Payment" class="qr" />
					<p class="hint">Scan QRIS to pay Rp {amount.toLocaleString()}</p>
					{#if paymentStatus === 'pending'}
						<p class="status-pending">Waiting for payment...</p>
					{/if}
				{/if}
			{:else}
				<div class="credit-section">
					<div class="credit-label-row">
						<span class="credit-label">Credits</span>
						<span
							class="tooltip-trigger"
							on:mouseenter={() => (showTooltip = true)}
							on:mouseleave={() => (showTooltip = false)}
							on:focus={() => (showTooltip = true)}
							on:blur={() => (showTooltip = false)}
							tabindex="0"
							role="button"
							aria-label="Credit info"
						>
							?
							{#if showTooltip}
								<span class="tooltip-content">
									<strong>5 credits ≈ 1 month usage</strong><br /><br />
									<strong>Claude Opus &amp; GPT 5.5</strong><br />
									Heavy: 1 credit ≈ 20-25 req (50K tokens/call)<br />
									Normal: 1 credit &gt;100 req (2K-5K tokens/call)<br /><br />
									<strong>Other models</strong><br />
									1 credit ≈ 200-500 req (depends on pricing)
								</span>
							{/if}
						</span>
					</div>

					<div class="credit-stepper">
						<button
							type="button"
							class="stepper-btn"
							disabled={credits <= MIN_CREDITS}
							on:click={decrementCredits}
						>
							−
						</button>
						<input
							type="number"
							class="credit-input"
							value={credits}
							min={MIN_CREDITS}
							max={MAX_CREDITS}
							on:input={handleCreditsInput}
						/>
						<button
							type="button"
							class="stepper-btn"
							disabled={credits >= MAX_CREDITS}
							on:click={incrementCredits}
						>
							+
						</button>
					</div>

					<p class="amount-display">Rp {amount.toLocaleString()}</p>

					<button
						type="button"
						class="pay-button"
						disabled={loading}
						on:click={startPayment}
					>
						Pay Now
					</button>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.plus-button {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		height: 32px;
		min-width: 48px;
		padding: 0 12px;
		border-radius: 9999px;
		border: 1px solid rgba(51, 113, 213, 0.35);
		background: rgba(51, 113, 213, 0.14);
		color: #7aa7ff;
		font-size: 12px;
		font-weight: 700;
		line-height: 1;
		letter-spacing: 0.03em;
		white-space: nowrap;
		cursor: pointer;
		transition:
			background-color 0.15s ease,
			color 0.15s ease,
			border-color 0.15s ease,
			transform 0.15s ease;
	}

	.plus-button:hover {
		background: rgba(51, 113, 213, 0.22);
		border-color: rgba(51, 113, 213, 0.6);
		color: #ffffff;
		transform: translateY(-1px);
	}

	.plus-text {
		display: inline-block;
		white-space: nowrap;
		word-break: keep-all;
	}

	.donation-popover {
		position: absolute;
		right: 0;
		top: calc(100% + 0.6rem);
		z-index: 9999;
		width: 230px;
		padding: 0.8rem;
		border-radius: 1rem;
		border: 1px solid #3371d5;
		background: #f1f8fe;
		color: #2b6cd4;
		box-shadow: 0 16px 40px rgba(0, 0, 0, 0.24);
		text-align: center;
	}

	:global(.dark) .donation-popover {
		background: #020c1d;
		border-color: #153a83;
		color: #6795ec;
	}

	.title {
		margin: 0;
		flex: 1;
		font-size: 0.8rem;
		font-weight: 700;
		line-height: 1.25;
		text-align: left;
	}

	.close-button {
		border: none;
		background: transparent;
		color: inherit;
		font-size: 1.1rem;
		line-height: 1;
		cursor: pointer;
		opacity: 0.65;
		padding: 0;
	}

	.close-button:hover {
		opacity: 1;
	}

	.credit-section {
		margin-top: 0.7rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.6rem;
	}

	.credit-label-row {
		display: flex;
		align-items: center;
		gap: 0.35rem;
		align-self: flex-start;
	}

	.credit-label {
		font-size: 0.75rem;
		font-weight: 600;
	}

	.tooltip-trigger {
		position: relative;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 16px;
		height: 16px;
		border-radius: 50%;
		background: rgba(51, 113, 213, 0.2);
		color: inherit;
		font-size: 0.6rem;
		font-weight: 700;
		cursor: help;
		user-select: none;
	}

	:global(.dark) .tooltip-trigger {
		background: rgba(103, 149, 236, 0.2);
	}

	.tooltip-content {
		position: absolute;
		top: -4px;
		right: calc(100% + 8px);
		width: 220px;
		padding: 0.6rem;
		border-radius: 0.5rem;
		background: #1a2332;
		color: #e2e8f0;
		font-size: 0.65rem;
		font-weight: 400;
		line-height: 1.5;
		text-align: left;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
		z-index: 10000;
		pointer-events: none;
	}

	.tooltip-content::after {
		content: '';
		position: absolute;
		top: 8px;
		left: 100%;
		border: 5px solid transparent;
		border-left-color: #1a2332;
	}

	:global(.dark) .tooltip-content {
		background: #1e293b;
		color: #cbd5e1;
	}

	:global(.dark) .tooltip-content::after {
		border-left-color: #1e293b;
	}

	.credit-stepper {
		display: flex;
		align-items: center;
		gap: 0;
	}

	.stepper-btn {
		width: 36px;
		height: 36px;
		display: flex;
		align-items: center;
		justify-content: center;
		border: 1px solid #3371d5;
		background: transparent;
		color: inherit;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition:
			background-color 0.15s ease,
			opacity 0.15s ease;
	}

	.stepper-btn:first-child {
		border-radius: 0.5rem 0 0 0.5rem;
	}

	.stepper-btn:last-child {
		border-radius: 0 0.5rem 0.5rem 0;
	}

	.stepper-btn:hover:not(:disabled) {
		background: rgba(51, 113, 213, 0.1);
	}

	.stepper-btn:disabled {
		opacity: 0.35;
		cursor: not-allowed;
	}

	:global(.dark) .stepper-btn {
		border-color: #153a83;
	}

	:global(.dark) .stepper-btn:hover:not(:disabled) {
		background: rgba(103, 149, 236, 0.1);
	}

	.credit-input {
		width: 48px;
		height: 36px;
		border: 1px solid #3371d5;
		border-left: none;
		border-right: none;
		background: transparent;
		color: inherit;
		font-size: 1rem;
		font-weight: 700;
		text-align: center;
		outline: none;
		appearance: textfield;
		-moz-appearance: textfield;
	}

	.credit-input::-webkit-outer-spin-button,
	.credit-input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}

	:global(.dark) .credit-input {
		border-color: #153a83;
	}

	.amount-display {
		margin: 0;
		font-size: 0.85rem;
		font-weight: 700;
		opacity: 0.85;
	}

	.pay-button {
		width: 100%;
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 0.5rem;
		background: #3371d5;
		color: #ffffff;
		font-size: 0.75rem;
		font-weight: 700;
		cursor: pointer;
		transition:
			background-color 0.15s ease,
			opacity 0.15s ease;
	}

	.pay-button:hover:not(:disabled) {
		background: #2563c4;
	}

	.pay-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	:global(.dark) .pay-button {
		background: #2563c4;
	}

	:global(.dark) .pay-button:hover:not(:disabled) {
		background: #1d4ed8;
	}

	.qr {
		width: 160px;
		height: 160px;
		object-fit: contain;
		display: block;
		margin: 0.7rem auto 0;
		border-radius: 0.6rem;
		background: white;
	}

	.qr-placeholder {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 180px;
		margin-top: 0.7rem;
	}

	.spinner {
		width: 32px;
		height: 32px;
		border: 3px solid rgba(51, 113, 213, 0.2);
		border-top-color: #3371d5;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.hint {
		margin: 0.45rem 0 0;
		font-size: 0.7rem;
		opacity: 0.75;
	}

	.error-text {
		margin: 0;
		font-size: 0.75rem;
		color: #e53e3e;
	}

	.success-icon {
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background: #38a169;
		color: white;
		font-size: 1.2rem;
		font-weight: 700;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.success-text {
		margin: 0.5rem 0 0;
		font-size: 0.75rem;
		font-weight: 600;
		color: #38a169;
	}

	.retry-button {
		margin-top: 0.5rem;
		padding: 0.3rem 0.8rem;
		border: 1px solid #3371d5;
		border-radius: 0.5rem;
		background: transparent;
		color: inherit;
		font-size: 0.7rem;
		font-weight: 600;
		cursor: pointer;
		transition: background-color 0.15s ease;
	}

	.retry-button:hover {
		background: rgba(51, 113, 213, 0.1);
	}

	.back-button {
		margin-top: 0.4rem;
		padding: 0;
		border: none;
		background: transparent;
		color: inherit;
		font-size: 0.65rem;
		opacity: 0.6;
		cursor: pointer;
	}

	.back-button:hover {
		opacity: 1;
		text-decoration: underline;
	}

	.status-pending {
		margin: 0.3rem 0 0;
		font-size: 0.65rem;
		opacity: 0.6;
		animation: pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%,
		100% {
			opacity: 0.6;
		}
		50% {
			opacity: 1;
		}
	}
</style>
