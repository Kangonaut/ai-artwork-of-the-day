<script lang="ts">
    import {page} from "$app/stores";

    export let title: string = "Untitled";
    export let pathname: string = "/untitled";
    export let pattern: string | undefined = undefined;

    $: isActive = $page.url.pathname.match(pattern ?? `^${pathname}$`);
</script>

<a
        class="btn btn-bg"
        class:variant-ghost-primary={isActive}
        class:variant-ghost-surface={!isActive}
        href={pathname}
>
    {title}
</a>