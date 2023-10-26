<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  let imageId = 1;
  const getImageId = () => {
    return imageId++;
  };
</script>

<!-- artworks -->
<div class="grid grid-cols-3 gap-5 bg-white w-full p-10">
  {#each data.artworks as artwork (artwork.id)}
    <div class="card card-hover overflow-hidden">
      <img
        class="brightness-50"
        src="https://picsum.photos/seed/{getImageId()}/1024/1024"
        alt="artwork"
      />
    </div>
  {/each}
</div>
