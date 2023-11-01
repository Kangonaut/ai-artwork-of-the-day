<script lang="ts">
  import { page } from "$app/stores";
</script>

<div
  class="h-full bg-cover"
  class:bg404={$page.status === 404}
  class:bg403={$page.status === 403}
  class:bg401={$page.status === 401}
>
  <div class="container h-full mx-auto flex justify-center items-center">
    <div class="space-y-10 text-center flex flex-col items-center">
      <div class="card p-5">
        {#if $page.status === 404}
          <h1 class="h1">Puff, this page has vanished!</h1>
        {:else if $page.status === 403}
          <h1 class="h1">You are not worthy enough to view this page!</h1>
        {:else if $page.status === 401}
          <h1 class="h1">I am not the account you are looking for!</h1>
        {/if}
        <h1 class="h4">{$page.status}: {$page.error?.message}</h1>
      </div>
    </div>
  </div>
</div>

<style>
  .bg404 {
    background-image: url("/error/404.jpeg");
  }

  .bg403 {
    background-image: url("/error/403.jpeg");
  }

  .bg401 {
    background-image: url("/error/401.jpeg");
  }
</style>
