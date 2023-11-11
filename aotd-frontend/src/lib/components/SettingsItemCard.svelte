<script lang="ts">
  export let icon: string;
  export let title: string;
  export let description: string;
  export let url: string;
</script>

<div class="flex p-5">
  <div
    class="badge-icon bg-secondary-800 text-secondary-300 w-fit h-fit p-3 m-auto mr-5"
  >
    <iconify-icon class="text-2xl" {icon} />
  </div>
  <div class="flex-1 text-start mr-10">
    <p class="text-left font-bold text-xl">{title}</p>
    <p>{description}</p>
  </div>
  <a href={url} class="btn btn-md variant-ghost-error m-auto">configure</a>
</div>
