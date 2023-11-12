<script lang="ts">
    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<h2 class="h2">Weather Data Source Settings</h2>

<p>TODO: Description</p>

<form method="post" class="grid grid-cols-1 gap-10" action="?/apply">
    <input type="hidden" name="isNew" value={data.settings == null}/>
    <label class="label">
        <span>Longitude</span>
        <input class="input" required name="longitude" type="number" step="0.01" value={data.settings?.longitude}/>
    </label>
    <label class="label">
        <span>Latitude</span>
        <input class="input" required name="latitude" type="number" step="0.01" value={data.settings?.latitude}/>
    </label>
    <button class="btn variant-ghost-primary m-auto">apply</button>
    <button class="btn variant-ghost-error m-auto" formaction="?/disable">disable</button>
</form>