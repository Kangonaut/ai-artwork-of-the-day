<script lang="ts">
    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<h2 class="h2">CalDav Data Source Settings</h2>

<p>TODO: Description</p>

<form method="post" class="grid grid-cols-1 gap-10" action="?/apply">
    <input type="hidden" name="isNew" value={data.settings == null}/>
    <label class="label">
        <span>CalDav URL</span>
        <input class="input" required name="caldav_url" type="url" value={data.settings?.caldav_url}/>
    </label>
    <label class="label">
        <span>Calendar URL</span>
        <input class="input" required name="calendar_url" type="url" value={data.settings?.calendar_url}/>
    </label>
    <label class="label">
        <span>Username</span>
        <input class="input" required name="username" type="text" value={data.settings?.username}/>
    </label>
    <label class="label">
        <span>Password</span>
        <input class="input" required name="password" type="password" value={data.settings?.password}/>
    </label>
    <button class="btn variant-ghost-primary m-auto">apply</button>
    <button class="btn variant-ghost-error m-auto" formaction="?/disable">disable</button>
</form>