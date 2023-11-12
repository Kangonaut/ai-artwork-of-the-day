<script lang="ts">
  import { enhance } from "$app/forms";
import type { PageData } from "./$types";

  export let data: PageData;
</script>

<div class="flex justify-center p-10 w-full">
  <div class="grid grid-cols-1 gap-20">
    <div class="grid grid-cols-1 gap-5 max-w-xl m-auto">
        <h2 class="h2 grow">{data.artwork.title}</h2>
        <p class="text-lg">@{data.artwork.user.username}</p>
    </div>
    <img
      class="object-cover rounded-xl max-w-2xl w-full"
      src="/api/public/artwork/{data.artwork.id}/image"
      alt="Sunset in the mountains"
    />
  </div>
</div>
