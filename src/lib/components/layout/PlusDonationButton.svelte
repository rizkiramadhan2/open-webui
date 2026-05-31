<script lang="ts">
    import { WEBUI_BASE_URL } from '$lib/constants';

    export let qrCodeUrl = `${WEBUI_BASE_URL}/static/qris.png`;
    export let message = 'Donate to get PLUS model';

    let open = false;
</script>

<div class="relative shrink-0">
    <button
        type="button"
        class="plus-button"
        aria-label="Donate to get PLUS model"
        on:click|stopPropagation={() => {
            open = !open;
        }}
    >
        <span class="plus-text">DONATE</span>
    </button>

    {#if open}
        <button
            type="button"
            class="fixed inset-0 z-[9998] cursor-default bg-transparent"
            aria-label="Close donation popup"
            on:click={() => {
                open = false;
            }}
        />

        <div class="donation-popover">
            <div class="flex items-start justify-between gap-2">
                <p class="title">{message}</p>

                <button
                    type="button"
                    class="close-button"
                    aria-label="Close"
                    on:click={() => {
                        open = false;
                    }}
                >
                    ×
                </button>
            </div>

            <img src={qrCodeUrl} alt="Donation QR" class="qr" />

            <p class="hint">Scan to support</p>
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
        width: 190px;
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

    .qr {
        width: 140px;
        height: 140px;
        object-fit: contain;
        display: block;
        margin: 0.7rem auto 0;
        border-radius: 0.6rem;
        background: white;
    }

    .hint {
        margin: 0.45rem 0 0;
        font-size: 0.7rem;
        opacity: 0.75;
    }
</style>