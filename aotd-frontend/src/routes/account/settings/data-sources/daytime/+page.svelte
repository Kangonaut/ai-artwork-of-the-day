<script lang="ts">
    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<h2 class="h2">Daytime Data Source Settings</h2>

<p>TODO: Description</p>

<form method="post" class="grid grid-cols-1 gap-10" action="?/apply">
    <input type="hidden" name="isNew" value={data.settings == null}/>
    <label class="label">
        <span>Timezone Offset:</span>
        <input class="input" required name="timezoneHourOffset" type="number" value={data.settings?.timezone_hour_offset}/>
    </label>
    <button class="btn variant-ghost-primary m-auto">apply</button>
    <button class="btn variant-ghost-error m-auto" formaction="?/disable">disable</button>
</form>