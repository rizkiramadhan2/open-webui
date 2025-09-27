<script lang="ts">
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  import { WEBUI_BASE_URL } from '$lib/constants';

  {/* export let qrCodeUrl = `/static/qris.png`; */}
  export let qrCodeUrl = `${WEBUI_BASE_URL}/static/qris.png`;
  export let message = 'Donate to get PLUS model';
  export let autoHideDelay = 1000;

  const dispatch = createEventDispatcher();

  let fullyVisible = true;
  let visible = true;

  let hideTimeout: ReturnType<typeof setTimeout>;

  function startAutoHide() {
    clearTimeout(hideTimeout);
    hideTimeout = setTimeout(() => {
      fullyVisible = false;
    }, autoHideDelay);
  }

  function cancelAutoHide() {
    clearTimeout(hideTimeout);
    fullyVisible = true;
  }

  function handleMouseEnter() {
    cancelAutoHide();
  }

  function handleMouseLeave() {
    startAutoHide();
  }

  function close() {
    visible = false;
    dispatch('close');
  }

  onMount(() => {
    startAutoHide();
  });

  onDestroy(() => {
    clearTimeout(hideTimeout);
  });
</script>

{#if visible}
  <div 
    class="popup fixed bottom-8 right-0 flex items-center rounded-lg shadow-lg bg-[#F1F8FE] dark:bg-[#020C1D] border border-[#3371D5] dark:border-[#03113B] text-[#2B6CD4] dark:text-[#6795EC] cursor-pointer select-none"
    on:mouseenter={handleMouseEnter}
    on:mouseleave={handleMouseLeave}
    class:partially-hidden={!fullyVisible}
  >
    <!-- The vertical label shown only when partially hidden -->
    <div class="label-container" aria-hidden={fullyVisible}>
      <span class="label-text">Get PLUS model</span>
    </div>

    <!-- The main popup content -->
    <div class="content flex items-center px-4 py-4">
      <div class="flex-1">
        <p class="font-semibold mb-2">{message}</p>
        <img src={qrCodeUrl} alt="Donation QR" class="w-50 h-50 rounded-md shadow" />
      </div>
    </div>
  </div>
{/if}

<style>
  .popup {
    width: 320px;
    /* Fully visible */
    transform: translateX(0);
    transition: transform 0.5s ease;
    z-index: 9999;
    overflow: visible; /* to show label outside bounding box if needed */
    bottom: 115px; 
  }


  /* Shift right leaving label visible */
  .popup.partially-hidden {
    /* 280px popup width + 40px label width */
    transform: translateX(calc(320px - 48px));
  }

  .label-container {
    position: absolute;
    left: 0;
    bottom: 0;
    top: 0;
    width: 48px;
    background-color: #3371d5; /* match border color */
    display: flex;
    align-items: center;
    justify-content: center;
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    writing-mode: vertical-rl;
    text-orientation: mixed;
    color: white;
    font-weight: bold;
    user-select: none;
    pointer-events: auto; /* so hover triggers when cursor is over label */
  }

  /* Hide the label when fully visible */
  .popup:not(.partially-hidden) .label-container {
    display: none;
  }

  .content {
    margin-left: 48px; /* to avoid being overlapped by label when partially hidden */
    padding-right: 48px;
  }
</style>