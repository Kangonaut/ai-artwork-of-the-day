<script lang="ts">
  import ArtworkCard from "$lib/components/ArtworkCard.svelte";
import type { PageData } from "./$types";

  export let data: PageData;
</script>

<!-- artworks -->
<div class="grid grid-cols-3 gap-10 w-full p-10">
  {#each data.artworks as artwork (artwork.id)}
    <ArtworkCard artwork={artwork}/>
  {/each}
</div>
