<script lang="ts">
  import type { PrivateArtwork } from "../types/artwork";

  export let artwork: PrivateArtwork;

  let imageId = Math.floor(Math.random() * 100) + 1;
</script>

<a
  class="max-w-sm rounded-lg overflow-hidden shadow-md variant-ghost-primary card-hover flex flex-col"
  href="/private/artwork/{artwork.id}"
>
  <img
    class="p-0.5 w-full object-cover rounded-lg"
    src="/api/private/artwork/{artwork.id}/image"
    alt="AI generated artwork"
  />
  <div class="flex flex-col h-full p-5">
    <div class="font-normal text-xl">{artwork.title}</div>
  </div>
</a>
