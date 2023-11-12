<script lang="ts">
  import { enhance } from "$app/forms";
import type { PageData } from "./$types";

  export let data: PageData;
</script>

<div class="flex justify-center p-10 w-full">
  <div class="grid grid-cols-1 gap-20">
    <div class="grid grid-cols-1 gap-5 max-w-xl m-auto">
      <div class="flex gap-5">
        <h2 class="h2 grow">{data.artwork.title}</h2>
        <form use:enhance method="POST" action={data.artwork.is_public ? "?/hide" : "?/publish"}>
          <button
            class="btn-icon btn-icon-lg"
            class:variant-ghost-success={data.artwork.is_public}
            class:variant-ghost-error={!data.artwork.is_public}
          >
            {#if data.artwork.is_public}
              <iconify-icon icon="solar:global-linear" />
            {:else}
              <iconify-icon icon="solar:lock-keyhole-bold" />
            {/if}
          </button>
        </form>
      </div>
      <p class="text-lg">{data.artwork.image_prompt}</p>
    </div>

    <img
      class="object-cover rounded-xl max-w-2xl w-full"
      src="/api/artwork/{data.artwork.id}/image"
      alt="Sunset in the mountains"
    />
  </div>
</div>
