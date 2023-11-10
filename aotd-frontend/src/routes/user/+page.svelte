<script lang="ts">
  import type { PageData } from "./$types";
  import { page } from "$app/stores";
  import AccountActionCard from "$lib/components/AccountActionCard.svelte";

  export let data: PageData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
  <div class="space-y-10 text-center flex flex-col items-center w-8/12">
    <h1 class="h1">
      <span>Welcome</span>
      <span
        class="bg-gradient-to-br from-blue-500 to-cyan-300 bg-clip-text text-transparent box-decoration-clone"
        >{$page.data.user.username}</span
      >
      <span>!</span>
    </h1>
    <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">Actions</h2>
      <AccountActionCard
        title="Logout"
        description="Logout of your Account. This might be useful if you want to login using another account (or maybe just for security reasons)."
        btnContent="Logout"
        btnAction="/api/auth/logout"
      />
      <hr />
      <AccountActionCard
        title="Delete Account"
        description="Delete your account. All of your data, including your artworks will be deleted indefinately."
        btnContent="Delete Account"
        btnAction="/api/auth/logout"
      />
    </div>
    <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">Data Sources</h2>
      <hr />
      <hr />
    </div>
    <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">Delivery Services</h2>
      <hr />
      <hr />
    </div>
  </div>
</div>
