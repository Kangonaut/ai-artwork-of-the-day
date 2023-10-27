<script lang="ts">
  import ArtworkCard from "$lib/components/ArtworkCard.svelte";
    import type { Artwork } from "$lib/types/artwork";
import type { PageData } from "./$types";

  export let data: PageData;
  const artworks = (data as any).artworks as Artwork[];
</script>

<!-- artworks -->
<div class="grid grid-cols-3 gap-10 w-full p-10">
  {#each artworks as artwork (artwork.id)}
    <ArtworkCard artwork={artwork}/>
  {/each}
</div>
