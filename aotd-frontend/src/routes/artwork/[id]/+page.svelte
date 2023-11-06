<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<div class="w-full p-10">
  <div class="flex justify-center mb-10">
    <div class="grid grid-cols-1 justify-center gap-5 max-w-xl w-full">
      <h2 class="h2">{data.artwork.title}</h2>
      <p class="text-lg">{data.artwork.image_prompt}</p>
    </div>
  </div>
  <div class="flex justify-center">
    <img
      class="object-cover rounded-xl max-w-2xl w-full"
      src="/api/artwork/{data.artwork.id}/image"
      alt="Sunset in the mountains"
    />
  </div>
</div>
