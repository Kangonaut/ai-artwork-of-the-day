<script lang="ts">
    export let data;
</script>

<h2 class="h2">Pushover Data Source Settings</h2>

<p>TODO: Description</p>

<form method="post" class="grid grid-cols-1 gap-10" action="?/apply">
    <input type="hidden" name="isNew" value={data.settings == null}/>
    <label class="label">
        <span>User Key</span>
        <input class="input" required name="user_key" maxlength="30" type="text" value={data.settings?.user_key ?? ""}/>
    </label>
    <button class="btn variant-ghost-primary m-auto">apply</button>
    <button class="btn variant-ghost-error m-auto" formaction="?/disable">disable</button>
</form>