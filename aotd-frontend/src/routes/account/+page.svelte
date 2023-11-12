<script lang="ts">
  import { page } from "$app/stores";
  import AccountActionCard from "$lib/components/AccountActionCard.svelte";
  import SettingsItemCard from "$lib/components/SettingsItemCard.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<div class="container h-full mx-auto flex justify-center items-center">
  <div class="space-y-10 text-center flex flex-col items-center p-10 w-8/12">
    <h1 class="h1">
      <span>Welcome</span>
      <span
        class="bg-gradient-to-br from-blue-500 to-cyan-300 bg-clip-text text-transparent box-decoration-clone"
        >{$page.data.user.username}</span
      >
      <span>!</span>
    </h1>

    <!-- User Settings -->
    <!-- <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">General</h2>
      <SettingsItemCard
        title="Account"
        icon="solar:user-bold"
        description="TODO: description"
        url="/account/settings"
        isEnabled={true}
      />
    </div> -->

    <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">Data Sources</h2>
      <SettingsItemCard
        title="Daytime"
        icon="solar:clock-circle-broken"
        description="Let your artworks be dependent on your current time of day."
        url="/account/settings/data-sources/daytime"
        isEnabled={data.isDaytimeEnabled}
      />
      <hr />
      <SettingsItemCard
        title="Art Stlyes"
        icon="solar:pallete-2-line-duotone"
        description="Explore different art styles everyday!"
        url="/account/settings/data-sources/art-styles"
        isEnabled={data.isArtStylesEnabled}
      />
      <hr />
      <SettingsItemCard
        title="Weather"
        icon="solar:cloud-sun-2-bold-duotone"
        description="What's the weather like today? From now on, you don't have to go outside to find out."
        url="/account/settings/data-sources/weather"
        isEnabled={data.isWeatherEnabled}
      />
      <hr />
      <SettingsItemCard
        title="CalDav"
        icon="solar:calendar-linear"
        description="What do you have planned today? Are you going on a hike or planning a cycling tour? Further personalize your artworks using your calendar."
        url="/account/settings/data-sources/caldav"
        isEnabled={data.isCalDavEnabled}
      />
    </div>
    <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">Delivery Services</h2>
      <hr />
      <SettingsItemCard
        title="Pushover"
        icon="tabler:brand-pushover"
        description="A convenient way to receive your daily artwork via push-notifications."
        url="/account/settings/delivery-services/pushover"
        isEnabled={data.isPushoverEnabled}
      />
    </div>
    <div class="grid grid-cols-1 gap-5 text-start w-full">
      <h2 class="h2">Actions</h2>
      <AccountActionCard
        title="Logout"
        description="Logout of your Account. This might be useful if you want to login using another account (or maybe just for security reasons)."
        btnContent="Logout"
        btnAction="/api/auth/logout"
      />

      <!-- Delete Account Action -->
      <!-- <hr />
      <AccountActionCard
        title="Delete Account"
        description="Delete your account. All of your data, including your artworks will be deleted indefinately."
        btnContent="Delete Account"
        btnAction="/api/auth/logout"
      /> -->
    </div>
  </div>
</div>
