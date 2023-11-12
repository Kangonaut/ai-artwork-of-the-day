<script lang="ts">
  import type { PrivateArtwork } from "../types/artwork";

  export let artwork: PrivateArtwork;

  let imageId = Math.floor(Math.random() * 100) + 1;
</script>

<a
  class="max-w-sm rounded-lg overflow-hidden shadow-md variant-ghost-primary card-hover"
  href="/private/artwork/{artwork.id}"
>
  <img
    class="p-0.5 w-full object-cover rounded-lg"
    src="/api/private/artwork/{artwork.id}/image"
    alt="AI generated artwork"
  />
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">{artwork.title}</div>
  </div>
</a>
