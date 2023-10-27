<script lang="ts">
  import type { Artwork } from "$lib/types/artwork";

  export let artwork: Artwork;

  let imageId = Math.floor(Math.random() * 100) + 1;
</script>

<div
  class="max-w-sm rounded-lg overflow-hidden shadow-md variant-ghost-primary card-hover"
>
  <img
    class="p-0.5 w-full object-cover rounded-lg"
    src="http://localhost:5173/api/artwork-image/{artwork.id}"
    alt="Sunset in the mountains"
  />
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">ID: {artwork.id}</div>
    <p>{artwork.image_prompt}</p>
  </div>
</div>
