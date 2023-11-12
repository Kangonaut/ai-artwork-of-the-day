<script lang="ts">
  import type { PublicArtwork } from "../types/artwork";

  export let artwork: PublicArtwork;
</script>

<a
  class="max-w-sm rounded-lg overflow-hidden shadow-md variant-ghost-primary card-hover flex flex-col"
  href="/public/artwork/{artwork.id}"
>
  <img
    class="p-0.5 w-full object-cover rounded-lg"
    src="/api/public/artwork/{artwork.id}/image"
    alt="AI generated artwork"
  />
  <div class="flex flex-col h-full p-5">
    <div class="font-normal text-xl">{artwork.title}</div>
    <div class="mt-auto text-lg font-bold text-right">
      @{artwork.user.username}
    </div>
  </div>
</a>
