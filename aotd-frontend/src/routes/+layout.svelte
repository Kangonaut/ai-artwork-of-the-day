<script lang="ts">
  import "../app.postcss";
  import { AppShell, AppBar } from "@skeletonlabs/skeleton";

  // Floating UI for Popups
  import {
    computePosition,
    autoUpdate,
    flip,
    shift,
    offset,
    arrow,
  } from "@floating-ui/dom";
  import { storePopup } from "@skeletonlabs/skeleton";
  import { page } from "$app/stores";
  import type { LayoutData } from "./$types";
  import NavButton from "$lib/components/NavButton.svelte";
  storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });

  import "iconify-icon";
</script>

<!-- App Shell -->
<AppShell>
  <svelte:fragment slot="header">
    <!-- App Bar -->
    <AppBar
      background="bg-transparent"
      gridColumns="grid-cols-3"
      slotDefault="place-self-center"
      slotTrail="place-content-end"
    >
      <svelte:fragment slot="lead">
        <a href="/" class="font-bold text-xl">AI Artwork of the Day</a>
      </svelte:fragment>

      <div class="flex space-x-5">
        <NavButton title="Home" pathname="/" />
        <NavButton
          title="Artwork Hub"
          pathname="/public/artworks/"
          pattern="^/public/artworks/\d+"
        />
        <NavButton
          title="My Artworks"
          pathname="/private/artworks/"
          pattern="^/private/artworks/\d+"
        />
      </div>

      <svelte:fragment slot="trail">
        {#if $page.data.user}
          <NavButton
            title={$page.data.user.username}
            pathname="/account"
            pattern="/account.*"
          />
        {:else}
          <NavButton title="Login" pathname="/auth/login" />
        {/if}
      </svelte:fragment>
    </AppBar>
  </svelte:fragment>
  <!-- Page Route Content -->
  <slot />
</AppShell>
