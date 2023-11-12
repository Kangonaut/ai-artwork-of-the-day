<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  const checkAll = () => {
    const inputs = document.getElementsByName("artStyles");
    inputs.forEach(input => (input as HTMLInputElement).checked = true);
  }
</script>

<h2 class="h2">Art Styles Data Source Settings</h2>

<p>TODO: Description</p>

<form method="post" class="grid grid-cols-1 gap-10" action="?/apply">
  <div class="grid grid-cols-4 gap-5">
    {#each data.availableArtStyles as availableArtStyle (availableArtStyle.id)}
      <label class="flex items-center space-x-2">
        <input
          class="checkbox"
          type="checkbox"
          name="artStyles"
          value={availableArtStyle.id}
          checked={data.settings.art_styles.includes(availableArtStyle.id)}
        />
        <span>{availableArtStyle.name}</span>
      </label>
    {/each}
  </div>
  <button class="btn variant-ghost-surface m-auto" on:click={checkAll}>select all</button>
  <button class="btn variant-ghost-primary m-auto" type="submit">apply</button>
  <button class="btn variant-ghost-error m-auto" formaction="?/disable"
    >disable</button
  >
</form>
