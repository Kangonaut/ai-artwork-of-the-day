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

  // export let data: LayoutData;
</script>

<!-- App Shell -->
<AppShell>
  <svelte:fragment slot="header">
    <!-- App Bar -->
    <AppBar>
      <svelte:fragment slot="lead">
        <strong class="text-xl">AI Artwork of the Day</strong>
      </svelte:fragment>
      <svelte:fragment slot="trail">
        <NavButton title="Home" pathname="/" />
        <NavButton title="Artwork Hub" pathname="/artworks/hub" />
        <NavButton title="My Artworks" pathname="/artworks/personal" pattern="^/artworks/personal/\d" />

        {#if $page.data.user}
          <form action="/auth/logout" method="POST">
            <button type="submit" class="btn btn-md variant-ghost-error"
              >Logout</button
            >
          </form>
        {:else}
          <NavButton title="Login" pathname="/auth/login" />
        {/if}
      </svelte:fragment>
    </AppBar>
  </svelte:fragment>
  <!-- Page Route Content -->
  <slot />
  <svelte:fragment slot="footer">
    <AppBar class="items-center">
      <a
        class="btn btn-sm variant-ghost-surface"
        href="https://github.com/Kangonaut/ai-artwork-of-the-day"
        target="_blank"
        rel="noreferrer"
      >
        <box-icon
          class="mr-1"
          type="logo"
          size="sm"
          name="github"
          color="white"
        />
        GitHub
      </a>
    </AppBar>
  </svelte:fragment>
</AppShell>
