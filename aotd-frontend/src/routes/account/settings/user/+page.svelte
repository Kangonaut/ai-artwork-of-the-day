<script lang="ts">
    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<h2 class="h2">User Settings</h2>

<p>TODO: Description</p>

<form method="post" class="grid grid-cols-1 gap-10" action="?/apply">
    <input type="hidden" name="isNew" value={data.settings == null}/>
    <label class="label">
        <span>Issue Time:</span>
        <input class="input" required name="issueTime" type="time" value={data.settings?.issue_time}/>
    </label>
    <button class="btn variant-ghost-primary m-auto">apply</button>
    <button class="btn variant-ghost-error m-auto" formaction="?/disable">disable</button>
</form>