<script lang="ts">
    import type { LayoutData } from './$types';
    
    export let data: LayoutData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
        <slot/>
    </div>
</div>