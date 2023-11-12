<script lang="ts">
    import { enhance } from "$app/forms";
    import { UiVariant } from "$lib/types/ui";

  export let title: string;
  export let description: string;
  export let btnContent: string;
  export let btnAction: string;
  export let btnVariant = UiVariant.ERROR;
</script>

<div class="flex p-5">
  <div class="flex-1 text-start mr-10">
    <p class="text-left font-bold text-xl">{title}</p>
    <p>{description}</p>
  </div>
  <form method="post" class="flex content-center">
    <button
      type="submit"
      class="btn btn-md m-auto"
      class:variant-ghost-error={btnVariant === UiVariant.ERROR}
      class:variant-ghost-warning={btnVariant === UiVariant.WARNING}
      class:variant-ghost-success={btnVariant === UiVariant.SUCCESS}
      formaction={btnAction}>{btnContent}</button
    >
  </form>
</div>
