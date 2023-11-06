<script lang="ts">
  import ArtworkCard from "$lib/components/ArtworkCard.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<!-- artworks -->
<div class="p-10 w-full">
  <div class="grid grid-cols-3 gap-10">
    {#each data.artworks as artwork (artwork.id)}
      <ArtworkCard {artwork} />
    {/each}
  </div>
  <form method="GET" class="mt-10 flex items-center justify-start space-x-10">
    <button
      class="btn variant-ghost-secondary"
      disabled={!data.page.previous}
      type="submit"
      formaction="./{data.page.page - 1}">Previous</button
    >

    <button
      class="btn variant-ghost-secondary"
      disabled={!data.page.next}
      type="submit"
      formaction="./{data.page.page + 1}">Next</button
    >
  </form>
</div>
