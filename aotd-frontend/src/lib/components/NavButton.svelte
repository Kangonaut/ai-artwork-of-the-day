<script lang="ts">
    import {page} from "$app/stores";

    export let title = "Untitled";
    export let pathname = "/untitled";
</script>

<a
        class="btn btn-bg"
        class:variant-ghost-primary={$page.url.pathname === pathname}
        class:variant-ghost-surface={$page.url.pathname !== pathname}
        href={pathname}
>
    {title}
</a>