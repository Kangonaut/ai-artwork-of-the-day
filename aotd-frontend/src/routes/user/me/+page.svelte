<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<div>
  <div>
    <span>ID: </span>
    <span>{data.user.id}</span>
  </div>
  <div>
    <span>Username: </span>
    <span>{data.user.username}</span>
  </div>
</div>
