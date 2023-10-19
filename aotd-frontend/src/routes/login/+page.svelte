<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<div>
  <h2 class="h2">Login</h2>
  <form>
    <div
      class="my-10 input-group input-group-divider grid-cols-[auto_1fr_auto]"
    >
      <div class="input-group-shim">Username</div>
      <input type="text" title="username" placeholder="hyper-organce-22" />
      <div title="Username already in use.">
        <box-icon type="solid" name="user" color="white" />
      </div>
    </div>
    <div
      class="my-10 input-group input-group-divider grid-cols-[auto_1fr_auto]"
    >
      <div class="input-group-shim">Password</div>
      <input
        type="password"
        title="password"
        placeholder="v3ry s3cure p4ssw0rd 1nd33d!"
      />
      <div title="Password does not fulfill the requirements.">
        <box-icon type="solid" name="key" color="white" />
      </div>
    </div>
    <button type="button" class="btn variant-ghost-primary">
      <span>Submit</span>
      <box-icon type="solid" name="rocket" color="white"></box-icon>
    </button>
  </form>
</div>
